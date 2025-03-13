import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from database.db import Database
from reports.excel_report import generate_excel_report
from reports.pdf_report import generate_pdf_report
from utils.email_utils import send_email

class ReportingNotificationsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database('inventory.db')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Generate Excel Report Button
        self.reportButton = QPushButton('Generate Excel Report')
        self.reportButton.clicked.connect(self.generateExcelReport)
        layout.addWidget(self.reportButton)

        # Generate PDF Report Button
        self.pdfReportButton = QPushButton('Generate PDF Report')
        self.pdfReportButton.clicked.connect(self.generatePDFReport)
        layout.addWidget(self.pdfReportButton)

        # Send Low-Stock Email Button
        self.emailButton = QPushButton('Send Low Stock Email Alert')
        self.emailButton.clicked.connect(self.sendLowStockEmail)
        layout.addWidget(self.emailButton)

    def generateExcelReport(self):
        products = self.db.get_products()
        sales = self.db.get_sales()
        file_path = generate_excel_report(products, sales)
        
        if os.path.exists(file_path):
            QMessageBox.information(self, "Success", "Excel report generated successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to generate Excel report.")

    def generatePDFReport(self):
        products = self.db.get_products()
        sales = self.db.get_sales()
        file_path = generate_pdf_report(products, sales)

        if os.path.exists(file_path):
            QMessageBox.information(self, "Success", "PDF report generated successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to generate PDF report.")

    def sendLowStockEmail(self):
        low_stock_items = self.db.get_low_stock_products()
        if not low_stock_items:
            QMessageBox.information(self, "Info", "No low-stock items found.")
            return

        email_body = "The following items are running low in stock:\n\n"
        for item in low_stock_items:
            email_body += f"{item[1]} (SKU: {item[5]}) - Only {item[3]} left!\n"

        try:
            send_email("Low Stock Alert", email_body, "your-email@gmail.com", "recipient-email@gmail.com", "your-email-password")
            QMessageBox.information(self, "Success", "Low-stock email sent successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to send email: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportingNotificationsTab()
    window.show()
    sys.exit(app.exec_())