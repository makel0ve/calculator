import sys

from logic import mathematical_calculation

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, \
                            QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QThread


class Widget(QWidget):
    def __init__(self):
        super().__init__()


class VBoxLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        
        self.setSpacing(5)


class Label(QLabel):
    textChanged = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setMinimumSize(QSize(470, 100))
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def setText(self, text):
        if text != self.text():
            super().setText(text)
            self._text = text
            self.textChanged.emit(text)


class GridLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        
        self.setSpacing(5)


class PushButton(QPushButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(text)
        self.setMinimumSize(QSize(100, 75))


class NewThread(QThread):
    def __init__(self, example):
        super().__init__()
        
        self.example = example
        self.example_text = example.text()
        
    
    def run(self):
        answer = mathematical_calculation(self.example_text)
        self.example.setText(answer)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.opening_parenthesis = 0
        
        self.setWindowTitle("Калькулятор")
        self.setMinimumSize(QSize(485, 550))
        self.main_button = [["C", "⌫", "*", "="],
                            ["7", "8", "9", "/"],
                            ["4", "5", "6", "+"],
                            ["1", "2", "3", "-"],
                            ["(", "0", ")", "x^2"]]
        self.main_button_dict = {}
        
        self.grid_layout = GridLayout()
        for i in range(5):
            for j in range(4):
                self.button = PushButton(text=self.main_button[i][j], objectName="Button")
                self.button.released.connect(lambda x=self.main_button[i][j]: self.button_click(x))
                self.main_button_dict[self.main_button[i][j]] = self.button
                self.grid_layout.addWidget(self.button, i, j)
        
        self.label = Label("0", objectName="Label")
        self.widget_grid = Widget()
        self.widget_grid.setLayout(self.grid_layout)
        self.v_box_layout = VBoxLayout()
        self.v_box_layout.addWidget(self.label)
        self.v_box_layout.addWidget(self.widget_grid)
        self.main_widget = Widget()
        self.main_widget.setLayout(self.v_box_layout)
        self.setCentralWidget(self.main_widget)
        self.setFocus()

    
    def keyPressEvent(self, event):
        key = event.key()
        char = event.text()
        allowed_characters = "0123456789/*-+^()"
        
        if key == Qt.Key.Key_Backspace:
            if self.label.text()[-1:] == "(":
                self.opening_parenthesis -= 1
            if self.label.text()[-1:] == ")":
                self.opening_parenthesis += 1
            if len(self.label.text()) > 1 and self.label.text()[-2:] != "^2":
                self.label.setText(self.label.text()[0:-1])
            elif self.label.text()[-2:] == "^2":
                self.label.setText(self.label.text()[1:-3])
            else:
                self.label.setText("0")
                
        elif key == Qt.Key.Key_Delete:
            self.label.setText("0")
            self.opening_parenthesis = 0
        
        elif char in allowed_characters:
            if self.label.text() == '0' and char.isdigit():
                self.label.setText(char)
                            
            elif char == '(':
                if (self.label.text()[-1:] == "(" or
                    self.label.text()[-1:] == "/" or
                    self.label.text()[-1:] == "*" or
                    self.label.text()[-1:] == "+" or
                    self.label.text()[-1:] == "-"):
                    self.opening_parenthesis += 1
                    self.label.setText(self.label.text()+'(')
                    
                elif len(self.label.text()) == 1:
                    self.opening_parenthesis += 1
                    self.label.setText('('+self.label.text())
                
                
            elif char == ')':
                if (self.opening_parenthesis > 0 and
                    (self.label.text()[-1:].isdigit() or
                    self.label.text()[-1:] == ")")):
                    self.opening_parenthesis -= 1
                    self.label.setText(self.label.text()+')')
            
            elif char == "*":
                if (self.label.text()[-1:] != "(" and
                    self.label.text()[-1:] != "*" and
                    self.label.text()[-1:] != "=" and
                    self.label.text()[-1:] != "/" and
                    self.label.text()[-1:] != "+" and
                    self.label.text()[-1:] != "-"):
                    self.label.setText(self.label.text()+'*')
                    
            elif char == "/":
                if (self.label.text()[-1:] != "(" and
                    self.label.text()[-1:] != "*" and
                    self.label.text()[-1:] != "=" and
                    self.label.text()[-1:] != "/" and
                    self.label.text()[-1:] != "+" and
                    self.label.text()[-1:] != "-"):
                    self.label.setText(self.label.text()+'/')
            
            elif char == "-":
                if (self.label.text()[-1:] != "(" and
                    self.label.text()[-1:] != "*" and
                    self.label.text()[-1:] != "=" and
                    self.label.text()[-1:] != "/" and
                    self.label.text()[-1:] != "+" and
                    self.label.text()[-1:] != "-"):
                    self.label.setText(self.label.text()+'-')
            
            elif char == "+":
                if (self.label.text()[-1:] != "(" and
                    self.label.text()[-1:] != "*" and
                    self.label.text()[-1:] != "=" and
                    self.label.text()[-1:] != "/" and
                    self.label.text()[-1:] != "+" and
                    self.label.text()[-1:] != "-"):
                    self.label.setText(self.label.text()+'+')
                    
            elif (self.label.text()[-1:] != ")" and
                self.label.text()[-2:] != "^2"):
                self.label.setText(self.label.text()+char)
        
        elif ((key == Qt.Key.Key_Enter or
               key == Qt.Key.Key_Return) 
              and 
              (self.label.text()[-1] == ")" or 
               self.label.text()[-1].isdigit())):
            if self.opening_parenthesis != 0:
                self.label.setText(self.label.text()+')'*self.opening_parenthesis)
                self.opening_parenthesis = 0
            self.NewThread_instance = NewThread(self.label)
            self.NewThread_instance.start()

        else:
            self.label.setText(self.label.text())
        
        
    def button_click(self, text):
        if text == "C":
            self.label.setText("0")
            self.opening_parenthesis = 0
            
        elif text == "⌫":
            if self.label.text()[-1:] == "(":
                self.opening_parenthesis -= 1
            if self.label.text()[-1:] == ")":
                self.opening_parenthesis += 1
            if len(self.label.text()) > 1 and self.label.text()[-2:] != "^2":
                self.label.setText(self.label.text()[0:-1])
            elif self.label.text()[-2:] == "^2":
                self.label.setText(self.label.text()[1:-3])
            else:
                self.label.setText("0")
                
        elif self.label.text() == '0' and text.isdigit():
            self.label.setText(text)
            
        elif text == 'x^2':
            if (self.label.text()[-2:] == "^2"):
                self.label.setText('('+self.label.text()+')^2')
                
            elif (self.label.text()[-1:] != "(" and
                self.label.text()[-1:] != "*" and
                self.label.text()[-1:] != "=" and
                self.label.text()[-1:] != "/" and
                self.label.text()[-1:] != "+" and
                self.label.text()[-1:] != "-"):
                self.label.setText(self.label.text()+'^2')
            
        elif text == '(':
            if (self.label.text()[-1:] == "(" or
                  self.label.text()[-1:] == "/" or
                  self.label.text()[-1:] == "*" or
                  self.label.text()[-1:] == "+" or
                  self.label.text()[-1:] == "-"):
                self.opening_parenthesis += 1
                self.label.setText(self.label.text()+'(')
                
            elif len(self.label.text()) == 1:
                self.opening_parenthesis += 1
                self.label.setText('('+self.label.text())
            
            
        elif text == ')':
            if (self.opening_parenthesis > 0 and
                (self.label.text()[-1:].isdigit() or
                self.label.text()[-1:] == ")")):
                self.opening_parenthesis -= 1
                self.label.setText(self.label.text()+')')
        
        elif text == "*":
            if (self.label.text()[-1:] != "(" and
                self.label.text()[-1:] != "*" and
                self.label.text()[-1:] != "=" and
                self.label.text()[-1:] != "/" and
                self.label.text()[-1:] != "+" and
                self.label.text()[-1:] != "-"):
                self.label.setText(self.label.text()+'*')
                
        elif text == "/":
            if (self.label.text()[-1:] != "(" and
                self.label.text()[-1:] != "*" and
                self.label.text()[-1:] != "=" and
                self.label.text()[-1:] != "/" and
                self.label.text()[-1:] != "+" and
                self.label.text()[-1:] != "-"):
                self.label.setText(self.label.text()+'/')
        
        elif text == "-":
            if (self.label.text()[-1:] != "(" and
                self.label.text()[-1:] != "*" and
                self.label.text()[-1:] != "=" and
                self.label.text()[-1:] != "/" and
                self.label.text()[-1:] != "+" and
                self.label.text()[-1:] != "-"):
                self.label.setText(self.label.text()+'-')
        
        elif text == "+":
            if (self.label.text()[-1:] != "(" and
                self.label.text()[-1:] != "*" and
                self.label.text()[-1:] != "=" and
                self.label.text()[-1:] != "/" and
                self.label.text()[-1:] != "+" and
                self.label.text()[-1:] != "-"):
                self.label.setText(self.label.text()+'+')
                
        elif text.isdigit():
            if (self.label.text()[-1:] != ")" and
                self.label.text()[-2:] != "^2"):
                self.label.setText(self.label.text()+text)
            
        elif (text == "=" and
              (self.label.text()[-1] == ")" or
               self.label.text()[-1].isdigit())):
            if self.opening_parenthesis != 0:
                self.label.setText(self.label.text()+')'*self.opening_parenthesis)
                self.opening_parenthesis = 0
            self.NewThread_instance = NewThread(self.label)
            self.NewThread_instance.start()
                

def style_sheet():
    StyleSheet = '''
        #Button {
            font: 16px;
        }
        #Label {
            font: 20px;
        }
    '''

    return StyleSheet


def main():
    sys.set_int_max_str_digits(10**9)
    app = QApplication([])
    StyleSheet = style_sheet()
    app.setStyleSheet(StyleSheet)
    window = MainWindow()
    window.show()
    app.exec()
    
    
if __name__ == "__main__":
    main()
    