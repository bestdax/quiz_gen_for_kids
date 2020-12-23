import pprint
import re
import sys
from translate import translate
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QGridLayout, \
    QTabWidget, QLabel, QComboBox, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.Qt import Qt
from config import config, write_cfg
from quizzes import quiz_gen, gen_pdf_quiz


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config = config()
        self.tabs = []
        self.initializeUI()

    # noinspection PyUnresolvedReferences
    def initializeUI(self):
        self.setWindowTitle(translate('rule_setting'))
        self.main_win_layout = QGridLayout()
        self.setup_tab()
        self.setLayout(self.main_win_layout)
        self.add_tab()
        self.setup_global_settings()
        self.set_rules()
        self.setup_buttons()
        self.show()

    def setup_tab(self):
        self.tab_widget = QTabWidget()
        self.tab_container_layout = QGridLayout()
        self.main_win_layout.addWidget(self.tab_widget)

    def add_tab(self):
        for user in self.config:
            container = QWidget()
            container.name = user
            self.tabs.append(container)
            container.setLayout(QGridLayout())
            self.tab_widget.addTab(container, user)

    def setup_global_settings(self):
        for n, user in enumerate(self.config):
            # setup global setting groupbox
            tab_container = self.tabs[n]
            groupbox = QGroupBox()
            layout = QGridLayout()
            groupbox.setLayout(layout)
            groupbox.setTitle(translate('global_setting'))
            groupbox.name = 'global'
            tab_container.layout().addWidget(groupbox)
            groupbox_layout = groupbox.layout()

            # setup global setting widgets
            widgets = []
            sequence = ['mix', 'pages', 'show_date', 'qty', 'quiz_dir']
            for key in sequence:
                label, widget = self.add_widget(key, self.config[user]['global'][key])
                if widget.name == 'quiz_dir':
                    widget.setDisabled(True)
                widgets.append(label)
                widgets.append(widget)
            for row in range(3):
                for col in range(4):
                    index = row * 4 + col
                    if index < len(widgets):
                        widget = widgets[index]
                        if widget.name == 'quiz_dir':
                            groupbox_layout.addWidget(widget, row, col, 1, 2)
                        else:
                            groupbox_layout.addWidget(widget, row, col)

    def set_rules(self):
        # 算式规则设置区
        for n, tab in enumerate(self.tabs):
            rule_tab_widget = QTabWidget()
            rule_tab_layout = QGridLayout()
            rule_tab_widget.setLayout(rule_tab_layout)
            tab.layout().addWidget(rule_tab_widget)
            rule_containers = []
            user = tab.name
            for n, rule in enumerate(self.config[user]['rules']):
                # build tab pages
                container = QWidget()
                rule_containers.append(container)
                rule_container_layout = QGridLayout()
                container.setLayout(rule_container_layout)
                rule_tab_widget.addTab(container, f"{translate('rule')}{n + 1}")
                container.name = f"rule {n+1}"

                example_label = QLabel(translate('example'))
                example_content_label = QLabel(quiz_gen(rule))
                example_content_label.setObjectName('example')
                rule_container_layout.addWidget(example_label, 0, 0)
                rule_container_layout.addWidget(example_content_label, 0, 1, 1, 2)

                refresh_button = QPushButton(translate('refresh'))
                rule_container_layout.addWidget(refresh_button, 0, 3)
                refresh_button.clicked.connect(self.onRefresh)

                widgets = self.build_rule_widgets(rule)
                for row in range(len(widgets) // 4 + 1):
                    for col in range(4):
                        index = row * 4 + col
                        if index < len(widgets):
                            rule_container_layout.addWidget(widgets[4 * row + col], row + 1, col)

    def add_widget(self, key, value):
        """
        :param key: a string for a label widget
        :param value: a string for the text of a combobox or lineedit
        :return: a label and a widget (combobox or lineedit)
        """
        name_of_label = translate(key.split()[-1])
        label = QLabel(name_of_label)
        label.name = key
        if isinstance(value, bool):
            widget = QComboBox()
            widget.name = key
            print(widget.currentText())
            self.setup_combo_and_default(widget, translate(str(value)))
            widget.currentIndexChanged.connect(self.onChange)
        else:
            value = str(translate(value))
            widget = QLineEdit()
            widget.name = key
            widget.setText(value)
            widget.textChanged.connect(self.onChange)
        return label, widget

    def build_rule_widgets(self, rule):
        widgets = []
        sequence = ['weight',
                    {'first_number': ['range', 'display']},
                    {'steps': ['operators', 'number', 'limits']}]
        for key in sequence:
            if isinstance(key, dict):
                if 'first_number' in key:
                    for value in key['first_number']:
                        first_number_key = value
                        content = rule['first_number'][value]
                        label, widget = self.add_widget('first_number ' + first_number_key, content)
                        widgets.append(label)
                        widgets.append(widget)
                if 'steps' in key:
                    for n, step in enumerate(rule['steps']):
                        for value in key['steps']:
                            if value == 'limits':
                                for limit in step['limits']:
                                    limit_key = limit
                                    content = step['limits'][limit]
                                    label, widget = self.add_widget(f'steps {n} limits {limit_key}', content)
                                    widgets.append(label)
                                    widgets.append(widget)
                            elif value == 'number':
                                for number_key in ['range', 'display']:
                                    content = step['number'][number_key]
                                    label, widget = self.add_widget(f'steps {n} number {number_key}', content)
                                    widgets.append(label)
                                    widgets.append(widget)
                            else:
                                subkey = value
                                content = step[subkey]
                                label, widget = self.add_widget(subkey, content)
                                widgets.append(label)
                                widgets.append(widget)
            else:
                label, widget = self.add_widget(key, rule[key])
                widgets.append(label)
                widgets.append(widget)

        return widgets

    @staticmethod
    def setup_combo_and_default(combobox, default):
        combobox.addItems([translate('True'), translate('False')])
        if translate(default):
            combobox.setCurrentIndex(0)
        else:
            combobox.setCurrentIndex(1)

    def setup_buttons(self):
        gen_button = QPushButton(translate('gen_quiz'))
        gen_button.clicked.connect(lambda: gen_pdf_quiz(self.config))
        self.layout().addWidget(gen_button)

    def onChange(self):
        sender = self.sender()
        if sender.parent().name == 'global':
            user = sender.parent().parent().name
            if isinstance(sender, QLineEdit):
                if sender.text().isdigit():
                    self.config[user]['global'][sender.name] = eval(sender.text())
            if isinstance(sender, QComboBox):
                self.config[user]['global'][sender.name] = translate(sender.currentText())
        else:
            user = sender.parent().parent().parent().parent().name
            rule_index = int(sender.parent().name.split()[1]) - 1
            rule = self.config[user]['rules'][rule_index]
            if isinstance(sender, QLineEdit):
                try:
                    value = eval(sender.text())
                except NameError:
                    value = sender.text()
            else:
                value = translate(sender.currentText())

            target = f'rule'
            for item in sender.name.split():
                if item.isdigit():
                    target += f'[{item}]'
                else:
                    target += f'["{item}"]'
            exec(target + '= value')

        write_cfg(self.config)

    def onRefresh(self):
        sender = self.sender()
        user = sender.parent().parent().parent().parent().name
        rule_index = int(sender.parent().name.split()[1]) - 1
        rule = self.config[user]['rules'][rule_index]
        quiz = quiz_gen(rule)
        for widget in sender.parent().children():
            if widget.objectName() == 'example':
                widget.setText(quiz)


def on_user_button(self):
    self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
