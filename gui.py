import pprint
import re
import sys
from translate import translate
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QGridLayout, \
    QTabWidget, QLabel, QComboBox, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.Qt import Qt
from config import config, write_cfg, add_step, rm_step
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
                widgets.extend([label, widget])
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
        # quiz rule setting
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
                container.name = f"rule {n}"
                widgets = []

                example_label = QLabel(translate('example'))
                example_content_label = QLabel(quiz_gen(rule))
                example_content_label.setObjectName('example')
                widgets.append(example_label)
                widgets.append(example_content_label)

                refresh_button = QPushButton(translate('refresh'))
                rule_container_layout.addWidget(refresh_button, 0, 3)
                refresh_button.clicked.connect(self.onRefresh)
                widgets.append(refresh_button)

                # build rule widgets and put them into correct positions
                widgets.extend(self.build_rule_widgets(rule))

                # add buttons to add and delete steps
                add_step_button = QPushButton(translate('add_step'))
                add_step_button.clicked.connect(self.on_add_step)
                rm_step_button = QPushButton(translate('rm_step'))
                rm_step_button.clicked.connect(self.on_rm_step)
                widgets.append(add_step_button)
                widgets.append(rm_step_button)
                container.widgets = widgets
                self.lay_rule_widgets(rule_container_layout, widgets)

    def lay_rule_widgets(self, layout, widgets):
        layout.addWidget(widgets[0], 0, 0)
        layout.addWidget(widgets[1], 0, 1, 1, 2)
        layout.addWidget(widgets[2], 0, 3)
        row, col = 1, 0
        for widget in widgets[3:-2]:
            span = 1
            one_line_items = ['weight', 'operators', 'show_answer']
            for item in one_line_items:
                if widget.name.endswith(item):
                    span = 3
            layout.addWidget(widget, row, col, 1, span)
            col += span
            if widget.name.endswith('remainder'):
                sep = self.setup_separator()
                row += 1
                col = 0
                span = 4
                layout.addWidget(sep, row, col, 1, span)
                row += 1
            if col == 4:
                col = 0
                row += 1
        layout.addWidget(widgets[-2], row, 0)
        layout.addWidget(widgets[-1], row, 1)

    def add_widget(self, key, value):
        """
        :param key: a string for a label widget
        :param value: a string for the text of a combobox or lineedit
        :return: a label and a widget (combobox or lineedit)
        """
        name_of_label = translate(key.split()[-1])
        label = QLabel(name_of_label)
        label.name = key + ' label'
        if isinstance(value, bool):
            widget = QComboBox()
            widget.name = key
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
                    'show_answer',
                    {'first_number': ['range', 'display']},
                    {'steps': ['operators', 'number', 'limits']}]
        for key in sequence:
            if isinstance(key, dict):
                if 'first_number' in key:
                    for value in key['first_number']:
                        first_number_key = value
                        content = rule['first_number'][value]
                        label, widget = self.add_widget('first_number ' + first_number_key, content)
                        widgets.extend([label, widget])
                if 'steps' in key:
                    for n, step in enumerate(rule['steps']):
                        step_widgets = self.setup_step_widgets(step, n)
                        widgets.extend(step_widgets)

            else:
                label, widget = self.add_widget(key, rule[key])
                widgets.extend([label, widget])

        return widgets

    @staticmethod
    def setup_combo_and_default(combobox, default):
        combobox.addItems([translate('True'), translate('False')])
        if translate(default):
            combobox.setCurrentIndex(0)
        else:
            combobox.setCurrentIndex(1)

    def setup_separator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        return sep

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
            rule_index = int(sender.parent().name.split()[1])
            rule = self.config[user]['rules'][rule_index]
            if isinstance(sender, QLineEdit):
                try:
                    value = int(sender.text())
                except ValueError:
                    try:
                        value = float(sender.text())
                    except ValueError:
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

        if self.validator(sender):
            write_cfg(self.config)
            self.onRefresh()

    def onRefresh(self):
        sender = self.sender()
        user = sender.parent().parent().parent().parent().name
        rule_index = int(sender.parent().name.split()[1])
        rule = self.config[user]['rules'][rule_index]
        quiz = quiz_gen(rule)
        for widget in sender.parent().children():
            if widget.objectName() == 'example':
                widget.setText(quiz)

    @staticmethod
    def validator(widget):
        if isinstance(widget, QLineEdit):
            text = widget.text()
            if widget.name.endswith('range'):
                if re.search(r'^\d+$', text):
                    if eval(text) == 0:
                        widget.setText('1')
                    return True
                elif re.search(r'^=\d+$', text):
                    return True
                elif re.search(r'^\d+, *\d+', text):
                    return True
                else:
                    return False
            if widget.name.endswith('ceiling') or widget.name.endswith('floor'):
                # noinspection PyComparisonWithNone
                if re.search(r'\d+', text) or text == '' or translate(text) == None:
                    return True
                else:
                    return False
            if widget.name.endswith('weight'):
                if re.search(r"^[-+]?\d*\.\d+$|^\d+$", text):
                    if 0 <= eval(text) <= 1:
                        return True
                    else:
                        return False
                else:
                    return False
            if widget.name.endswith('operators'):
                if text:
                    for c in text:
                        if c not in '+-*/':
                            return False
                    return True
                else:
                    return False
        else:
            return True

    def setup_step_widgets(self, step, n):
        widgets = []
        sequence = ['operators', 'number', 'limits']
        for key in sequence:
            if key == 'limits':
                for limit in step['limits']:
                    content = step['limits'][limit]
                    label, widget = self.add_widget(f'steps {n} limits {limit}', content)
                    widgets.extend([label, widget])
            elif key == 'number':
                for number_key in ['range', 'display']:
                    content = step['number'][number_key]
                    label, widget = self.add_widget(f'steps {n} number {number_key}', content)
                    widgets.extend([label, widget])
            else:
                content = step[key]
                label, widget = self.add_widget(f'steps {n} {key}', content)
                widgets.extend([label, widget])
        return widgets

    def on_add_step(self):
        sender = self.sender()
        user = sender.parent().parent().parent().parent().name
        rule_index = int(sender.parent().name.split()[1])
        rule = self.config[user]['rules'][rule_index]
        widgets = sender.parent().widgets

        step = add_step(rule)
        write_cfg(self.config)
        step_widgets = self.setup_step_widgets(step, len(rule['steps']))
        widgets = widgets[:-2] + step_widgets + widgets[-2:]
        sender.parent().widgets = widgets
        self.lay_rule_widgets(sender.parent().layout(), widgets)
        self.onRefresh()

    def on_rm_step(self):
        sender = self.sender()
        user = sender.parent().parent().parent().parent().name
        rule_index = int(sender.parent().name.split()[1])
        rule = self.config[user]['rules'][rule_index]
        widgets = sender.parent().widgets
        layout = sender.parent().layout()
        widgets = widgets[:-20] + widgets[-2:]
        sender.parent().widgets = widgets

        if rm_step(rule):
            write_cfg(self.config)
            for i in reversed(range(layout.count())):
                widgetToRemove = layout.itemAt(i).widget()
                # remove it from the layout list
                # layout.removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)
            self.lay_rule_widgets(layout, widgets)
            self.onRefresh()


def on_user_button(self):
    self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
