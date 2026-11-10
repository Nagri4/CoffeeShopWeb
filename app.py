"""
Найкраща Кава — веб-додаток кав'ярні (курсовий проєкт).

Етап II–III: сторінки, шаблони Jinja2 та обробка форм.
Дані поки що зберігаються у списках Python (data.py);
на етапі IV їх буде перенесено в базу даних SQLite.
"""
import re
from datetime import date, datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from data import BOOKING_TIMES, CATEGORIES, MENU_ITEMS, MY_RESERVATIONS

app = Flask(__name__)
app.secret_key = "change-me-in-production"  # потрібен для flash-повідомлень і сесій

SORT_OPTIONS = {
    "popular": "За популярністю",
    "price_asc": "Спочатку дешевші",
    "price_desc": "Спочатку дорожчі",
    "name": "За назвою",
}


# ---------- допоміжні функції ----------

def get_category(category_id):
    return next((c for c in CATEGORIES if c["id"] == category_id), None)


def get_category_by_slug(slug):
    return next((c for c in CATEGORIES if c["slug"] == slug), None)


def get_item(item_id):
    return next((i for i in MENU_ITEMS if i["id"] == item_id), None)


@app.context_processor
def inject_helpers():
    """Робить функції доступними в усіх шаблонах."""
    return {"get_category": get_category, "current_year": date.today().year}


# ---------- публічні сторінки ----------

@app.route("/")
def index():
    popular = sorted(MENU_ITEMS, key=lambda i: i["popularity"], reverse=True)[:4]
    return render_template("index.html", popular=popular)


@app.route("/menu")
def menu():
    slug = request.args.get("category", "")
    sort = request.args.get("sort", "popular")
    query = request.args.get("q", "").strip()

    items = list(MENU_ITEMS)
    active_category = get_category_by_slug(slug)
    if active_category:
        items = [i for i in items if i["category_id"] == active_category["id"]]
    if query:
        items = [i for i in items if query.lower() in i["name"].lower()]

    if sort == "price_asc":
        items.sort(key=lambda i: i["price"])
    elif sort == "price_desc":
        items.sort(key=lambda i: i["price"], reverse=True)
    elif sort == "name":
        items.sort(key=lambda i: i["name"])
    else:
        sort = "popular"
        items.sort(key=lambda i: i["popularity"], reverse=True)

    counts = {c["id"]: sum(1 for i in MENU_ITEMS if i["category_id"] == c["id"]) for c in CATEGORIES}
    return render_template(
        "menu.html",
        items=items,
        categories=CATEGORIES,
        counts=counts,
        total=len(MENU_ITEMS),
        active_slug=active_category["slug"] if active_category else "",
        sort=sort,
        sort_options=SORT_OPTIONS,
        query=query,
    )


@app.route("/menu/<int:item_id>")
def menu_item(item_id):
    item = get_item(item_id)
    if item is None:
        abort(404)
    similar = [i for i in MENU_ITEMS if i["category_id"] == item["category_id"] and i["id"] != item["id"]][:4]
    return render_template("item.html", item=item, category=get_category(item["category_id"]), similar=similar)


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
            # Етап IV: тут буде INSERT у таблицю reservations
            flash(f"Дякуємо, {values['name'].strip()}! Бронювання на {values['date']} о {values['time']} прийнято.", "success")
            return redirect(url_for("booking"))
    return render_template(
        "booking.html", values=values, errors=errors, times=BOOKING_TIMES, today=date.today().isoformat()
    )


@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        # Етап V: перевірка пароля через check_password_hash і запис у session
        flash("Вхід і реєстрація запрацюють після підключення бази даних.", "info")
        return redirect(url_for("account"))
    return render_template("account.html", reservations=MY_RESERVATIONS)


# ---------- панель адміністратора ----------

@app.route("/admin")
def admin():
    return render_template("admin.html", items=MENU_ITEMS, categories=CATEGORIES)


@app.route("/admin/menu/<int:item_id>/delete", methods=["POST"])
def admin_delete(item_id):
    item = get_item(item_id)
    if item is None:
        abort(404)
    # Етап V: тут буде DELETE FROM menu_items WHERE id = ?
    flash(f"Позицію «{item['name']}» буде видалено після підключення бази даних.", "info")
    return redirect(url_for("admin"))


# ---------- сторінки помилок ----------

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
