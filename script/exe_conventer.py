import sys

from main_field import mipf
from PyQt5 import QtWidgets
import design


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.press.clicked.connect(self.run_script)

        self.press.setDisabled(True)

        self.default_k = self.line_k_res.text()
        self.default_a = self.line_a_att.text()
        self.default_line = self.lineEdit.text()

        self.progressBar.hide()

        self.line_a_att.installEventFilter(self)
        self.line_k_res.installEventFilter(self)
        self.lineEdit.installEventFilter(self)

        self.autoParam.installEventFilter(self)
        self.autoParam.stateChanged.connect(self.hide)
        self.autoParam.stateChanged.connect(self.press_ability)

        self.coordCheck.installEventFilter(self)
        self.coordCheck.stateChanged.connect(self.hide_2)
        self.coordCheck.stateChanged.connect(self.press_ability)

    def press_ability(self):
        if self.coordCheck.isChecked():
            if self.autoParam.isChecked():
                self.press.setDisabled(False)
            elif self.line_a_att.text() != self.default_a and self.line_k_res != self.default_k:
                self.press.setDisabled(False)
        elif self.autoParam.isChecked():
            if self.coordCheck.isChecked():
                self.press.setDisabled(False)
            elif self.lineEdit.text() != self.default_line:
                self.press.setDisabled()
        else:
            self.press.setDisabled(True)

    def hide(self):
        if self.autoParam.isChecked():
            self.line_k_res.hide()
            self.line_a_att.hide()
        else:
            self.line_k_res.show()
            self.line_a_att.show()

    def hide_2(self):
        if self.coordCheck.isChecked():
            self.lineEdit.hide()
        else:
            self.lineEdit.show()

    def eventFilter(self, obj, event):
        if obj == self.line_k_res:
            if event.type() == event.Enter:
                if self.line_k_res.text() == self.default_k:
                    self.line_k_res.clear()
            elif event.type() == event.Leave:
                if self.line_k_res.text() == "":
                    self.line_k_res.setText(self.default_k)
        elif obj == self.line_a_att:
            if event.type() == event.Enter:
                if self.line_a_att.text() == self.default_a:
                    self.line_a_att.clear()
            elif event.type() == event.Leave:
                if self.line_a_att.text() == "":
                    self.line_a_att.setText(self.default_a)
        elif obj == self.lineEdit:
            if event.type() == event.Enter:
                if self.lineEdit.text() == self.default_line:
                    self.lineEdit.clear()
            elif event.type() == event.Leave:
                if self.lineEdit.text() == "":
                    self.lineEdit.setText(self.default_line)
        return super().eventFilter(obj, event)

    def focusInEvent(self, event):
        if self.line_k_res.text() == self.line_k_res.text():
            self.line_k_res.clear()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if self.line_k_res.text() == "":
            self.line_k_res.setText(self.line_k_res.text())
        super().focusOutEvent(event)

    def run_script(self):
        if self.autoParam.isChecked():
            a = 50000
            k = 15
        else:
            a = self.line_a_att.text()
            k = self.line_k_res.text()
        mipf(k, a)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = ExampleApp()

    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
