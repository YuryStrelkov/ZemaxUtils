from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
import sys

from TaskBuilder import SchemeParams
from UI.ui_task_file_view import UITaskFileView, UITaskFileViewsList


class UITaskFileTab(QWidget):
    def __init__(self, parent=None):
        super(UITaskFileTab, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self._task_file_ui = UITaskFileView()
        self.layout().addWidget(self._task_file_ui)

    def setup(self, content: SchemeParams) -> None:
        self._task_file_ui.setup(content)


class UIMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MainWindow')
        self.setWindowIcon(QIcon('./assets/editor.png'))
        self.setGeometry(100, 100, 500, 300)
        self._build_menu_bar()
        self._main_tabs = QTabWidget(self)
        self.setCentralWidget(self._main_tabs)
        self._zmx_file_tab = QWidget()
        self._zmx_file_tab.setLayout(QVBoxLayout())
        self._task_file_tab = QWidget()
        self._task_file_tab.setLayout(QVBoxLayout())
        self._main_tabs.addTab(self._task_file_tab, 'Task file info')
        self._main_tabs.addTab(self._zmx_file_tab, 'Zemax file info')
        self._zemax_files_tabs = None
        self._tasks_files_tabs = None
        self.create_task_file_tabs()
        self.create_zemax_file_tabs()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Status :: no-status')
        self.show()

    def cretae_task_file_tab(self, content: SchemeParams):
        """Create the General page UI."""
        tab    = QWidget()
        tab.setLayout(QVBoxLayout())
        scheme_tab = UITaskFileTab()
        scheme_tab.setup(content)
        tab.layout().addWidget(scheme_tab)  # QLabel("TAB"))
        return tab

    def cretae_zemax_file_tab(self, content: SchemeParams):
        """Create the General page UI."""
        tab    = QWidget()
        tab.setLayout(QVBoxLayout())
        scheme_tab = UITaskFileTab()
        scheme_tab.setup(content)
        tab.layout().addWidget(scheme_tab)  # QLabel("TAB"))
        return tab

    def create_task_file_tabs(self, src_file: str = "../ZemaxSchemesSettings/combined_params.json"):
        if self._tasks_files_tabs:
            self._tasks_files_tabs.deleteLater()
        self._tasks_files_tabs =  UITaskFileViewsList()  # QTabWidget()
        self._task_file_tab.layout().addWidget(self._tasks_files_tabs)
        scheme = SchemeParams.read(src_file)
        self._tasks_files_tabs.setup(scheme)

    def create_zemax_file_tabs(self, src_file: str = "../ZemaxSchemesSettings/polychrome.json"):
        if self._zemax_files_tabs:
            self._zmx_file_tab.layout().removeWidget(self._zemax_files_tabs)

        self._zemax_files_tabs = QTabWidget()
        self._zmx_file_tab.layout().addWidget(self._zemax_files_tabs)

        file_name = src_file.split('/')[-1].split('.')[0]
        scheme = SchemeParams.read(src_file)
        [self._zemax_files_tabs.addTab(self.cretae_task_file_tab(t),
                                       f"{file_name} : scheme{i:3}") for i, t in enumerate(scheme)]

    def _build_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        help_menu = menu_bar.addMenu('&Help')
        file_menu.addAction('Open Settings File', lambda: print('not done yet...'))
        file_menu.addAction('Open Zemax File', lambda: print('not done yet...'))
        file_menu.addAction('Open Task', lambda: print('not done yet...'))
        file_menu.addAction('Save Task', lambda: print('not done yet...'))
        file_menu.addAction('Run Task', lambda: print('not done yet...'))
        file_menu.addAction('Exit', lambda: self._exit_app())

        # mode_menu.addAction(f'SaveFrame(f)', lambda: print('not done yet...'))
        # mode_menu.addAction('RecordFrames(s)', lambda: print('not done yet...'))
        # mode_menu.addAction('RecordVideo(r)', lambda: print('not done yet...'))
        # mode_menu.addAction('Stop(x)', lambda: print('not done yet...'))

        # settings_menu.addAction(f'Load camera settings', lambda: print('not done yet...'))
        # settings_menu.addAction(f'Save camera settings', lambda: print('not done yet...'))
        # settings_menu.addAction(f'Load calibration settings', lambda: print('not done yet...'))
        # settings_menu.addAction(f'Save calibration settings', lambda: print('not done yet...'))

    def _exit_app(self):
        self.close()


def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font_size = 11
    font_name = "Consolas"
    app.setStyleSheet(f'.QLabel      {{ font-family: {font_name};\nfont-size: {font_size}pt;}}\n'
                      f'.QTabWidget  {{ font-family: {font_name};\nfont-size: {font_size}pt;}}\n'
                      f'.QToolButton {{ font-family: {font_name};\nfont-size: {font_size}pt;}}\n'
                      f'.QPushButton {{ font-family: {font_name};\nfont-size: {font_size - 1}pt;}}\n'
                      f'.QHeaderView {{ font-family: {font_name};\nfont-size: {font_size}pt;}}\n'
                      f'.QTableWidgetItem {{ font-size: {font_size}pt;}}')
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    window = UIMainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
