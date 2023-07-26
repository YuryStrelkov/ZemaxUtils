from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication
import sys
# https://www.pythontutorial.net/pyqt/pyqt-qmainwindow/

# TODO


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Editor')
        self.setGeometry(100, 100, 500, 300)
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        help_menu = menu_bar.addMenu('&Help')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())