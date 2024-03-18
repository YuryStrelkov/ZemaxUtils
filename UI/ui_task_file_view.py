from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QApplication, QPushButton
from PyQt5.QtCore import Qt
from TaskBuilder import SchemeParams, SurfaceParams
from UI.ui_collapsible_box import CollapsibleBox
from UI.ui_table import UITableWidget
from typing import List, Union


class UITaskFileView(QScrollArea):
    def __init__(self, parent=None):
        super(UITaskFileView, self).__init__(parent)
        content = QWidget()
        content.setLayout(QVBoxLayout())
        content.layout().setAlignment(Qt.AlignTop)
        self.setWidget(content)
        self.setWidgetResizable(True)
        self._scheme_common_info = CollapsibleBox(title="SCHEME COMMON")
        self._scheme_surfs_remap = CollapsibleBox(title="SURFACES REMAP")
        self._scheme_fields      = CollapsibleBox(title="SCHEME FIELDS")
        self._scheme_waves       = CollapsibleBox(title="SCHEME WAVES")
        self._scheme_surfaces    = CollapsibleBox(title="SCHEME SURFACES")
        self._scheme_extra_data  = CollapsibleBox(title="SCHEME EXTRA DATA")
        content.layout().addWidget(self._scheme_common_info)
        content.layout().addWidget(self._scheme_surfs_remap)
        content.layout().addWidget(self._scheme_fields)
        content.layout().addWidget(self._scheme_waves)
        content.layout().addWidget(self._scheme_surfaces)
        content.layout().addWidget(self._scheme_extra_data)
        content.layout().addStretch()

    def setup(self, content: SchemeParams):
        self.set_scheme_fields(content)
        self.set_scheme_surfs_remap(content)
        self.set_scheme_waves(content)
        self.set_scheme_surfaces(content)
        self.set_scheme_extra_data(content)
        self.set_scheme_common_info(content)

    @staticmethod
    def _info_label(label_text: str) -> QVBoxLayout:
        info_label = QLabel()
        info_layout = QVBoxLayout()
        info_label.setText(label_text)
        info_layout.addWidget(info_label)
        return info_layout

    def set_scheme_surfs_remap(self, scheme: SchemeParams) -> 'UITaskFileView':
        if not scheme.surf_remap:
            self._scheme_surfs_remap.set_content_layout(UITaskFileView._info_label("No surfaces remap info..."))
            return self
        layout = QVBoxLayout()
        data = tuple((("scheme index", k), ("Zemax index", v)) for k, v in scheme.surf_remap.items())
        layout.addWidget(UITableWidget.make_table_from_iterable(data))
        self._scheme_surfs_remap.set_content_layout(layout)
        return self

    def set_scheme_waves(self, scheme: SchemeParams) -> 'UITaskFileView':
        if not scheme.waves:
            self._scheme_waves.set_content_layout(UITaskFileView._info_label("No wave lengths data..."))
            return self
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.waves))
        self._scheme_waves.set_content_layout(layout)
        return self

    def set_scheme_fields(self, scheme: SchemeParams) -> 'UITaskFileView':
        if not scheme.fields:
            self._scheme_fields.set_content_layout(UITaskFileView._info_label("No fields data..."))
            return self
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.fields.fields))
        self._scheme_fields.set_content_layout(layout)
        return self

    def set_scheme_surfaces(self, scheme: SchemeParams) -> 'UITaskFileView':
        if not scheme.surf_params:
            self._scheme_surfaces.set_content_layout(UITaskFileView._info_label("No surfaces data..."))
            return self
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.surf_params))
        self._scheme_surfaces.set_content_layout(layout)
        return self

    def set_scheme_extra_data(self, scheme: SchemeParams) -> 'UITaskFileView':
        if not scheme.surf_params:
            self._scheme_extra_data.set_content_layout(UITaskFileView._info_label("No extra data..."))
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

    def set_scheme_common_info(self, scheme: SchemeParams) -> 'UITaskFileView':
        layout = QVBoxLayout()
        info1 = QLabel()
        info2 = QLabel()
        info1.setText(scheme.description_short)
        info2.setText(scheme.description_long)
        layout.addWidget(info1)
        layout.addWidget(info2)
        self._scheme_common_info.set_content_layout(layout)
        return self


class UITaskFileViewsList(QWidget):
    class indices_call_back_wrapper:
        def __init__(self, index: int, callback):
            self._index = index
            self._callback = callback

        def __call__(self, *args, **kwargs):
            self._callback(self._index)

    def __init__(self, parent=None):
        super(UITaskFileViewsList, self).__init__(parent)
        self._schemes_list = QScrollArea()
        self._scheme_view  = UITaskFileView()
        self._scheme_params: Union[List[SchemeParams], None] = None
        self._active_scheme = -1
        self._active_button = None  # Union[QPushButton, ]
        self._active_button_style = None
        layout = QHBoxLayout()
        layout.addWidget(self._schemes_list)
        layout.addWidget(self._scheme_view, 1)
        self._schemes_list_content = QWidget()
        self._schemes_list.setWidget(self._schemes_list_content)
        self._schemes_list.setWidgetResizable(True)
        schemes_list_content_layout = QVBoxLayout(self._schemes_list_content)
        schemes_list_content_layout.layout().setAlignment(Qt.AlignTop)
        self.setLayout(layout)

    @staticmethod
    def _clear_layout(layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def _set_active_scheme(self, index: int):
        if index == self._active_scheme:
            return
        if self._active_button is not None:
            self._active_button.setChecked(False)
        self._active_button = self._schemes_list_content.layout().itemAt(index).widget()
        self._active_scheme = index
        self._scheme_view.deleteLater()
        self._scheme_view = UITaskFileView()
        self.layout().addWidget(self._scheme_view, 1)
        self._scheme_view.setup(self._scheme_params[index])

    def _setup_schemes_list(self):
        UITaskFileViewsList._clear_layout(self._schemes_list_content.layout())
        for index, schemes in enumerate(self._scheme_params):
            desc = schemes.description_short
            btn = QPushButton(f"{index} : {desc if len(desc) < 20 else desc[0:17] + '...'}")
            btn.setCheckable(True)
            btn.clicked.connect(UITaskFileViewsList.indices_call_back_wrapper(index, self._set_active_scheme))
            self._schemes_list_content.layout().addWidget(btn)

    def setup(self, params: List[SchemeParams]):
        self._scheme_params = params
        self._setup_schemes_list()
        self._active_scheme = -1
        self._set_active_scheme(0)


def run():
    import sys
    scheme = SchemeParams.read("../ZemaxSchemesSettings/polychrome.json")
    app = QApplication(sys.argv)
    window = UITaskFileViewsList()
    window.setup(scheme)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
