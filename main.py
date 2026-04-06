import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMainWindow,
    QGridLayout,
    QLabel,
    QVBoxLayout,
)
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QThread

from logic import mathematical_calculation
from constants import (
    OPERATORS,
    BUTTON_LAYOUT,
    STYLE_SHEET
)


class CalcLabel(QLabel):
    """Поле для отображения выражения и результата."""

    textChanged = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumSize(QSize(470, 100))
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def setText(self, text):
        if text != self.text():
            super().setText(text)
            self.textChanged.emit(text)


class CalcButton(QPushButton):
    """Кнопка калькулятора."""

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(text)
        self.setMinimumSize(QSize(100, 75))


class CalculationThread(QThread):
    """Поток для выполнения вычислений без блокировки UI."""

    def __init__(self, label):
        super().__init__()

        self.label = label
        self.expression = label.text()

    def run(self):
        answer = mathematical_calculation(self.expression)
        self.label.setText(answer)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.opening_parenthesis = 0
        self.setWindowTitle("Калькулятор")
        self.setMinimumSize(QSize(485, 550))

        self.label = CalcLabel("0", objectName="Label")

        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)

        for i, row in enumerate(BUTTON_LAYOUT):
            for j, text in enumerate(row):
                button = CalcButton(text=text, objectName="Button")
                button.released.connect(lambda t=text: self._handle_input(t))
                grid_layout.addWidget(button, i, j)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        v_layout = QVBoxLayout()
        v_layout.setSpacing(5)
        v_layout.addWidget(self.label)
        v_layout.addWidget(grid_widget)

        main_widget = QWidget()
        main_widget.setLayout(v_layout)
        self.setCentralWidget(main_widget)
        self.setFocus()


    def _last_char(self) -> str:
        """Возвращает последний символ выражения."""

        return self.label.text()[-1:] if self.label.text() else ""

    def _ends_with_operator(self) -> bool:
        """Проверяет, заканчивается ли выражение оператором или '='."""

        return self._last_char() in OPERATORS or self._last_char() == "="

    def _ends_with_open_paren(self) -> bool:
        """Проверяет, заканчивается ли выражение открывающей скобкой."""

        return self._last_char() == "("

    def _can_append_operator(self) -> bool:
        """Проверяет, можно ли добавить оператор в текущую позицию."""

        return not self._ends_with_operator() and not self._ends_with_open_paren()

    def _append(self, char: str) -> None:
        """Добавляет символ к текущему выражению."""

        self.label.setText(self.label.text() + char)

    def _handle_clear(self) -> None:
        """Очищает выражение."""

        self.label.setText("0")
        self.opening_parenthesis = 0

    def _handle_backspace(self) -> None:
        """Удаляет последний символ или ^2."""

        text = self.label.text()

        if self._last_char() == "(":
            self.opening_parenthesis -= 1

        elif self._last_char() == ")":
            self.opening_parenthesis += 1

        if len(text) > 1 and not text.endswith("^2"):
            self.label.setText(text[:-1])

        elif text.endswith("^2"):
            self.label.setText(text[1:-3])

        else:
            self.label.setText("0")

    def _handle_digit(self, digit: str) -> None:
        """Обрабатывает ввод цифры."""

        if self.label.text() == "0":
            self.label.setText(digit)

        elif self._last_char() != ")" and not self.label.text().endswith("^2"):
            self._append(digit)

    def _handle_operator(self, op: str) -> None:
        """Обрабатывает ввод оператора (+, -, *, /)."""

        if self._can_append_operator():
            self._append(op)

    def _handle_open_paren(self) -> None:
        """Обрабатывает ввод открывающей скобки."""

        if self._ends_with_open_paren() or self._last_char() in OPERATORS:
            self.opening_parenthesis += 1
            self._append("(")

        elif len(self.label.text()) == 1:
            self.opening_parenthesis += 1
            self.label.setText("(" + self.label.text())

    def _handle_close_paren(self) -> None:
        """Обрабатывает ввод закрывающей скобки."""

        if self.opening_parenthesis > 0 and (
            self._last_char().isdigit() or self._last_char() == ")"
        ):
            self.opening_parenthesis -= 1
            self._append(")")

    def _handle_square(self) -> None:
        """Обрабатывает возведение в квадрат."""

        if self.label.text().endswith("^2"):
            self.label.setText("(" + self.label.text() + ")^2")

        elif self._can_append_operator():
            self._append("^2")

    def _handle_equals(self) -> None:
        """Запускает вычисление выражения."""

        if self._last_char().isdigit() or self._last_char() == ")":
            if self.opening_parenthesis != 0:
                self._append(")" * self.opening_parenthesis)
                self.opening_parenthesis = 0

            self._calc_thread = CalculationThread(self.label)
            self._calc_thread.start()

    def _handle_input(self, text: str) -> None:
        """Единая точка входа для обработки любого ввода."""
        
        if text == "C":
            self._handle_clear()

        elif text == "⌫":
            self._handle_backspace()

        elif text.isdigit():
            self._handle_digit(text)

        elif text in OPERATORS:
            self._handle_operator(text)

        elif text == "(":
            self._handle_open_paren()

        elif text == ")":
            self._handle_close_paren()

        elif text == "x^2":
            self._handle_square()

        elif text == "=":
            self._handle_equals()

    def keyPressEvent(self, event):
        key = event.key()
        char = event.text()

        key_mapping = {
            Qt.Key.Key_Backspace: "⌫",
            Qt.Key.Key_Delete: "C",
            Qt.Key.Key_Enter: "=",
            Qt.Key.Key_Return: "=",
        }

        if key in key_mapping:
            self._handle_input(key_mapping[key])
            
        elif char in "0123456789/*-+()":
            self._handle_input(char)


def main():
    sys.set_int_max_str_digits(10**9)
    app = QApplication([])
    app.setStyleSheet(STYLE_SHEET)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()