import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QGridLayout, \
    QTabWidget, QLabel, QComboBox, QLineEdit

from config import config


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config = config()
        self.tabs = []
        self.initializeUI()

    # noinspection PyUnresolvedReferences
    def initializeUI(self):
        # self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("算式规则设置")
        self.main_win_layout = QGridLayout()
        self.setup_tab()
        self.setLayout(self.main_win_layout)
        self.add_tab()
        self.setup_global_settings()
        self.show()

    def setup_tab(self):
        self.tab_widget = QTabWidget()
        self.tab_container_layout = QGridLayout()
        self.main_win_layout.addWidget(self.tab_widget)

    def add_tab(self):
        for cfg in self.config:
            user = cfg['user']
            container = QWidget()
            self.tabs.append(container)
            container.setLayout(QGridLayout())
            self.tab_widget.addTab(container, user)

    def setup_global_settings(self):
        for n, cfg in enumerate(self.config):
            user = cfg['user']
            # 添加全局设置groupbox
            groupbox = QGroupBox()
            layout = QGridLayout()
            groupbox.setLayout(layout)
            groupbox.setTitle("全局设置")
            container = self.tabs[n]
            container_layout = container.layout()
            container_layout.addWidget(groupbox)

            # 添加全局设置的各个信息组件
            mix_label = QLabel('题型混合')
            layout.addWidget(mix_label)
            mix_combobox = QComboBox()
            mix_combobox.addItems(['否', '是'])
            layout.addWidget(mix_combobox, 0, 1)

            pages_label = QLabel('页数')
            layout.addWidget(pages_label, 0, 2)
            pages_line_edit = QLineEdit(f'{cfg["global"]["pages"]}')
            layout.addWidget(pages_line_edit, 0, 3)

            qty_label = QLabel('试题数量')
            layout.addWidget(qty_label, 1, 0)
            qty_line_edit = QLineEdit(f'{cfg["global"]["qty"]}')
            layout.addWidget(qty_line_edit, 1, 1)

            date_label = QLabel('显示日期')
            layout.addWidget(date_label, 1, 2)
            date_combobox = QComboBox()
            date_combobox.addItems(['是', '否'])
            layout.addWidget(date_combobox, 1, 3)

            quiz_dir_label = QLabel('输出文件夹')
            layout.addWidget(quiz_dir_label, 2, 0)
            quiz_dir_line_edit = QLineEdit(f"{cfg['global']['quiz_dir']}")
            quiz_dir_line_edit.setDisabled(True)
            layout.addWidget(quiz_dir_line_edit, 2, 1, 2, 2)




def on_user_button(self):
    self.close()


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
