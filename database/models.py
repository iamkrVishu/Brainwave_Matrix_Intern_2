import sqlite3

class Database:
    def __init__(self, db_name="inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create Products Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                category TEXT NOT NULL,
                sku TEXT UNIQUE NOT NULL,
                expiry_date TEXT
            )
        """)

        # Create Users Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('Admin', 'Staff', 'Viewer')) NOT NULL
            )
        """)

        # Create Sales Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity_sold INTEGER NOT NULL,
                sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()