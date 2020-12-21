import sys
from trans_parser import translate
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QGridLayout, \
    QTabWidget, QLabel, QComboBox, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.Qt import Qt
from config import config


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.trans = translate()
        self.config = config()
        self.tabs = []
        self.initializeUI()

    # noinspection PyUnresolvedReferences
    def initializeUI(self):
        # self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle(self.trans['rule_setting'])
        self.main_win_layout = QGridLayout()
        self.setup_tab()
        self.setLayout(self.main_win_layout)
        self.add_tab()
        self.setup_global_settings()
        self.set_rules()
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
            groupbox.setTitle(self.trans['global_setting'])
            container = self.tabs[n]
            container_layout = container.layout()
            container_layout.addWidget(groupbox)

            # 添加全局设置的各个信息组件
            mix_label = QLabel(self.trans['mix'])
            layout.addWidget(mix_label, 0, 0)
            mix_combobox = QComboBox()
            self.setdefault(mix_combobox, cfg['global']['mix'])
            layout.addWidget(mix_combobox, 0, 1)

            pages_label = QLabel(self.trans['pages'])
            layout.addWidget(pages_label, 1, 0)
            pages_line_edit = QLineEdit(f'{cfg["global"]["pages"]}')
            layout.addWidget(pages_line_edit, 1, 1)

            qty_label = QLabel(self.trans['qty'])
            layout.addWidget(qty_label, 2, 0)
            qty_line_edit = QLineEdit(f'{cfg["global"]["qty"]}')
            layout.addWidget(qty_line_edit, 2, 1)

            date_label = QLabel(self.trans['show_date'])
            layout.addWidget(date_label, 3, 0)
            date_combobox = QComboBox()
            self.setdefault(date_combobox, cfg['global']['show_date'])
            layout.addWidget(date_combobox, 3, 1)

            quiz_dir_label = QLabel(self.trans['quiz_dir'])
            layout.addWidget(quiz_dir_label, 4, 0)
            quiz_dir_line_edit = QLineEdit(f"{cfg['global']['quiz_dir']}")
            quiz_dir_line_edit.setDisabled(True)
            layout.addWidget(quiz_dir_line_edit, 4, 1)

    def set_rules(self):
        # 算式规则设置区
        for n, tab in enumerate(self.tabs):
            rule_tab_widget = QTabWidget()
            rule_tab_layout = QGridLayout()
            rule_tab_widget.setLayout(rule_tab_layout)
            tab.layout().addWidget(rule_tab_widget)
            rule_containers = []
            cfg = self.config[n]
            for n, rule in enumerate(cfg['rules']):
                # build tab pages
                container = QWidget()
                rule_containers.append(container)
                rule_container_layout = QGridLayout()
                container.setLayout(rule_container_layout)
                rule_tab_widget.addTab(container, f"{self.trans['rule']}{n + 1}")

                widgets = self.build_rule_widgets(rule)
                for row in range(len(widgets) // 4 + 1):
                    for col in range(4):
                        index = row * 4 + col
                        if index < len(widgets):
                            rule_container_layout.addWidget(widgets[4 * row + col], row, col)

                # # display rules
                # weight_label = QLabel(self.trans['weight'])
                #
                # weight_widget = QLineEdit(str(rule['weight']))
                #
                # show_answer_label = QLabel(self.trans['show_answer'])
                #
                # show_answer_widget = QComboBox()
                # self.setdefault(show_answer_widget, rule['show_answer'])
                #
                # separator = QFrame()
                # separator.setFrameShape(QFrame.HLine)
                # separator.setFrameShadow(QFrame.Sunken)
                #
                # first_number_range_label = QLabel(self.trans['first_number'] + self.trans['range'])
                #
                # first_number_range_widget = QLineEdit(str(rule['first_number']['range']))
                #
                # first_number_display_label = QLabel(self.trans['display'])
                #
                # first_number_display_widget = QComboBox()
                # self.setdefault(first_number_display_widget, rule['first_number']['display'])
                # rule_container_layout.addWidget(first_number_display_widget,  5, 1)
                #
                # row = 6
                # for n, step in enumerate(rule['steps']):
                #     operators_label = QLabel(self.trans['operators'])
                #     rule_container_layout.addWidget(operators_label, row + n * 11, 0)
                #     operators_widget = QLineEdit(rule['steps'][0]['operators'])
                #     rule_container_layout.addWidget(operators_widget, row + n * 11, 1)
                #
                #     number_range_label = QLabel(self.trans['number'] + self.trans['range'])
                #     rule_container_layout.addWidget(number_range_label, row + 2 + 11 * n, 0)
                #
                #     number_range_widget = QLineEdit(str(step['number']['range']))
                #     rule_container_layout.addWidget(number_range_widget, row + 2 + 11 * n, 1)
                #
                #     number_display_label = QLabel(self.trans['display'])
                #     rule_container_layout.addWidget(number_display_label, row + 3 + 11 * n, 0)
                #
                #     number_display_widget = QComboBox()
                #     self.setdefault(number_display_widget, step['number']['display'])
                #     rule_container_layout.addWidget(number_display_widget, row + 3 + 11 * n, 1)
                #
                #     ceiling_label = QLabel(self.trans['ceiling'])
                #     rule_container_layout.addWidget(ceiling_label, row + 4 + 11 * n, 0)
                #
                #     ceiling_value = self.trans.get(step['limits']['ceiling'], step['limits']['ceiling'])
                #     ceiling_widget = QLineEdit(str(ceiling_value))
                #     rule_container_layout.addWidget(ceiling_widget, row + 4 + 11 * n, 1)
                #
                #     floor_label = QLabel(self.trans['floor'])
                #     rule_container_layout.addWidget(floor_label, row + 5 + 11 * n, 0)
                #
                #     floor_widget = QLineEdit(self.trans[str(step['limits']['floor'])])
                #     rule_container_layout.addWidget(floor_widget, row + 5 + 11 * n, 1)
                #
                #     brackets_label = QLabel(self.trans['brackets'])
                #     rule_container_layout.addWidget(brackets_label, row + 6 + 11 * n, 0)
                #
                #     brackets_widget = QLineEdit(self.trans[str(step['limits']['brackets'])])
                #     rule_container_layout.addWidget(brackets_widget, row + 6 + 11 * n, 1)
                #
                #     carry_label = QLabel(self.trans['carry'])
                #     rule_container_layout.addWidget(carry_label, row + 7 + 11 * n, 0)
                #
                #     carry_widget = QLineEdit(self.trans[str(step['limits']['carry'])])
                #     rule_container_layout.addWidget(carry_widget, row + 7 + 11 * n, 1)
                #
                #     borrow_label = QLabel(self.trans['borrow'])
                #     rule_container_layout.addWidget(borrow_label, row + 8 + 11 * n, 0)
                #
                #     borrow_widget = QLineEdit(str(step['limits']['borrow']))
                #     rule_container_layout.addWidget(borrow_widget, row + 8 + 11 * n, 1)
                #
                #     remainder_label = QLabel(self.trans['remainder'])
                #     rule_container_layout.addWidget(remainder_label, row + 9 + 11 * n, 0)
                #
                #     remainder_widget = QLineEdit(self.trans[str(step['limits']['remainder'])])
                #     rule_container_layout.addWidget(remainder_widget, row + 9 + 11 * n, 1)
                #
                #     separator = QFrame()
                #     separator.setFrameShape(QFrame.HLine)
                #     separator.setFrameShadow(QFrame.Sunken)
                #     rule_container_layout.addWidget(separator, row + 10 + 11 * n, 0, row + 10 + 11 * n, 1)

    def build_rule_widgets(self, rule):
        widgets = []

        def add_widget(key, value):
            label = QLabel(key)
            widgets.append(label)
            if isinstance(value, bool):
                widget = QComboBox()
                self.setdefault(widget, value)
                widgets.append(widget)
            else:
                value = str(value)
                widget = QLineEdit(self.trans.get(value, value))
                widgets.append(widget)

        sequence = ['weight', {'first_number': ['range', 'display']}, {'steps': {'operators', 'number', 'limits'}} ]
        def get_keys(rule):
            for name in sequence:
                if isinstance(name, dict):
                    if 'first_number' in name:
                        for value in name['first_number']:
                            add_widget(self.trans['first_number'] + self.trans[value], rule['first_number'][value])
                    if 'steps' in name:
                        for n, step in enumerate(rule['steps']):
                            for value in name['steps']:
                                if value == 'operators':
                                    key = self.trans['steps'] + str(n + 1) + self.trans['operators']
                                    content = step['operators']
                                    add_widget(key, content)
                                if value == 'number':
                                    for item in ['range', 'display']:
                                        key = self.trans['steps'] + str(n + 1) + self.trans['number'] + self.trans[item]
                                        content = step['number'][item]
                                        add_widget(key, content)
                                if value == 'limits':
                                    for limit in step['limits']:
                                        key = self.trans['steps'] + str(n+1) + self.trans['limits'] + self.trans[limit]
                                        content = step['limits'][limit]
                                        add_widget(key, content)
                else:
                    add_widget(self.trans[name], rule[name])

        get_keys(rule)

        return widgets

    @staticmethod
    def get_keys(rule):
        keys = []
        for key in rule.keys():
            if isinstance(rule[key], dict):
                for inner_key in rule[key].keys():
                    if isinstance(rule[key][inner_key], dict):
                        get_keys(rule[key][inner_key])
            else:
                keys.append(key)

        return keys

    def setdefault(self, combobox, default):
        combobox.addItems([self.trans['True'], self.trans['False']])
        if default:
            combobox.setCurrentIndex(0)
        else:
            combobox.setCurrentIndex(1)


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
