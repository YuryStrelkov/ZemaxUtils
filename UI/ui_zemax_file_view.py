from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QApplication, QPushButton
from PyQt5.QtCore import Qt
from TaskBuilder import SchemeParams, SurfaceParams
from UI.ui_collapsible_box import CollapsibleBox
from UI.ui_table import UITableWidget
from ZFile import ZFile
from typing import List, Union


class UIZemaxFileView(QScrollArea):
    def __init__(self, parent=None):
        super(UIZemaxFileView, self).__init__(parent)
        content = QWidget()
        content.setLayout(QVBoxLayout())
        content.layout().setAlignment(Qt.AlignTop)
        self.setWidget(content)
        self.setWidgetResizable(True)
        self._scheme_common_info = CollapsibleBox(title="SCHEME COMMON")
        # self._scheme_surfs_remap = CollapsibleBox(title="SURFACES REMAP")
        self._scheme_fields      = CollapsibleBox(title="SCHEME FIELDS")
        self._scheme_waves       = CollapsibleBox(title="SCHEME WAVES")
        self._scheme_surfaces    = CollapsibleBox(title="SCHEME SURFACES")
        self._scheme_extra_data  = CollapsibleBox(title="SCHEME EXTRA DATA")
        content.layout().addWidget(self._scheme_common_info)
        # content.layout().addWidget(self._scheme_surfs_remap)
        content.layout().addWidget(self._scheme_fields)
        content.layout().addWidget(self._scheme_waves)
        content.layout().addWidget(self._scheme_surfaces)
        content.layout().addWidget(self._scheme_extra_data)
        content.layout().addStretch()

    def setup(self, content: ZFile):
        self.set_scheme_fields(content)
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

    # def set_scheme_surfs_remap(self, scheme: SchemeParams) -> 'UIZemaxFileView':
    #     if not scheme.surf_remap:
    #         self._scheme_surfs_remap.set_content_layout(UIZemaxFileView._info_label("No surfaces remap info..."))
    #         return self
    #     layout = QVBoxLayout()
    #     data = tuple((("scheme index", k), ("Zemax index", v)) for k, v in scheme.surf_remap.items())
    #     layout.addWidget(UITableWidget.make_table_from_iterable(data))
    #     self._scheme_surfs_remap.set_content_layout(layout)
    #     return self

    def set_scheme_waves(self, scheme: ZFile) -> 'UIZemaxFileView':
        layout = QVBoxLayout()
        waves = tuple((('wave length', wl), ('weight', ww)) for wl, ww in
                      zip(scheme.waves.wavelengths, scheme.waves.weights))
        layout.addWidget(UITableWidget.make_table_from_iterable(waves))
        self._scheme_waves.set_content_layout(layout)
        return self

    def set_scheme_fields(self, scheme: ZFile) -> 'UIZemaxFileView':
        if not scheme.fields:
            self._scheme_fields.set_content_layout(UIZemaxFileView._info_label("No fields data..."))
            return self
        layout = QVBoxLayout()
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.fields.fields))
        layout.addWidget(UITableWidget.make_table_from_iterable(scheme.fields.fields_info))
        self._scheme_fields.set_content_layout(layout)
        return self

    def set_scheme_surfaces(self, scheme: ZFile) -> 'UIZemaxFileView':
        layout = QVBoxLayout()
        surfaces = scheme.surfaces_params
        surfaces_transforms = tuple(tuple(t.transforms_info) for t in scheme.surfaces.values())
        layout.addWidget(UITableWidget.make_table_from_iterable(surfaces))
        layout.addWidget(UITableWidget.make_table_from_iterable(surfaces_transforms))
        self._scheme_surfaces.set_content_layout(layout)
        return self

    def set_scheme_extra_data(self, scheme: ZFile) -> 'UIZemaxFileView':
        max_extra_length = max(len(v.extra_params) for v in scheme.surfaces.values())
        if max_extra_length == 0:
            self._scheme_extra_data.set_content_layout(UIZemaxFileView._info_label("No extra data..."))
            return self
        return self

    def set_scheme_common_info(self, scheme: ZFile) -> 'UIZemaxFileView':
        layout = QVBoxLayout()
        v = tuple(scheme.common_params)
        layout.addWidget(UITableWidget.make_table_from_iterable(tuple(scheme.common_params)))
        self._scheme_common_info.set_content_layout(layout)
        return self
