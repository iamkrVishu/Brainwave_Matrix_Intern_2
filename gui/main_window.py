import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QAction, QMessageBox
from gui.product_management import ProductManagementTab
from gui.reporting_notifications import ReportingNotificationsTab
from gui.user_authentication import UserAuthenticationTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 900, 600)

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # Adding tabs
        self.productTab = ProductManagementTab()
        self.reportTab = ReportingNotificationsTab()
        self.authTab = UserAuthenticationTab()

        self.stackedWidget.addWidget(self.productTab)
        self.stackedWidget.addWidget(self.reportTab)
        self.stackedWidget.addWidget(self.authTab)

        # Create menu bar
        self.create_menu()

    def create_menu(self):
        menuBar = self.menuBar()

        # Product Menu
        productMenu = menuBar.addMenu("Products")
        productAction = QAction("Manage Products", self)
        productAction.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.productTab))
        productMenu.addAction(productAction)

        # Reports Menu
        reportMenu = menuBar.addMenu("Reports")
        reportAction = QAction("Generate Reports", self)
        reportAction.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.reportTab))
        reportMenu.addAction(reportAction)

        # User Management
        userMenu = menuBar.addMenu("User Management")
        userAction = QAction("Manage Users", self)
        userAction.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.authTab))
        userMenu.addAction(userAction)

        # Logout Option
        logoutAction = QAction("Logout", self)
        logoutAction.triggered.connect(self.logout)
        menuBar.addAction(logoutAction)

    def logout(self):
        confirm = QMessageBox.question(self, "Logout", "Are you sure you want to log out?", 
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())