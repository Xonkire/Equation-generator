import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, \
    QStackedWidget, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QClipboard
from PyQt5.QtCore import Qt
import random
import numpy as np

class EquationGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        page_select_equation_type = self.create_select_equation_type_page()
        self.stacked_widget.addWidget(page_select_equation_type)
        page_quadratic_settings = self.create_quadratic_settings_page()
        self.stacked_widget.addWidget(page_quadratic_settings)
        page_exponential_settings = self.create_exponential_settings_page()
        self.stacked_widget.addWidget(page_exponential_settings)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
                border: 2px solid #45a049;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QLabel {
                color: #333;
                font-size: 18px;
                margin-bottom: 10px;
            }
        """)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Генератор уравнений')
        self.setWindowIcon(QIcon(':/icon.png'))
        self.show()

    def create_select_equation_type_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        quadratic_button = QPushButton('Квадратные', self)
        quadratic_button.clicked.connect(self.show_quadratic_settings_page)
        layout.addWidget(quadratic_button)
        exponential_button = QPushButton('Показательные', self)
        exponential_button.clicked.connect(self.show_exponential_settings_page)
        layout.addWidget(exponential_button)
        page.setLayout(layout)
        return page

    def create_quadratic_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.form_layout_quadratic = QFormLayout()
        self.min_a_input = QLineEdit(self)
        self.max_a_input = QLineEdit(self)
        self.min_b_input = QLineEdit(self)
        self.max_b_input = QLineEdit(self)
        self.min_c_input = QLineEdit(self)
        self.max_c_input = QLineEdit(self)
        self.equation_count_input = QLineEdit(self)
        self.min_a_input.setText('-10')
        self.max_a_input.setText('10')
        self.min_b_input.setText('-10')
        self.max_b_input.setText('10')
        self.min_c_input.setText('-10')
        self.max_c_input.setText('10')
        self.form_layout_quadratic.addRow('Мин. a:', self.min_a_input)
        self.form_layout_quadratic.addRow('Макс. a:', self.max_a_input)
        self.form_layout_quadratic.addRow('Мин. b:', self.min_b_input)
        self.form_layout_quadratic.addRow('Макс. b:', self.max_b_input)
        self.form_layout_quadratic.addRow('Мин. c:', self.min_c_input)
        self.form_layout_quadratic.addRow('Макс. c:', self.max_c_input)
        self.form_layout_quadratic.addRow('Количество уравнений:', self.equation_count_input)
        self.equation_label_quadratic = QLabel(self)
        self.equation_label_quadratic.setFont(QFont("Arial", 20))
        self.equation_label_quadratic.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.equation_label_quadratic.linkActivated.connect(self.copy_to_clipboard)
        layout.addLayout(self.form_layout_quadratic)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.equation_label_quadratic)
        layout.addWidget(scroll_area)
        generate_button_quadratic = QPushButton('Генерировать уравнения', self)
        generate_button_quadratic.clicked.connect(self.generate_quadratic_equations)
        layout.addWidget(generate_button_quadratic)
        prev_button_quadratic = QPushButton('Назад', self)
        prev_button_quadratic.clicked.connect(self.prev_page)
        layout.addWidget(prev_button_quadratic)
        page.setLayout(layout)
        return page

    def create_exponential_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.form_layout_exponential = QFormLayout()
        self.equation_count_input_exponential = QLineEdit(self)
        self.form_layout_exponential.addRow('Количество уравнений:', self.equation_count_input_exponential)
        self.equation_label_exponential = QLabel(self)
        self.equation_label_exponential.setFont(QFont("Arial", 20))
        self.equation_label_exponential.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.equation_label_exponential.linkActivated.connect(self.copy_to_clipboard)
        layout.addLayout(self.form_layout_exponential)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.equation_label_exponential)
        layout.addWidget(scroll_area)
        generate_button_exponential = QPushButton('Генерировать уравнения', self)
        generate_button_exponential.clicked.connect(self.generate_exponential_equations)
        layout.addWidget(generate_button_exponential)
        prev_button_exponential = QPushButton('Назад', self)
        prev_button_exponential.clicked.connect(self.prev_page)
        layout.addWidget(prev_button_exponential)
        page.setLayout(layout)
        return page

    def show_quadratic_settings_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_exponential_settings_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def prev_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def generate_quadratic_equations(self):
        try:
            min_a = int(self.min_a_input.text())
            max_a = int(self.max_a_input.text())
            min_b = int(self.min_b_input.text())
            max_b = int(self.max_b_input.text())
            min_c = int(self.min_c_input.text())
            max_c = int(self.max_c_input.text())
            equation_count = int(self.equation_count_input.text())
            equations = []

            for i in range(1, equation_count + 1):
                a = random.randint(min_a, max_a)
                while a == 0:
                    a = random.randint(min_a, max_a)

                # Generate b and c based on the range
                b = random.randint(min_b, max_b)
                c = random.randint(min_c, max_c)

                # Adjust signs based on the generated values
                a_str = f"{a if a != -1 else '-'}x²" if a !=0 else ""
                b_str = f" {'-' if b < 0 else '+'} {abs(b)}x" if b != 0 else ""
                c_str = f" {'-' if c < 0 else '+'} {abs(c)}" if c != 0 else ""

                # Check if b or c is zero, and exclude them from the equation
                equation_str = f"{i}) {a_str}{b_str}{c_str} = 0"
                equations.append(equation_str)

            self.equation_label_quadratic.setText("<br>".join(equations))
        except ValueError:
            self.equation_label_quadratic.setText("Пожалуйста, введите корректные числовые значения.")

    def generate_exponential_equations(self):
        try:
            equation_count = int(self.equation_count_input_exponential.text())
            equations = []
            for i in range(1, equation_count + 1):
                a = random.randint(1, 5)
                b = random.randint(-5, 5)
                c = random.randint(1, 5)
                d = random.randint(-5, 5)
                e = random.randint(1, 5)
                equation_str = f"{i}) {a}<sup>({b}x + {c})</sup> = {a}<sup>({d}x + {e})</sup>"
                equations.append(equation_str)
            self.equation_label_exponential.setText("<br>".join(equations))
        except ValueError:
            self.equation_label_exponential.setText("Пожалуйста, введите корректные числовые значения.")

    def copy_to_clipboard(self, link):
        clipboard = QApplication.clipboard()
        clipboard.setText(link)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EquationGenerator()
    sys.exit(app.exec_())
