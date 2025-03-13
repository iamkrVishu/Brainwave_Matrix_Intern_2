import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, 
    QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from database.db import Database

class InventoryTrackingTab(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database('inventory.db')  # Single DB instance
        self.initUI()
        self.loadProducts()  # Load available products
        self.updateSaleTable()  # Load sales data

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.productLabel = QLabel('Product:')
        self.productInput = QComboBox()

        self.quantityLabel = QLabel('Quantity:')
        self.quantityInput = QLineEdit()

        self.dateLabel = QLabel('Date (YYYY-MM-DD):')
        self.dateInput = QLineEdit()

        self.layout.addWidget(self.productLabel, 0, 0)
        self.layout.addWidget(self.productInput, 0, 1)
        self.layout.addWidget(self.quantityLabel, 1, 0)
        self.layout.addWidget(self.quantityInput, 1, 1)
        self.layout.addWidget(self.dateLabel, 2, 0)
        self.layout.addWidget(self.dateInput, 2, 1)

        self.addSaleButton = QPushButton('Add Sale')
        self.addSaleButton.clicked.connect(self.addSale)
        self.layout.addWidget(self.addSaleButton, 3, 0, 1, 2)

        self.saleTable = QTableWidget()
        self.saleTable.setRowCount(0)
        self.saleTable.setColumnCount(5)
        self.saleTable.setHorizontalHeaderLabels(['ID', 'Product Name', 'Quantity', 'Date', 'Status'])
        self.saleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.saleTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.saleTable, 4, 0, 1, 2)

    def loadProducts(self):
        """ Load available products into the combo box """
        products = self.db.get_products()
        self.productInput.clear()
        for product in products:
            self.productInput.addItem(f"{product[1]} (ID:{product[0]})", product[0])  # Store product ID as data

    def addSale(self):
        try:
            product_id = self.productInput.currentData()  # Get selected product ID
            quantity = self.quantityInput.text().strip()  # Input quantity as string
            date = self.dateInput.text().strip()

            if not product_id:
                print("❌ Error: No product selected!")
                return

            if not quantity.isdigit():
                print("❌ Error: Quantity must be a number!")
                return

            quantity = int(quantity)  # Convert quantity to integer

            if quantity <= 0:
                print("❌ Error: Quantity must be greater than zero!")
                return

            # Check stock availability
            product = self.db.get_product_by_id(product_id)
            if not product:
                print("❌ Error: Product not found in database!")
                return
            
            available_stock = int(product[3])  # ✅ FIX: Convert stock to integer

            if available_stock < quantity:
                print(f"❌ Error: Not enough stock! Available: {available_stock}, Required: {quantity}")
                return

            # Perform sale transaction
            self.db.add_sale((product_id, quantity, date))

            # Now, update stock only if sale was successful
            self.db.update_product_stock(product_id, available_stock - quantity)

            print("✅ Sale added successfully & stock updated!")
            self.updateSaleTable()

        except ValueError:
            print("❌ Error: Quantity must be a valid integer!")

    def updateSaleTable(self):
        """ Refresh sales table with latest data """
        sales = self.db.get_sales()
        self.saleTable.setRowCount(len(sales))

        for i, sale in enumerate(sales):
            product = self.db.get_product_by_id(sale[1])  # Fetch product details
            product_name = product[1] if product else "Unknown"

            available_stock = int(product[3]) if product else 0
            status = "Stock Available" if available_stock > 0 else "Out of Stock"

            self.saleTable.setItem(i, 0, QTableWidgetItem(str(sale[0])))
            self.saleTable.setItem(i, 1, QTableWidgetItem(product_name))
            self.saleTable.setItem(i, 2, QTableWidgetItem(str(sale[2])))
            self.saleTable.setItem(i, 3, QTableWidgetItem(sale[3]))
            self.saleTable.setItem(i, 4, QTableWidgetItem(status))

        print("✅ Sale Table Updated!")

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InventoryTrackingTab()
    window.show()
    sys.exit(app.exec_())