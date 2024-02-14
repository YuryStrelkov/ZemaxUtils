
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget, \
    QVBoxLayout, QTabWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from typing import Union
import sys

from TaskBuilder import SchemeParams
from UI import ImageWidget
from UI.ui_table import UITableWidget


class TextInputForm(QMainWindow):
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


class UIMainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MainWindow')
        self.setWindowIcon(QIcon('./assets/editor.png'))
        self.setGeometry(100, 100, 500, 300)
        self._build_menu_bar()
        self._tabs = self.create_tabs()  # ImageWidget(parent=self)
        self.setCentralWidget(self._tabs)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Status :: no-status')
        self.show()

    def cretae_tab(self, content):
        """Create the General page UI."""
        tab    = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table(tab, content))  # QLabel("TAB"))
        tab.setLayout(layout)
        return tab

    def create_tabs(self):
        container = QTabWidget(self)  # контейнер с вертикальным размещением
        scheme = SchemeParams.read("../ZemaxScemesSettings/scheme_08_02_2024.json")
        tables = [params.surf_params for params in scheme]
        [container.addTab(self.cretae_tab(t), f"tab:{i:3}" ) for i, t in enumerate(tables)]
        return container

    def _build_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        mode_menu = menu_bar.addMenu('&Modes')
        settings_menu = menu_bar.addMenu('&Settings')
        help_menu = menu_bar.addMenu('&Help')
        file_menu.addAction('Connect', lambda: print('not done yet...'))
        file_menu.addAction('Connect to port', lambda: print('not done yet...'))
        file_menu.addAction('Disconnect', lambda: print('not done yet...'))
        file_menu.addAction('Exit', lambda: self._exit_app())

        mode_menu.addAction(f'SaveFrame(f)', lambda: print('not done yet...'))
        mode_menu.addAction('RecordFrames(s)', lambda: print('not done yet...'))
        mode_menu.addAction('RecordVideo(r)', lambda: print('not done yet...'))
        mode_menu.addAction('Stop(x)', lambda: print('not done yet...'))

        settings_menu.addAction(f'Load camera settings', lambda: print('not done yet...'))
        settings_menu.addAction(f'Save camera settings', lambda: print('not done yet...'))
        settings_menu.addAction(f'Load calibration settings', lambda: print('not done yet...'))
        settings_menu.addAction(f'Save calibration settings', lambda: print('not done yet...'))

    def _exit_app(self):
        self.close()


def run():
    app = QApplication(sys.argv)
    window = UIMainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
