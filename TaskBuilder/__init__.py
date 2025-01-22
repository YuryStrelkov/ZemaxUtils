import json
import os.path
from typing import Dict

from .fields_params import load_fields_params
from .surface_params import read_surfaces
from .surface_params import SurfaceParams
from .fields_params import FieldsParams
from .scheme_params import SchemeParams
from .task_builder import TaskBuilder
from .waves_params import read_waves
from .fields_params import Field
from .waves_params import Wave


os.environ["ZEMAX_SETTINGS_PATH"] = os.path.join(os.path.dirname(__file__), "zemaxSettings.json")
os.environ["ZEMAX_SRC_SCRIPTS_DIR"] = os.path.join(os.path.dirname(__file__), "ZPLScripts")


def load_zemax_path_settings() -> Dict[str, str]:
    try:
        with open(os.environ["ZEMAX_SETTINGS_PATH"], "rt") as settings_file:
            vals = json.load(settings_file)
            return {"zemax_exe": vals['zemax_exe'] if 'zemax_cli' in vals else "empty...",
                    "zemax_cli": vals['zemax_cli'] if 'zemax_cli' in vals else "empty...",
                    "zemax_scripts": vals['zemax_scripts'] if 'zemax_scripts' in vals else "empty..."}
    except FileNotFoundError as _:
        ...
    return {"zemax_exe": "empty...",
            "zemax_cli": "empty...",
            "zemax_scripts": "empty..."}


def update_scripts(scripts_location: str) -> None:
    from distutils.dir_util import copy_tree
    copy_tree(os.environ["ZEMAX_SRC_SCRIPTS_DIR"], scripts_location)


def zemax_path_wizard() -> None:
    import sys
    from typing import Callable
    from PyQt5.QtWidgets import (
        QApplication,
        QHBoxLayout,
        QVBoxLayout,
        QPushButton,
        QFormLayout,
        QLineEdit,
        QWidget,
        QFileDialog,
        QDialogButtonBox,
    )

    def _is_exe(line_edit: QLineEdit) -> bool:
        file = line_edit.text()
        if flag := (os.path.isfile(file) and file.endswith("exe")):
            line_edit.setStyleSheet("color: black;  background-color: white")
        else:
            line_edit.setStyleSheet("color: red;  background-color: white")
        return flag

    def _is_dir(line_edit: QLineEdit) -> bool:
        file = line_edit.text()
        if flag := (os.path.isdir(file)):
            line_edit.setStyleSheet("color: black;  background-color: white")
        else:
            line_edit.setStyleSheet("color: red;  background-color: white")
        return flag

    def _open_directory(line_edit: QLineEdit) -> bool:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(None, "QFileDialog.getOpenFileNames()", "", options=options)
        line_edit.setText(directory if len(directory) else "empty...")
        return bool(len(directory))

    def _open_file(line_edit: QLineEdit) -> bool:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "",
                                                "Executables (*.exe)", options=options)
        line_edit.setText(files[-1] if len(files) else "empty...")
        return bool(len(files))

    def make_form_row(form: QFormLayout, *,
                      label_text: str,
                      button_text: str = "choose..",
                      default_text: str = "empty...",
                      text_changed_callback: Callable[[QLineEdit], bool] = None,
                      btn_pressed_callback: Callable[[QLineEdit], bool] = None) -> QLineEdit:
        _widget = QWidget()
        _layout = QHBoxLayout()
        _line = QLineEdit(default_text)
        if text_changed_callback:
            _line.textChanged.connect(lambda _: text_changed_callback(_line))
        _layout.addWidget(_line)
        _btn = QPushButton(button_text)
        if btn_pressed_callback:
            _btn.clicked.connect(lambda _: btn_pressed_callback(_line))
        _layout.addWidget(_btn)
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget.setLayout(_layout)
        form.addRow(label_text, _widget)
        return _line

    def _validate_paths(zemax_exe: QLineEdit, zemax_cli: QLineEdit, zemax_scripts: QLineEdit) -> bool:
        return all((_is_exe(zemax_exe), _is_exe(zemax_cli), _is_dir(zemax_scripts)))

    def _submit_paths(application: QApplication, zemax_exe: QLineEdit, zemax_cli: QLineEdit, zemax_scripts: QLineEdit):
        if not _validate_paths(zemax_exe, zemax_cli, zemax_scripts):
            return
        rep = ('\\', '/')
        update_scripts(zemax_scripts.text().replace(*rep))
        with open(os.environ["ZEMAX_SETTINGS_PATH"], "wt") as z_settings:
            print("{", file=z_settings)
            print(f"\t\"zemax_exe\":     \"{zemax_exe.text().replace(*rep)}\",", file=z_settings)
            print(f"\t\"zemax_cli\":     \"{zemax_cli.text().replace(*rep)}\",", file=z_settings)
            print(f"\t\"zemax_scripts\": \"{zemax_scripts.text().replace(*rep)}\"", file=z_settings)
            print("}", file=z_settings)
        application.exit()

    application = QApplication([])
    vertical_container = QWidget()
    vertical_container.resize(800, 150)
    vertical_container.setWindowTitle("Zemax paths wizard")
    vertical_container.setLayout(QVBoxLayout())
    paths = QWidget()
    vertical_container.layout().addWidget(paths)
    paths.setLayout(QFormLayout())
    settings = load_zemax_path_settings()
    line1 = make_form_row(paths.layout(),
                          label_text="Zemax \"exe\" location:",
                          text_changed_callback=_is_exe,
                          btn_pressed_callback=_open_file,
                          default_text=settings["zemax_exe"])
    line2 = make_form_row(paths.layout(),
                          label_text="Zemax \"CLI\" location:",
                          text_changed_callback=_is_exe,
                          btn_pressed_callback=_open_file,
                          default_text=settings["zemax_cli"])
    line3 = make_form_row(paths.layout(),
                          label_text="Zemax \"Scripts\" folder:",
                          text_changed_callback=_is_dir,
                          btn_pressed_callback=_open_directory,
                          default_text=settings["zemax_scripts"])
    buttons = QDialogButtonBox()
    buttons.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
    buttons.accepted.connect(lambda: _submit_paths(application, line1, line2, line3))
    buttons.rejected.connect(lambda: application.exit())
    buttons.setCenterButtons(True)
    vertical_container.layout().addWidget(buttons)
    # run ui
    vertical_container.show()
    sys.exit(application.exec())


def zemax_path_settings_check() -> None:
    settings_path = os.environ["ZEMAX_SETTINGS_PATH"]
    if os.path.isfile(settings_path):
        try:
            with open(settings_path, "rt") as settings_file:
                vals = json.load(settings_file)
                if all((os.path.isfile(vals['zemax_exe']) and vals['zemax_exe'].endswith("exe"),
                        os.path.isfile(vals['zemax_cli']) and vals['zemax_cli'].endswith("exe"),
                        os.path.isdir(vals['zemax_scripts']))):
                    os.environ["ZEMAX_EXE"] = vals['zemax_exe']
                    os.environ["ZEMAX_CLI"] = vals['zemax_cli']
                    return
        except KeyError as _:
            zemax_path_wizard()
    else:
        zemax_path_wizard()


zemax_path_settings_check()
# zemax_path_wizard()
