"""
Найкраща Кава — веб-додаток кав'ярні (курсовий проєкт).

Етап IV: дані зберігаються в базі SQLite (coffee.db).
Читання (Read) — каталог, сторінка позиції, адмін-панель;
створення (Create) — форма бронювання.
Усі SQL-запити параметризовані (плейсхолдери «?») — захист від SQL-ін'єкцій.
"""
import re
from datetime import date, datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from db import close_db, execute, query

app = Flask(__name__)
app.secret_key = "change-me-in-production"  # потрібен для flash-повідомлень і сесій
app.teardown_appcontext(close_db)

BOOKING_TIMES = [f"{h:02d}:{m:02d}" for h in range(8, 21) for m in (0, 30)]

# Сортування: ключ із адреси -> фрагмент ORDER BY.
# Значення беруться лише з цього словника, тому в SQL не потрапляє введення користувача.
SORT_OPTIONS = {
    "popular": ("За популярністю", "m.popularity DESC"),
    "price_asc": ("Спочатку дешевші", "m.price ASC"),
    "price_desc": ("Спочатку дорожчі", "m.price DESC"),
    "name": ("За назвою", "m.name COLLATE NOCASE ASC"),
}

# Основний запит позицій меню разом із назвою категорії (JOIN)
ITEMS_SQL = """
    SELECT m.*, c.name AS category_name, c.slug AS category_slug
    FROM menu_items AS m
    JOIN categories AS c ON c.id = m.category_id
"""


@app.context_processor
def inject_globals():
    return {"current_year": date.today().year}


@app.template_filter("date_ua")
def date_ua(value):
    """2026-12-24 -> 24.12.2026"""
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
    except (TypeError, ValueError):
        return value


# ---------- публічні сторінки ----------

@app.route("/")
def index():
    popular = query(ITEMS_SQL + " ORDER BY m.popularity DESC LIMIT 4")
    return render_template("index.html", popular=popular)


@app.route("/menu")
def menu():
    slug = request.args.get("category", "")
    sort = request.args.get("sort", "popular")
    search = request.args.get("q", "").strip()
    if sort not in SORT_OPTIONS:
        sort = "popular"

    conditions, params = [], []
    if slug:
        conditions.append("c.slug = ?")
        params.append(slug)
    if search:
        conditions.append("m.name LIKE ?")
        params.append(f"%{search}%")

    sql = ITEMS_SQL
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY " + SORT_OPTIONS[sort][1]
    items = query(sql, params)

    categories = query("""
        SELECT c.*, COUNT(m.id) AS items_count
        FROM categories AS c
        LEFT JOIN menu_items AS m ON m.category_id = c.id
        GROUP BY c.id
        ORDER BY c.sort_order
    """)
    total = query("SELECT COUNT(*) AS n FROM menu_items", one=True)["n"]

    return render_template(
        "menu.html",
        items=items,
        categories=categories,
        total=total,
        active_slug=slug,
        sort=sort,
        sort_options={k: v[0] for k, v in SORT_OPTIONS.items()},
        query=search,
    )


@app.route("/menu/<int:item_id>")
def menu_item(item_id):
    item = query(ITEMS_SQL + " WHERE m.id = ?", (item_id,), one=True)
    if item is None:
        abort(404)
    similar = query(
        ITEMS_SQL + " WHERE m.category_id = ? AND m.id != ? ORDER BY m.popularity DESC LIMIT 4",
        (item["category_id"], item_id),
    )
    return render_template("item.html", item=item, similar=similar)


def validate_booking(form):
    """Серверна перевірка форми бронювання. Повертає словник помилок."""
    errors = {}
    name = form.get("name", "").strip()
    phone = form.get("phone", "").strip().replace(" ", "")
    day = form.get("date", "")
    time = form.get("time", "")
    guests = form.get("guests", "")
    comment = form.get("comment", "").strip()

    if not 2 <= len(name) <= 50:
        errors["name"] = "Вкажіть ім'я (від 2 до 50 символів)"
    if not re.fullmatch(r"\+380\d{9}", phone):
        errors["phone"] = "Введіть номер у форматі +380XXXXXXXXX"
    try:
        if datetime.strptime(day, "%Y-%m-%d").date() < date.today():
            errors["date"] = "Дата не може бути в минулому"
    except ValueError:
        errors["date"] = "Оберіть дату"
    if time not in BOOKING_TIMES:
        errors["time"] = "Оберіть час зі списку"
    if not guests.isdigit() or not 1 <= int(guests) <= 10:
        errors["guests"] = "Від 1 до 10 гостей"
    if len(comment) > 300:
        errors["comment"] = "Не більше 300 символів"
    return errors


@app.route("/booking", methods=["GET", "POST"])
def booking():
    values = {"guests": "2"}
    errors = {}
    if request.method == "POST":
        values = request.form.to_dict()
        errors = validate_booking(request.form)
        if not errors:
            execute(
                """INSERT INTO reservations (name, phone, date, time, guests, comment)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    values["name"].strip(),
                    values["phone"].strip().replace(" ", ""),
                    values["date"],
                    values["time"],
                    int(values["guests"]),
                    values.get("comment", "").strip(),
                ),
            )
            flash(
                f"Дякуємо, {values['name'].strip()}! Бронювання на {date_ua(values['date'])} "
                f"о {values['time']} прийнято. Ми зателефонуємо для підтвердження.",
                "success",
            )
            return redirect(url_for("booking"))
    return render_template(
        "booking.html", values=values, errors=errors, times=BOOKING_TIMES, today=date.today().isoformat()
    )


@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        # Етап V: перевірка пароля через check_password_hash і запис у session
        flash("Вхід і реєстрація запрацюють на наступному етапі.", "info")
        return redirect(url_for("account"))
    # Поки немає входу, показуємо бронювання демо-користувача (id = 2, Олена)
    reservations = query(
        "SELECT * FROM reservations WHERE user_id = ? ORDER BY date DESC, time DESC", (2,)
    )
    return render_template("account.html", reservations=reservations)


# ---------- панель адміністратора ----------

@app.route("/admin")
def admin():
    items = query(ITEMS_SQL + " ORDER BY c.sort_order, m.name")
    categories = query("SELECT * FROM categories ORDER BY sort_order")
    return render_template("admin.html", items=items, categories=categories)


@app.route("/admin/menu/<int:item_id>/delete", methods=["POST"])
def admin_delete(item_id):
    item = query("SELECT name FROM menu_items WHERE id = ?", (item_id,), one=True)
    if item is None:
        abort(404)
    # Етап V: тут буде DELETE FROM menu_items WHERE id = ? (після входу адміністратора)
    flash(f"Видалення «{item['name']}» запрацює на наступному етапі.", "info")
    return redirect(url_for("admin"))


# ---------- сторінки помилок ----------

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
