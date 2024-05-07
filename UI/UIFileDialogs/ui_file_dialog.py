from PyQt5.QtWidgets import QFileDialog
from typing import Dict


class UIFileDialogs:
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("\"UIFileDialogs\" class is static only!")

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
    def save_directory_dialog():
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(None, "QFileDialog.getOpenFileNames()", "", options=options)
        return directory

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
