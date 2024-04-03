import json

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QPalette, QColor
import sys

from TaskBuilder import SchemeParams
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

    def create_zemax_file_tabs(self, src_file: str = "../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX"):
        if self._zemax_files_tabs:
            self._zmx_file_tab.layout().removeWidget(self._zemax_files_tabs)

        self._zemax_files_tabs =  UIZemaxFileView()  # QTabWidget()
        self._zmx_file_tab.layout().addWidget(self._zemax_files_tabs)
        scheme = ZFile()
        scheme.load(src_file)
        self._zemax_files_tabs.setup(scheme)

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


PALETTE_KEYS = {"Active": 0,
                "All": 5,
                "AlternateBase": 16,
                "Background": 10,
                "Base": 9,
                "BrightText": 7,
                "Button": 1,
                "ButtonText": 8,
                "Current": 4,
                "Dark": 4,
                "Disabled": 1,
                "Foreground": 0,
                "Highlight": 12,
                "HighlightedText": 13,
                "Inactive": 2,
                "Light": 2,
                "Link": 14,
                "LinkVisited": 15,
                "Mid": 5,
                "Midlight": 3,
                "NColorGroups": 3,
                "NColorRoles": 21,
                "Normal": 0,
                "NoRole": 17,
                "PlaceholderText": 20,
                "Shadow": 11,
                "Text": 6,
                "ToolTipBase": 18,
                "ToolTipText": 19,
                "Window": 10,
                "WindowText": 0}


def _load_palette(src: dict) -> QPalette():
        if 'Palette' not in src:
            return QPalette()
        palette = src['Palette']
        q_palette = QPalette()
        for key, val in palette.items():
            if key not in PALETTE_KEYS:
                continue
            q_palette.setColor(PALETTE_KEYS[key], QColor(*tuple(int(v) for v in val.values())))
        return q_palette


def load_style(style_src: str, application: QApplication) -> None:
    with open(style_src, 'rt') as input_file:
        json_file = json.load(input_file)
        application.setPalette(_load_palette(json_file))
        if 'WidgetsStyles' not in json_file:
            return
        widgets_styles = json_file['WidgetsFontStyles']
        style_sheet = []
        for style in widgets_styles:
            if 'selector' not in style:
                continue
            selector = style['selector']
            font_family = 'Arial'
            font_size = '10'
            font_units = 'pt'
            if 'font-family' in style:
                font_family = style['font-family']
            if 'font-size' in style:
                font_size = style['font-size']
            if 'font-units' in style:
                font_units = style['font-units']
            style_sheet.append(f"{selector}{{font-family: {font_family}; font-size: {font_size}{font_units};}}")
        application.setStyleSheet('\n'.join(v for v in style_sheet))


def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # load_style('../dark_theme_palette.json', app)
    window = UIMainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
