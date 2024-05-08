from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea
from UI import render_scheme_preview
from UI import CollapsibleBox
from UI import UITableWidget
from PyQt5.QtCore import Qt
import matplotlib as plt
from ZFile import ZFile
plt.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class UIZemaxFileView(QScrollArea):
    def __init__(self, parent=None):
        super(UIZemaxFileView, self).__init__(parent)
        content = QWidget()
        content.setLayout(QVBoxLayout())
        content.layout().setAlignment(Qt.AlignTop)
        self.setWidget(content)
        self.setWidgetResizable(True)
        self._scheme_preview = QWidget()  # CollapsibleBox(title="SCHEME PREVIEW")
        self._scheme_preview.setLayout(QVBoxLayout())  # CollapsibleBox(title="SCHEME PREVIEW")
        self._scheme_preview.setFixedHeight(800)
        # self._scheme_preview = CollapsibleBox(title="SCHEME PREVIEW")
        self._scheme_common_info = CollapsibleBox(title="SCHEME COMMON")
        # self._scheme_surfs_remap = CollapsibleBox(title="SURFACES REMAP")
        self._scheme_fields = CollapsibleBox(title="SCHEME FIELDS")
        self._scheme_waves = CollapsibleBox(title="SCHEME WAVES")
        self._scheme_surfaces = CollapsibleBox(title="SCHEME SURFACES")
        self._scheme_extra_data = CollapsibleBox(title="SCHEME EXTRA DATA")
        self._label = QLabel("\nParams of zemax scheme ... \n")
        content.layout().addWidget(self._label)
        content.layout().addWidget(self._scheme_preview)
        content.layout().addWidget(self._scheme_common_info)
        content.layout().addWidget(self._scheme_fields)
        content.layout().addWidget(self._scheme_waves)
        content.layout().addWidget(self._scheme_surfaces)
        content.layout().addWidget(self._scheme_extra_data)

    def set_label_test(self, text: str) -> None:
        self._label.setText(f"\nParams of zemax scheme \"{text}\" \n")

    def setup(self, content: ZFile):
        self.set_scheme_preview(content)
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

    def set_scheme_waves(self, scheme: ZFile) -> 'UIZemaxFileView':
        layout = QVBoxLayout()
        waves = tuple((('wave length', wl), ('weight', ww)) for wl, ww in
                      zip(scheme.waves.wavelengths, scheme.waves.weights))
        layout.addWidget(UITableWidget.make_table_from_iterable(waves))
        self._scheme_waves.set_content_layout(layout)
        return self

    def set_scheme_preview(self, scheme: ZFile) -> 'UIZemaxFileView':
        if not scheme.fields:
            # self._scheme_preview.set_content_layout(UIZemaxFileView._info_label("No preview data..."))
            self._scheme_preview.layout().addWidget(UIZemaxFileView._info_label("No preview data..."))
            return self
        self.set_label_test(scheme.name.params[0])
        sc = MplCanvas()
        toolbar = NavigationToolbar(sc)
        render_scheme_preview(scheme, axis=sc.axes)
        self._scheme_preview.layout().addWidget(toolbar)
        self._scheme_preview.layout().addWidget(sc)
        # sc.fig.tight_layout()
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
