import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView, 
    QHeaderView, QMessageBox
)
from database.db import Database

class ProductManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database('inventory.db')
        self.initUI()
        self.updateProductTable()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.nameLabel = QLabel('Name:')
        self.nameInput = QLineEdit()

        self.priceLabel = QLabel('Price:')
        self.priceInput = QLineEdit()

        self.quantityLabel = QLabel('Quantity:')
        self.quantityInput = QLineEdit()

        self.categoryLabel = QLabel('Category:')
        self.categoryInput = QComboBox()
        self.categoryInput.addItems(['Electronics', 'Fashion', 'Home Goods'])

        self.skuLabel = QLabel('SKU:')
        self.skuInput = QLineEdit()

        self.expiryDateLabel = QLabel('Expiry Date:')
        self.expiryDateInput = QLineEdit()

        # Buttons
        self.addProductButton = QPushButton('Add Product')
        self.addProductButton.clicked.connect(self.addProduct)

        self.editProductButton = QPushButton('Edit Product')
        self.editProductButton.clicked.connect(self.editProduct)

        self.deleteProductButton = QPushButton('Delete Product')
        self.deleteProductButton.clicked.connect(self.deleteProduct)

        # Search Input
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search Product...")
        self.searchInput.textChanged.connect(self.searchProduct)

        # Product Table
        self.productTable = QTableWidget()
        self.productTable.setRowCount(0)
        self.productTable.setColumnCount(7)
        self.productTable.setHorizontalHeaderLabels(['ID', 'Name', 'Price', 'Quantity', 'Category', 'SKU', 'Expiry Date'])
        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.productTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.productTable.itemSelectionChanged.connect(self.loadSelectedProduct)

        # Adding widgets to layout
        self.layout.addWidget(self.nameLabel, 0, 0)
        self.layout.addWidget(self.nameInput, 0, 1)
        self.layout.addWidget(self.priceLabel, 1, 0)
        self.layout.addWidget(self.priceInput, 1, 1)
        self.layout.addWidget(self.quantityLabel, 2, 0)
        self.layout.addWidget(self.quantityInput, 2, 1)
        self.layout.addWidget(self.categoryLabel, 3, 0)
        self.layout.addWidget(self.categoryInput, 3, 1)
        self.layout.addWidget(self.skuLabel, 4, 0)
        self.layout.addWidget(self.skuInput, 4, 1)
        self.layout.addWidget(self.expiryDateLabel, 5, 0)
        self.layout.addWidget(self.expiryDateInput, 5, 1)
        self.layout.addWidget(self.addProductButton, 6, 0, 1, 2)
        self.layout.addWidget(self.editProductButton, 7, 0, 1, 2)
        self.layout.addWidget(self.deleteProductButton, 8, 0, 1, 2)
        self.layout.addWidget(self.searchInput, 9, 0, 1, 2)
        self.layout.addWidget(self.productTable, 10, 0, 1, 2)

    def addProduct(self):
        try:
            name = self.nameInput.text().strip()
            price = float(self.priceInput.text().strip())
            quantity = int(self.quantityInput.text().strip())
            category = self.categoryInput.currentText()
            sku = self.skuInput.text().strip()
            expiry_date = self.expiryDateInput.text().strip()

            if not name or not sku:
                QMessageBox.warning(self, "Input Error", "Name and SKU cannot be empty!")
                return

            product = (name, price, quantity, category, sku, expiry_date)
            if self.db.add_product(product):
                QMessageBox.information(self, "Success", "Product added successfully!")
                self.updateProductTable()
            else:
                QMessageBox.warning(self, "Error", "Duplicate SKU!")

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price and Quantity must be numbers!")

    def editProduct(self):
        selected_row = self.productTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No product selected!")
            return

        try:
            product_id = int(self.productTable.item(selected_row, 0).text())
            name = self.nameInput.text().strip()
            price = float(self.priceInput.text().strip())
            quantity = int(self.quantityInput.text().strip())
            category = self.categoryInput.currentText()
            sku = self.skuInput.text().strip()
            expiry_date = self.expiryDateInput.text().strip()

            if not name or not sku:
                QMessageBox.warning(self, "Input Error", "Name and SKU cannot be empty!")
                return

            # Corrected function call
            if self.db.update_product(product_id, name, price, quantity, category, sku, expiry_date):
                QMessageBox.information(self, "Success", "Product updated successfully!")
                self.updateProductTable()
            else:
                QMessageBox.warning(self, "Error", "Update failed!")

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price and Quantity must be numbers!")

    def deleteProduct(self):
        selected_row = self.productTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No product selected!")
            return

        product_id = int(self.productTable.item(selected_row, 0).text())

        confirmation = QMessageBox.question(self, "Delete Confirmation", "Are you sure?", 
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.db.delete_product(product_id)
            self.updateProductTable()

    def searchProduct(self):
        search_text = self.searchInput.text().strip()
        products = self.db.search_products(search_text)
        self.populateTable(products)

    def updateProductTable(self):
        products = self.db.get_products()
        self.populateTable(products)

    def populateTable(self, products):
        self.productTable.setRowCount(len(products))
        for i, product in enumerate(products):
            for j in range(len(product)):
                self.productTable.setItem(i, j, QTableWidgetItem(str(product[j])))

    def loadSelectedProduct(self):
        selected_row = self.productTable.currentRow()
        if selected_row < 0:
            return

        self.nameInput.setText(self.productTable.item(selected_row, 1).text())
        self.priceInput.setText(self.productTable.item(selected_row, 2).text())
        self.quantityInput.setText(self.productTable.item(selected_row, 3).text())
        self.categoryInput.setCurrentText(self.productTable.item(selected_row, 4).text())
        self.skuInput.setText(self.productTable.item(selected_row, 5).text())
        self.expiryDateInput.setText(self.productTable.item(selected_row, 6).text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProductManagementTab()
    window.show()
    sys.exit(app.exec_())