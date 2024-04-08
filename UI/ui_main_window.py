import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QWidget, QVBoxLayout, QTabWidget, QTextEdit
from PyQt5.QtGui import QIcon, QPalette, QColor
import sys

from TaskBuilder import SchemeParams
from UI.UICollapsible.ui_collapsible_box import CollapsibleBox
from UI.UIStyle import load_style
from UI.ui_task_file_view import UITaskFileView, UITaskFileViewsList
from UI.ui_zemax_file_view import UIZemaxFileView
from ZFile import ZFile


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
        self._central_container = QWidget()
        self._central_container.setLayout(QVBoxLayout())
        self._main_tabs = QTabWidget(self)
        self._central_container.layout().addWidget(self._main_tabs)

        # self._logging_area = QScrollArea()
        # self._logging_area.setWidgetResizable(True)
        # self._logging_area.setMaximumHeight(200)
        layout = QVBoxLayout()
        self._logging_collapsible_area = CollapsibleBox(title="LOGGING INFO")
        self._logging_area = QTextEdit()
        self._logging_area.setReadOnly(True)
        self._logging_area.setLineWrapMode(QTextEdit.NoWrap)
        self._logging_area.setMaximumHeight(200)
        font = self._logging_area.font()
        font.setFamily("Consolas")
        font.setPointSize(12)
        self._logging_area.setFont(font)
        layout.addWidget(self._logging_area)
        self._logging_collapsible_area.set_content_layout(layout)
        self._central_container.layout().addWidget(self._logging_collapsible_area)

        self.setCentralWidget(self._central_container)
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

    def create_zemax_file_tabs(self, src_file: str = "../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX"):
        if self._zemax_files_tabs:
            self._zmx_file_tab.layout().removeWidget(self._zemax_files_tabs)

        self._zemax_files_tabs =  UIZemaxFileView()  # QTabWidget()
        self._zmx_file_tab.layout().addWidget(self._zemax_files_tabs)
        scheme = ZFile()
        if scheme.load(src_file):
            self._logging_area.append(f"Successfully load zemax file at path: {src_file}\n")
            self._zemax_files_tabs.setup(scheme)
            # for message in io_log_2d():
            #     self._logging_area.append(f"{message}\n")
#
            # for message in trace_log_2d():
            #     self._logging_area.append(f"{message}\n")
#
            # for message in draw_log_2d():
            #     self._logging_area.append(f"{message}\n")

        else:
            self._logging_area.append(f"Failed to load zemax file at path: {src_file}\n")

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
    load_style('../dark_theme_palette.json', app)
    window = UIMainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
