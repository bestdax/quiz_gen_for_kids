import sys

from PyQt5.QtWidgets import QWidget, QApplication


class UserSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("请选择用户名称")
        self.show()


def run():
    app = QApplication(sys.argv)
    window = UserSelector()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserSelector()
    sys.exit(app.exec_())
