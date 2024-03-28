#  https://www.pythontutorial.net/pyqt/pyqt-qtablewidget/
import sys
from typing import List, Iterable, Union, Tuple

from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget,\
    QPushButton, QVBoxLayout, QTabWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from TaskBuilder import SchemeParams, SurfaceParams
from UI.ui_table import UITableWidget
# TODO remove


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Employees')
        self.setWindowIcon(QIcon('./assets/usergroup.png'))
        self.setGeometry(100, 100, 665, 400)
        params = SchemeParams.read("../ZemaxSchemesSettings/scheme_08_02_2024.json")[-1].surf_params
        self.table = UITableWidget.make_table(params)
        dock = QDockWidget('table-editor')
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
        self.create_buttons(dock)

    def create_buttons(self, parent):
        form   = QWidget()
        layout = QHBoxLayout(form)
        form.setLayout(layout)
        layout.setContentsMargins(2, 2, 2, 2)

        btn_add = QPushButton('AddRow')
        btn_add.clicked.connect(lambda: self.table.append_row())
        layout.addWidget(btn_add)

        btn_rem = QPushButton('RemRow')
        btn_rem.clicked.connect(lambda: self.table.remove_rows(show_confirm_dialog=True))
        layout.addWidget(btn_rem)

        btn_add = QPushButton('AddCol')
        btn_add.clicked.connect(lambda: self.table.append_col())
        layout.addWidget(btn_add)

        btn_rem = QPushButton('RemCol')
        btn_rem.clicked.connect(lambda: self.table.remove_cols(show_confirm_dialog=True))
        layout.addWidget(btn_rem)

        btn_rem = QPushButton('RemSelected')
        btn_rem.clicked.connect(lambda: self.table.remove_selection(show_confirm_dialog=True))
        layout.addWidget(btn_rem)
        parent.setWidget(form)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())