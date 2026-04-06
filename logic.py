from exceptions import CalculatorError


class Parser:
    """
    Парсер математических выражений на основе рекурсивного спуска.
    """

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def parse(self) -> float:
        result = self._expression()

        if self.pos < len(self.text):
            raise CalculatorError(f"Неожиданный символ: '{self.text[self.pos]}'")
        
        return result

    def _current_char(self) -> str | None:
        if self.pos < len(self.text):
            return self.text[self.pos]
        
        return None

    def _advance(self) -> None:
        self.pos += 1

    def _expression(self) -> float:
        """Обрабатывает сложение и вычитание."""

        result = self._term()

        while self._current_char() in ('+', '-'):
            op = self._current_char()
            self._advance()
            right = self._term()

            if op == '+':
                result += right

            else:
                result -= right

        return result

    def _term(self) -> float:
        """Обрабатывает умножение и деление."""

        result = self._factor()

        while self._current_char() in ('*', '/'):
            op = self._current_char()
            self._advance()
            right = self._factor()

            if op == '*':
                result *= right

            else:
                if right == 0:
                    raise CalculatorError("Деление на ноль")
                
                result /= right

        return result

    def _factor(self) -> float:
        """Обрабатывает возведение в квадрат (^2)."""

        result = self._base()

        while (self.pos + 1 < len(self.text)
               and self.text[self.pos:self.pos + 2] == '^2'):
            self.pos += 2
            result = result ** 2

        return result

    def _base(self) -> float:
        """Обрабатывает числа и выражения в скобках."""

        char = self._current_char()

        if char == '(':
            self._advance()
            result = self._expression()

            if self._current_char() != ')':
                raise CalculatorError("Ожидалась закрывающая скобка")
            
            self._advance()

            return result

        return self._number()

    def _number(self) -> float:
        """Считывает число (целое или дробное)."""

        start = self.pos

        if self._current_char() == '-':
            self._advance()

        if self._current_char() is None or not self._current_char().isdigit():
            raise CalculatorError(f"Ожидалось число на позиции {self.pos}")

        while self._current_char() is not None and self._current_char().isdigit():
            self._advance()

        if self._current_char() == '.':
            self._advance()

            if self._current_char() is None or not self._current_char().isdigit():
                raise CalculatorError("Ожидалась цифра после точки")
            
            while self._current_char() is not None and self._current_char().isdigit():
                self._advance()

        return float(self.text[start:self.pos])


def mathematical_calculation(example: str) -> str:
    """
    Вычисляет математическое выражение и возвращает результат в виде строки.

    Args:
        example: строка с математическим выражением.

    Returns:
        Результат вычисления в виде строки.
    """

    try:
        parser = Parser(example)
        result = parser.parse()

        if result == int(result):
            return str(int(result))
        
        return str(round(result, 10))

    except CalculatorError as e:
        return f"Ошибка: {e}"
    
    except Exception:
        return "Ошибка"