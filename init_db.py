"""
Створює базу даних coffee.db і заповнює її початковими даними.

Запуск:  python init_db.py
Увага: якщо база вже існує, її буде створено заново (усі бронювання зникнуть).
"""
import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash

from data import CATEGORIES, MENU_ITEMS

BASE = Path(__file__).parent
DATABASE = BASE / "coffee.db"


def init_db():
    con = sqlite3.connect(DATABASE)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript((BASE / "schema.sql").read_text(encoding="utf-8"))

    for i, c in enumerate(CATEGORIES):
        con.execute(
            "INSERT INTO categories (id, name, slug, sort_order) VALUES (?, ?, ?, ?)",
            (c["id"], c["name"], c["slug"], i),
        )

    for m in MENU_ITEMS:
        con.execute(
            """INSERT INTO menu_items
               (id, category_id, name, description, details, price, volume, calories,
                label, image, is_available, popularity)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (m["id"], m["category_id"], m["name"], m["description"], m["details"], m["price"],
             m["volume"], m["calories"], m["label"], m["image"], int(m["is_available"]), m["popularity"]),
        )

    # Тестові акаунти (паролі зберігаються лише як хеш)
    users = [
        ("Адміністратор", "admin@coffee.local", "", "admin123", "admin"),
        ("Олена", "olena@example.com", "+380671234567", "olena123", "guest"),
    ]
    for name, email, phone, password, role in users:
        con.execute(
            "INSERT INTO users (name, email, phone, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone, generate_password_hash(password), role),
        )

    # Кілька бронювань для демонстрації (user_id = 2 — Олена)
    reservations = [
        (2, "Олена", "+380671234567", "2026-12-24", "18:30", 2, "Біля вікна", "confirmed"),
        (2, "Олена", "+380671234567", "2026-12-31", "10:00", 4, "", "pending"),
        (2, "Олена", "+380671234567", "2026-10-12", "19:00", 2, "", "done"),
    ]
    con.executemany(
        """INSERT INTO reservations (user_id, name, phone, date, time, guests, comment, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        reservations,
    )

    con.commit()
    con.close()


if __name__ == "__main__":
    init_db()
    print(f"Базу даних створено: {DATABASE.name}")
