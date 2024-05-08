from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTextEdit
from UI import UITaskFileView, UITaskFileViewsList
from TaskBuilder import SchemeParams, TaskBuilder
from DocxBuilder.report import Report
from ResultBuilder import ResultFile
from UI import UIZemaxFileView
from UI import CollapsibleBox
from UI import UIFileDialogs
from UI import load_style
from ZFile import ZFile
import os.path
import sys


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
        self._session = TaskBuilder()
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

    def _load_tasks(self, src_file: str = "../ZemaxSchemesSettings/combined_params.json") -> None:
        self._session.task_file_src = src_file
        if not self._session.has_tasks:
            return
        if self._tasks_files_tabs:
            self._tasks_files_tabs.deleteLater()
        self._tasks_files_tabs =  UITaskFileViewsList()  # QTabWidget()
        self._task_file_tab.layout().addWidget(self._tasks_files_tabs)
        self._tasks_files_tabs.setup([i for i in self._session.tasks])

    def _load_zmx_file(self, src_file: str = "../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX") -> None:
        self._session.z_file_proto_src = src_file
        if not self._session.has_zemax_file:
            return
        if self._zemax_files_tabs:
            self._zmx_file_tab.layout().removeWidget(self._zemax_files_tabs)
        self._zemax_files_tabs = UIZemaxFileView()  # QTabWidget()
        self._zmx_file_tab.layout().addWidget(self._zemax_files_tabs)
        self._zemax_files_tabs.setup(self._session.z_file)

    def _run_task(self) -> None:
        if not self._session.is_valid:
            self._logging_area.append(f"Invalid task settings...")
            self._logging_area.append(f"Zemax file is : \"{self._session.z_file_proto_src}\"")
            self._logging_area.append(f"Task file or files are: \"{self._session.task_file_src}\"")
        self._session.run_task()

    def _save_results(self, report_directory: str) -> None:
        if not self._session.is_valid:
            return
        rdir = self._session.task_results_directory
        files = tuple((os.path.join(rdir, f), f)for f in os.listdir(rdir)if f.endswith('json'))
        report_directory = report_directory if report_directory != '' else rdir
        if not os.path.isdir(report_directory):
            os.mkdir(report_directory)
        for f_absolute_name, f_name in files:
            try:
                results = ResultFile()
                rep = Report()
                results.load(f_absolute_name)
                rep.update(results, True)
                name = '.'.join(v for v in f_name.split('.')[:-1])
                rep.save(os.path.join(report_directory, f"{name}.docx"))
            except Exception as ex:
                print(f"Report exception : {ex}")

    def _build_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        # help_menu = menu_bar.addMenu('&Help')
        file_menu.addAction('Open Zemax File', lambda: self._load_zmx_file(UIFileDialogs.open_file_name_dialog({'Zemax File': "zmx"})))
        file_menu.addAction('Open Task File', lambda: self._load_tasks(UIFileDialogs.open_file_names_dialog({'JSON File': "json"})))
        file_menu.addAction('Run Task File', lambda: self._run_task())
        file_menu.addAction('Make Report File', lambda: self._save_results(UIFileDialogs.save_directory_dialog()))
        file_menu.addAction('Exit', lambda: self._exit_app())

    def _exit_app(self):
        self.close()

    @staticmethod
    def run():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        load_style('UI/dark_theme_palette.json', app)
        UIMainWindow()
        sys.exit(app.exec())


if __name__ == '__main__':
    UIMainWindow.run()
