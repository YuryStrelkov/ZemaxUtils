import sys
from typing import Dict

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon


class UIFileDialogs:
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("\"UIFileDialogs\" class is static only!")
    # def __init__(self):
    #     super().__init__()
    #     self.title = 'PyQt5 file dialogs - pythonspot.com'
    #     self.border = (10, 10, 640, 640)
    #     self.init_ui()

    # def init_ui(self):
    #     self.setWindowTitle(self.title)
    #     self.setGeometry(*self.border)
    #     print(self.open_file_name_dialog())
    #     print(self.open_file_names_dialog())
    #     print(self.save_file_dialog())
    #     self.show()

    @staticmethod
    def _parce_filters(filters: Dict[str, str] = None) -> str:
        if filters:
            return ";;".join(f"{f_name} (*.{f_filter})" for f_name, f_filter in filters.items())
        else:
            return "All Files (*);;JSON Files (*.json)"

    @staticmethod
    def open_file_name_dialog(filters: Dict[str, str] = None):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                   UIFileDialogs._parce_filters(filters), options=options)
        return file_name

    @staticmethod
    def open_file_names_dialog(filters: Dict[str, str] = None):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "",
                                                UIFileDialogs._parce_filters(filters), options=options)
        return files

    @staticmethod
    def save_file_dialog(filters: Dict[str, str] = None):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(None, "QFileDialog.getSaveFileName()", "",
                                                   UIFileDialogs._parce_filters(filters), options=options)
        return file_name


#  if __name__ == '__main__':
#      app = QApplication(sys.argv)
#      ex = UIFileDialogs()
#      sys.exit(app.exec_())