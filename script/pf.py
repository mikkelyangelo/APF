import sys
from main_field import mainn
from PyQt5 import QtWidgets
import design

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.press.clicked.connect(self.run_script)


    def run_script(self):
       # Получите значение параметра из элемента управления
       #  parameter_value = parameter_input.text()
        k = self.line_k_res.text()
        a = self.line_a_att.text()
        mainn(k, a)
    # Запустите ваш существующий скрипт Python с параметром
    # Например, используйте subprocess или exec для выполнения кода

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = ExampleApp()


    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
