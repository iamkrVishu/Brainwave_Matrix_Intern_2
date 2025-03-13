import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """ Entry point of the application """
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()