-- =========================================================
-- Найкраща Кава — схема бази даних SQLite
-- Запуск: python init_db.py (створює файл coffee.db)
-- =========================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

-- Категорії меню: Кава, Чай, Десерти...
CREATE TABLE categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL UNIQUE,
    slug        TEXT    NOT NULL UNIQUE,          -- для адреси: /menu?category=coffee
    sort_order  INTEGER NOT NULL DEFAULT 0
);

-- Позиції меню. Кожна належить одній категорії (зв'язок «один до багатьох»)
CREATE TABLE menu_items (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id   INTEGER NOT NULL,
    name          TEXT    NOT NULL,
    description   TEXT    NOT NULL DEFAULT '',    -- короткий опис для картки
    details       TEXT    NOT NULL DEFAULT '',    -- повний опис для сторінки позиції
    price         INTEGER NOT NULL CHECK (price > 0),
    volume        TEXT    NOT NULL DEFAULT '',    -- «250 мл», «80 г»
    calories      TEXT    NOT NULL DEFAULT '',
    label         TEXT    NOT NULL DEFAULT '',    -- «Хіт», «Новинка» або порожньо
    image         TEXT    NOT NULL DEFAULT '',    -- назва файлу в static/img/menu/
    is_available  INTEGER NOT NULL DEFAULT 1,     -- 1 — в наявності, 0 — немає
    popularity    INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE RESTRICT
);

-- Користувачі (гості й адміністратор). Пароль зберігається лише як хеш
CREATE TABLE users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT    NOT NULL,
    email          TEXT    NOT NULL UNIQUE,
    phone          TEXT    NOT NULL DEFAULT '',
    password_hash  TEXT    NOT NULL,
    role           TEXT    NOT NULL DEFAULT 'guest' CHECK (role IN ('guest', 'admin')),
    created_at     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Бронювання столиків. user_id може бути порожнім, якщо бронював гість без входу
CREATE TABLE reservations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    name        TEXT    NOT NULL,
    phone       TEXT    NOT NULL,
    date        TEXT    NOT NULL,                 -- РРРР-ММ-ДД
    time        TEXT    NOT NULL,                 -- ГГ:ХХ
    guests      INTEGER NOT NULL CHECK (guests BETWEEN 1 AND 10),
    comment     TEXT    NOT NULL DEFAULT '',
    status      TEXT    NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'confirmed', 'done', 'cancelled')),
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX idx_menu_items_category ON menu_items (category_id);
CREATE INDEX idx_reservations_user ON reservations (user_id);
