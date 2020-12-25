import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
import PyQt5.sip

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

