from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel, QLineEdit, QPushButton, QWidget, \
    QVBoxLayout, QTabWidget, QScrollArea, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
import sys

from TaskBuilder import SchemeParams, SurfaceParams
from UI.ui_table import UITableWidget
from collapsible import CollapsibleBox


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


class UITaskFileTab(QWidget):
    def __init__(self, parent=None):
        super(UITaskFileTab, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        scroll = QScrollArea()
        content = QWidget()
        content.setLayout(QVBoxLayout())
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        content.layout().setAlignment(Qt.AlignTop)
        self._scheme_common_info = CollapsibleBox(title="SCHEME COMMON")
        self._scheme_fields      = CollapsibleBox(title="SCHEME FIELDS")
        self._scheme_waves       = CollapsibleBox(title="SCHEME WAVES")
        self._scheme_surfaces    = CollapsibleBox(title="SCHEME SURFACES")
        self._scheme_extra_data  = CollapsibleBox(title="SCHEME EXTRA DATA")
        content.layout().addWidget(self._scheme_common_info)
        content.layout().addWidget(self._scheme_fields)
        content.layout().addWidget(self._scheme_waves)
        content.layout().addWidget(self._scheme_surfaces)
        content.layout().addWidget(self._scheme_extra_data)
        content.layout().addStretch()
        self.layout().addWidget(scroll)

    def set_scheme_waves(self, scheme: SchemeParams) -> 'UITaskFileTab':
        if not scheme.waves:
            info_layout = QVBoxLayout()
            info_label = QLabel()
            info_label.setText("No wave lengths data...")
            info_layout.addWidget(info_label)
            self._scheme_waves.set_content_layout(info_layout)
            return self
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.waves))
        self._scheme_waves.set_content_layout(layout)
        return self

    def set_scheme_fields(self, scheme: SchemeParams) -> 'UITaskFileTab':
        if not scheme.fields:
            info_layout = QVBoxLayout()
            info_label = QLabel()
            info_label.setText("No fields data...")
            info_layout.addWidget(info_label)
            self._scheme_fields.set_content_layout(info_layout)
            return self
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.fields.fields))
        self._scheme_fields.set_content_layout(layout)
        return self

    def set_scheme_surfaces(self, scheme: SchemeParams) -> 'UITaskFileTab':
        if not scheme.surf_params:
            info_layout = QVBoxLayout()
            info_label = QLabel()
            info_label.setText("No surfaces data...")
            info_layout.addWidget(info_label)
            self._scheme_surfaces.set_content_layout(info_layout)
            return self
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.surf_params))
        self._scheme_surfaces.set_content_layout(layout)
        return self

    def set_scheme_extra_data(self, scheme: SchemeParams) -> 'UITaskFileTab':
        if not scheme.surf_params:
            info_layout = QVBoxLayout()
            info_label = QLabel()
            info_label.setText("No extra data...")
            info_layout.addWidget(info_label)
            self._scheme_extra_data.set_content_layout(info_layout)
            return self
        params: List[SurfaceParams] = scheme.surf_params
        params_t = []
        for i, p in enumerate(params):
            params_t.append([('surf_n', i)])
            params_t[-1].extend((f"Zernike {i}", z) for i, z in enumerate(p.zernike))
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(params_t))
        self._scheme_extra_data.set_content_layout(layout)
        return self

    def set_scheme_common_info(self, scheme: SchemeParams) -> 'UITaskFileTab':
        layout = QVBoxLayout()
        info1 = QLabel()
        info2 = QLabel()
        info1.setText(scheme.description_short)
        info2.setText(scheme.description_long)
        layout.addWidget(info1)
        layout.addWidget(info2)
        self._scheme_common_info.set_content_layout(layout)
        return self


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
        scheme_tab.set_scheme_fields(content)
        scheme_tab.set_scheme_waves(content)
        scheme_tab.set_scheme_surfaces(content)
        scheme_tab.set_scheme_extra_data(content)
        scheme_tab.set_scheme_common_info(content)
        tab.layout().addWidget(scheme_tab)  # QLabel("TAB"))
        return tab

    def cretae_zemax_file_tab(self, content: SchemeParams):
        """Create the General page UI."""
        tab    = QWidget()
        tab.setLayout(QVBoxLayout())
        scheme_tab = UITaskFileTab()
        scheme_tab.set_scheme_fields(content)
        scheme_tab.set_scheme_waves(content)
        scheme_tab.set_scheme_surfaces(content)
        scheme_tab.set_scheme_extra_data(content)
        scheme_tab.set_scheme_common_info(content)
        tab.layout().addWidget(scheme_tab)  # QLabel("TAB"))
        return tab

    def create_task_file_tabs(self, src_file: str = "../ZemaxScemesSettings/polychrome.json"):
        if self._tasks_files_tabs:
            self._task_file_tab.layout().removeWidget(self._tasks_files_tabs)

        self._tasks_files_tabs = QTabWidget()
        self._task_file_tab.layout().addWidget(self._tasks_files_tabs)

        file_name = src_file.split('/')[-1].split('.')[0]
        scheme = SchemeParams.read(src_file)
        [self._tasks_files_tabs.addTab(self.cretae_task_file_tab(t),
                                       f"{file_name} : scheme{i:3}") for i, t in enumerate(scheme)]

    def create_zemax_file_tabs(self, src_file: str = "../ZemaxScemesSettings/polychrome.json"):
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
    window = UIMainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
