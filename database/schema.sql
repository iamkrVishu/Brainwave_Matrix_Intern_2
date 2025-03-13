CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    category TEXT NOT NULL,
    sku TEXT NOT NULL UNIQUE,  -- Ensuring SKU is unique
    expiry_date DATE DEFAULT NULL,
    low_stock_threshold INTEGER DEFAULT 5  -- New column for low-stock alerts
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
);