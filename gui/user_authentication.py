import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from database.db import Database

class UserAuthenticationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Database('inventory.db')  # Single DB instance
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.usernameLabel = QLabel('Username:')
        self.usernameInput = QLineEdit()

        self.passwordLabel = QLabel('Password:')
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)  # Hide password

        self.roleLabel = QLabel('Role:')
        self.roleInput = QComboBox()
        self.roleInput.addItems(['Admin', 'Staff', 'Viewer'])

        self.layout.addWidget(self.usernameLabel, 0, 0)
        self.layout.addWidget(self.usernameInput, 0, 1)
        self.layout.addWidget(self.passwordLabel, 1, 0)
        self.layout.addWidget(self.passwordInput, 1, 1)
        self.layout.addWidget(self.roleLabel, 2, 0)
        self.layout.addWidget(self.roleInput, 2, 1)

        self.addUserButton = QPushButton('Add User')
        self.addUserButton.clicked.connect(self.addUser)
        self.layout.addWidget(self.addUserButton, 3, 0, 1, 2)

        self.loginButton = QPushButton('Login')
        self.loginButton.clicked.connect(self.login)
        self.layout.addWidget(self.loginButton, 4, 0, 1, 2)

    def hash_password(self, password):
        """ Hash password using SHA-256 """
        return hashlib.sha256(password.encode()).hexdigest()

    def addUser(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()
        role = self.roleInput.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and Password cannot be empty!")
            return

        hashed_password = self.hash_password(password)

        if self.db.user_exists(username):
            QMessageBox.warning(self, "Error", "Username already exists!")
            return

        self.db.add_user((username, hashed_password, role))
        QMessageBox.information(self, "Success", "User added successfully!")

    def login(self):
        username = self.usernameInput.text().strip()
        password = self.passwordInput.text().strip()
        hashed_password = self.hash_password(password)

        user = self.db.validate_user(username, hashed_password)
        if user:
            QMessageBox.information(self, "Login Successful", f"Welcome, {user[1]} ({user[3]})")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserAuthenticationTab()
    window.show()
    sys.exit(app.exec_())