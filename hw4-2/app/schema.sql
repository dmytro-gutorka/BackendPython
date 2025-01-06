CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT NULL,
    last_name TEXT NULL,
    photo TEXT
);

CREATE TABLE IF NOT EXISTS item(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    photo TEXT DEFAULT null,
    price_per_hour REAL DEFAULT null NULL,
    price_per_day REAL DEFAULT null NULL,
    price_per_week REAL DEFAULT null NULL,
    price_per_month REAL DEFAULT null NULL
);

CREATE TABLE IF NOT EXISTS contract (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    contract_num Integer NOT NULL,
    leaser_id INTEGER NOT NULL,
    taker_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY (leaser_id) REFERENCES user(id),
    FOREIGN KEY (taker_id) REFERENCES user(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
);

CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_user INTEGER NOT NULL,
    to_user INTEGER NOT NULL,
    description TEXT NOT NULL,
    contract INTEGER NOT NULL,
    FOREIGN KEY (from_user) REFERENCES user(id),
    FOREIGN KEY (to_user) REFERENCES user(id),
    FOREIGN KEY (contract) REFERENCES contract(id)

);

CREATE TABLE IF NOT EXISTS favourites(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
);