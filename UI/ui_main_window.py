import os.path
from typing import List, Union

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTextEdit
import sys
from TaskBuilder import SchemeParams
from UI.UICollapsible.ui_collapsible_box import CollapsibleBox
from UI.UIFileDialogs import UIFileDialogs
from UI.UIStyle import load_style
from UI.io_utils import collect_files_via_dir
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


class ZemaxUtilsSession:
    def __init__(self):
        self._zemax_file = ZFile()
        self._tasks_files = None

    @property
    def zmx_file(self) -> ZFile:
        return self._zemax_file

    @property
    def tasks_files(self) -> List[SchemeParams]:
        return self._tasks_files

    def load_task_file(self, src_file: Union[str, List[str]]):
        if isinstance(src_file, str):
            self._tasks_files = SchemeParams.read(src_file)
            return len(self._tasks_files) != 0
        if isinstance(src_file, List):
            self._tasks_files = SchemeParams.read_and_merge(src_file)
            return len(self._tasks_files) != 0
        raise ValueError(f"Unknown type \"{type(src_file)}\" of task files paths...")

    def load_zmx_file(self, src_file: str) -> bool:
        return self._zemax_file.load(src_file)


class UIMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('MainWindow')
        self.setGeometry(100, 100, 500, 300)
        self._build_menu_bar()
        self._central_container = QWidget()
        self._central_container.setLayout(QVBoxLayout())
        self._main_tabs = QTabWidget(self)
        self._central_container.layout().addWidget(self._main_tabs)

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
        self._session = ZemaxUtilsSession()
        self.show()

    def create_task_file_tabs(self, src_file: str = None):  # "../ZemaxSchemesSettings/combined_params.json"):
        if not src_file:
            return
        if self._tasks_files_tabs:
            self._tasks_files_tabs.deleteLater()
        self._tasks_files_tabs =  UITaskFileViewsList()  # QTabWidget()
        self._task_file_tab.layout().addWidget(self._tasks_files_tabs)
        scheme = SchemeParams.read(src_file)
        self._tasks_files_tabs.setup(scheme)

    def create_zemax_file_tabs(self, src_file: str = None):  # "../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX"):
        if self._zemax_files_tabs:
            self._zmx_file_tab.layout().removeWidget(self._zemax_files_tabs)

        self._zemax_files_tabs =  UIZemaxFileView()  # QTabWidget()
        self._zmx_file_tab.layout().addWidget(self._zemax_files_tabs)
        if not src_file:
            return
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

    def _load_tasks(self, src_file: str = "../ZemaxSchemesSettings/combined_params.json") -> bool:
        if not self._session.load_task_file(src_file):
            return False
        if self._tasks_files_tabs:
            self._tasks_files_tabs.deleteLater()
        self._tasks_files_tabs =  UITaskFileViewsList()  # QTabWidget()
        self._task_file_tab.layout().addWidget(self._tasks_files_tabs)
        self._tasks_files_tabs.setup(self._session.tasks_files)
        return True

    def _load_zmx_file(self, src_file: str = "../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX"):
        if not self._session.load_zmx_file(src_file):
            return False
        if self._zemax_files_tabs:
            self._zmx_file_tab.layout().removeWidget(self._zemax_files_tabs)
        self._zemax_files_tabs = UIZemaxFileView()  # QTabWidget()
        self._zmx_file_tab.layout().addWidget(self._zemax_files_tabs)
        self._zemax_files_tabs.setup(self._session.zmx_file)

    def _build_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        help_menu = menu_bar.addMenu('&Help')
        file_menu.addAction('Open Settings File', lambda: print('not done yet...'))
        file_menu.addAction('Open Zemax File', lambda: self._load_zmx_file(UIFileDialogs.open_file_name_dialog({'Zemax File': "zmx"})))
        file_menu.addAction('Open Task', lambda: self._load_tasks(UIFileDialogs.open_file_names_dialog({'JSON File': "json"})))
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
