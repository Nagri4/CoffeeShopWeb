"""Підключення до бази даних SQLite."""
import sqlite3
from pathlib import Path

from flask import g

DATABASE = Path(__file__).parent / "coffee.db"


def get_db():
    """Повертає з'єднання з БД (одне на запит)."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row          # рядки можна читати як item["name"]
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(exception=None):
    """Закриває з'єднання наприкінці запиту."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, params=(), one=False):
    """SELECT-запит. Параметри передаються лише через плейсхолдери «?»."""
    cur = get_db().execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows


def execute(sql, params=()):
    """INSERT / UPDATE / DELETE із збереженням змін. Повертає id нового запису."""
    db = get_db()
    cur = db.execute(sql, params)
    db.commit()
    return cur.lastrowid
