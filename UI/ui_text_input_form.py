from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QSize


class UITextInputForm(QMainWindow):
    def __init__(self, callback_func, frame_title, field_tite):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(320, 140))
        self.setWindowTitle(frame_title)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText(f'{field_tite}:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(lambda v: self.parse_input_data(callback_func))
        pybutton.resize(200, 32)
        pybutton.move(80, 60)

    def parse_input_data(self, callback_func):
        callback_func(self.line.text())
        self.destroy()

