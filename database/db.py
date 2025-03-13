import sqlite3
from bcrypt import hashpw, gensalt, checkpw

class Database:
    def __init__(self, db_name="inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('Admin', 'Staff', 'Viewer')) NOT NULL
            )
        """)
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

    ## ✅ PRODUCT MANAGEMENT FUNCTIONS ##
    def add_product(self, product):
        """Add a new product (Ensures unique SKU)."""
        try:
            self.cursor.execute("""
                INSERT INTO products (name, price, quantity, category, sku, expiry_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, product)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Duplicate SKU

    def update_product(self, product_id, name, price, quantity, category, sku, expiry_date):
        """Update an existing product."""
        self.cursor.execute("""
            UPDATE products 
            SET name=?, price=?, quantity=?, category=?, sku=?, expiry_date=? 
            WHERE id=?
        """, (name, price, quantity, category, sku, expiry_date, product_id))
        self.conn.commit()
        return True  # Return True if update succeeds

    def delete_product(self, product_id):
        """Delete a product by ID."""
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()

    def get_products(self):
        """Retrieve all products."""
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def search_products(self, search_text):
        """Search products by name, SKU, or category."""
        self.cursor.execute("""
            SELECT * FROM products WHERE 
            name LIKE ? OR sku LIKE ? OR category LIKE ?
        """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
        return self.cursor.fetchall()

    ## ✅ USER AUTHENTICATION FUNCTIONS ##
    def add_user(self, user):
        """Add a new user with hashed password."""
        username, password, role = user
        hashed_password = hashpw(password.encode(), gensalt())  # Hash password
        try:
            self.cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            """, (username, hashed_password, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Duplicate username

    def validate_user(self, username, password):
        """Check user credentials."""
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if user and checkpw(password.encode(), user[2].encode()):  # Compare hashed passwords
            return user
        return None

    ## ✅ SALES & STOCK MANAGEMENT ##
    def add_sale(self, product_id, quantity_sold):
        """Record a sale & update stock."""
        self.cursor.execute("INSERT INTO sales (product_id, quantity_sold) VALUES (?, ?)", (product_id, quantity_sold))
        self.cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity_sold, product_id))
        self.conn.commit()

    def get_sales(self):
        """Retrieve all sales records."""
        self.cursor.execute("SELECT * FROM sales")
        return self.cursor.fetchall()

    def close(self):
        """Close database connection."""
        self.conn.close()