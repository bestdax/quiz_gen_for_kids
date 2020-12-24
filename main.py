import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
import PyQt5.sip

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())

