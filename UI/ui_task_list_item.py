import random
import sys
from typing import Iterable, List, Set, Callable

from PyQt5.QtGui import QPalette, QColor
from TaskBuilder import SchemeParams, SurfaceParams
from ZFile import ZFile
from UI import BitSet32
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication, QCheckBox, QScrollArea, QSizePolicy, QFrame, QToolButton
from UI.UICollapsible.ui_collapsible_box import CollapsibleBox
from PyQt5.QtCore import Qt

_ACTIVE_BIT = 0
_COMMON_BIT = 1
_SPOT_BIT = 2
_PSF_BIT = 3
_MTF_BIT = 4

_SETTINGS_BITS = (_ACTIVE_BIT, _COMMON_BIT, _SPOT_BIT, _PSF_BIT, _MTF_BIT)


class UITaskListItem(QWidget):
    _items_ids: Set[int] = set()
    _items_ids_free: Set[int] = set()

    @staticmethod
    def _get_id() -> int:
        _id =  len(UITaskListItem._items_ids) if len(UITaskListItem._items_ids_free) == 0 else \
            UITaskListItem._items_ids_free.pop()
        UITaskListItem._items_ids.add(_id)
        return _id

    @staticmethod
    def init_check_box(name: str, callback=None) -> QCheckBox:
        check_box = QCheckBox(f"{name}")
        check_box.setChecked(True)
        if callback:
            check_box.toggled.connect(callback)
        return check_box

    def _toggle_default(self, bit: int, value: bool = None) -> bool:
        val = self._state.is_bit_set(bit)
        if value is None:
            return self._toggle_default(bit, not self._state.is_bit_set(bit))
        if self._state.is_bit_set(bit) == value:
            return value
        if value:
            self._state.set_bit(bit)
        else:
            self._state.clear_bit(bit)
        return value

    def _toggle_enable(self, value: bool = None) -> bool:
        if not self._toggle_default(_ACTIVE_BIT, value):
            self._common_check_box.setEnabled(False)
            self._psf_check_box.setEnabled(False)
            self._mtf_check_box.setEnabled(False)
            self._spot_check_box.setEnabled(False)
            return False
        else:
            self._common_check_box.setEnabled(True)
            self._psf_check_box.setEnabled(True)
            self._mtf_check_box.setEnabled(True)
            self._spot_check_box.setEnabled(True)
            return True

    @property
    def enabled(self) -> bool:
        return self._state.is_bit_set(_ACTIVE_BIT)

    @property
    def compute_common(self) -> bool:
        return self._state.is_bit_set(_COMMON_BIT)

    @property
    def compute_mtf(self) -> bool:
        return self._state.is_bit_set(_MTF_BIT)

    @property
    def compute_psf(self) -> bool:
        return self._state.is_bit_set(_PSF_BIT)

    @property
    def compute_spot(self) -> bool:
        return self._state.is_bit_set(_SPOT_BIT)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        if self._active_check_box.isChecked() == value:
            return
        self._active_check_box.setChecked(value)

    @compute_common.setter
    def compute_common(self, value: bool) -> None:
        if self._common_check_box.isChecked() == value:
            return
        self._common_check_box.setChecked(value)

    @compute_mtf.setter
    def compute_mtf(self, value: bool) -> None:
        if self._mtf_check_box.isChecked() == value:
            return
        self._mtf_check_box.setChecked(value)

    @compute_psf.setter
    def compute_psf(self, value: bool) -> None:
        if self._psf_check_box.isChecked() == value:
            return
        self._psf_check_box.setChecked(value)

    @compute_spot.setter
    def compute_spot(self, value: bool) -> None:
        if self._spot_check_box.isChecked() == value:
            return
        self._spot_check_box.setChecked(value)

    def __init__(self, item_name: str = None, parent=None):
        super(UITaskListItem, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self._item_id = UITaskListItem._get_id()
        self._state: BitSet32 = BitSet32()
        self._item_settings = CollapsibleBox(title=item_name if item_name else f"item: {self._item_id}", close_btn=True)
        # self._item_settings.setStyleSheet(generate_color())
        self.layout().setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout()
        for bit in _SETTINGS_BITS:
            self._state.set_bit(bit)
        self._active_check_box = UITaskListItem.init_check_box('ACTIVE', lambda: self._toggle_enable())
        self._common_check_box = UITaskListItem.init_check_box('COMMON', lambda: self._toggle_default(_COMMON_BIT))
        self._psf_check_box    = UITaskListItem.init_check_box('PSF', lambda: self._toggle_default(_PSF_BIT))
        self._mtf_check_box    = UITaskListItem.init_check_box('MTF', lambda: self._toggle_default(_MTF_BIT))
        self._spot_check_box   = UITaskListItem.init_check_box('SPOT', lambda: self._toggle_default(_SPOT_BIT))
        # self._active_check_box.setStyleSheet(generate_color())
        # self._common_check_box.setStyleSheet(generate_color())
        # self._psf_check_box.setStyleSheet(generate_color())
        # self._mtf_check_box.setStyleSheet(generate_color())
        # self._spot_check_box.setStyleSheet(generate_color())

        self._active_check_box. setMinimumHeight(30)
        self._common_check_box. setMinimumHeight(30)
        self._psf_check_box.    setMinimumHeight(30)
        self._mtf_check_box.    setMinimumHeight(30)
        self._spot_check_box.   setMinimumHeight(30)

        layout.addWidget(self._active_check_box)
        layout.addWidget(self._common_check_box)
        layout.addWidget(self._psf_check_box)
        layout.addWidget(self._mtf_check_box)
        layout.addWidget(self._spot_check_box)
        self._item_settings.set_content_layout(layout)
        self.layout().addWidget(self._item_settings)

    @property
    def show_button(self) -> QToolButton:
        return self._item_settings.toggle_button


class UITasksList(QScrollArea):
    @property
    def list_items(self) -> List[UITaskListItem]:
        return self._items

    def __init__(self, items: Iterable[str], parent=None):
        super(UITasksList, self).__init__(parent)
        self.setWidgetResizable(True)
        self.content = QWidget()
        self.content.setLayout(QVBoxLayout())
        self.content.layout().setAlignment(Qt.AlignTop)
        self.setAlignment(Qt.AlignTop)
        self.setWidget(self.content)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFrameShape(QFrame.NoFrame)
        self._items: List[UITaskListItem] = []
        self.setup(items)

    def setup(self, items: Iterable[str] = None, items_callbacks: Iterable[str] = None):
        if not items:
            return
        for i in reversed(range(self.content.layout().count())):
            self.content.layout().itemAt(i).widget().setParent(None)
        self._items.clear()
        for item in items:
            it = UITaskListItem(item)
            self.content.layout().addWidget(it)
            self._items.append(it)
        if not items_callbacks:
            return
        for item, callback in zip(self._items, items_callbacks):
            item.show_button.clicked.connect(callback)
            ...  # item.connect(UITaskFileViewsList.indices_call_back_wrapper(index, self._set_active_scheme))


class UITasksListView(QWidget):
    def _toggle_default(self, bit: int, value: bool = None) -> bool:
        if value is None:
            return self._toggle_default(bit, not self._state.is_bit_set(bit))
        if self._state.is_bit_set(bit) == value:
            return value
        if value:
            self._state.set_bit(bit)
        else:
            self._state.clear_bit(bit)
        return value

    def _toggle_enable(self, value: bool = None) -> bool:
        if not self._toggle_default(_ACTIVE_BIT, value):
            self._common_check_box.setEnabled(False)
            self._psf_check_box.setEnabled(False)
            self._mtf_check_box.setEnabled(False)
            self._spot_check_box.setEnabled(False)
            for item in self._items_list.list_items:
                item.enabled = False
            return False
        else:
            self._common_check_box.setEnabled(True)
            self._psf_check_box.setEnabled(True)
            self._mtf_check_box.setEnabled(True)
            self._spot_check_box.setEnabled(True)
            for item in self._items_list.list_items:
                item.enabled = True
            return True

    def _toggle_psf(self, value: bool = None) -> bool:
        if self._toggle_default(_PSF_BIT, value):
            for item in self._items_list.list_items:
                item.compute_psf = True
            return True
        else:
            for item in self._items_list.list_items:
                item.compute_psf = False
            return False

    def _toggle_mtf(self, value: bool = None) -> bool:
        if self._toggle_default(_MTF_BIT, value):
            for item in self._items_list.list_items:
                item.compute_mtf = True
            return True
        else:
            for item in self._items_list.list_items:
                item.compute_mtf = False
            return False

    def _toggle_spot(self, value: bool = None) -> bool:
        if self._toggle_default(_SPOT_BIT, value):
            for item in self._items_list.list_items:
                item.compute_spot = True
            return True
        else:
            for item in self._items_list.list_items:
                item.compute_spot = False
            return False

    def _toggle_common(self, value: bool = None) -> bool:
        if self._toggle_default(_COMMON_BIT, value):
            for item in self._items_list.list_items:
                item.compute_common = True
            return True
        else:
            for item in self._items_list.list_items:
                item.compute_common = False
            return False

    @property
    def enabled(self) -> bool:
        return self._state.is_bit_set(_ACTIVE_BIT)

    @property
    def compute_common(self) -> bool:
        return self._state.is_bit_set(_COMMON_BIT)

    @property
    def compute_mtf(self) -> bool:
        return self._state.is_bit_set(_MTF_BIT)

    @property
    def compute_psf(self) -> bool:
        return self._state.is_bit_set(_PSF_BIT)

    @property
    def compute_spot(self) -> bool:
        return self._state.is_bit_set(_SPOT_BIT)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._active_check_box.setChecked(self._toggle_enable(value))

    @compute_common.setter
    def compute_common(self, value: bool) -> None:
        self._common_check_box.setChecked(self._toggle_common(value))

    @compute_mtf.setter
    def compute_mtf(self, value: bool) -> None:
        self._mtf_check_box.setChecked(self._toggle_mtf(value))

    @compute_psf.setter
    def compute_psf(self, value: bool) -> None:
        self._psf_check_box.setChecked(self._toggle_psf(value))

    @compute_spot.setter
    def compute_spot(self, value: bool) -> None:
        self._spot_check_box.setChecked(self._toggle_spot(value))

    def __init__(self,  items: Iterable[str] = None, parent=None):
        super(UITasksListView, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self._state: BitSet32 = BitSet32()
        for bit in _SETTINGS_BITS:
            self._state.set_bit(bit)
        container = QWidget()
        container.setLayout(QVBoxLayout())
        self._active_check_box = UITaskListItem.init_check_box('ACTIVE', lambda: self._toggle_enable())
        self._common_check_box = UITaskListItem.init_check_box('COMMON', lambda: self._toggle_common())
        self._psf_check_box = UITaskListItem.init_check_box('PSF', lambda: self._toggle_psf())
        self._mtf_check_box = UITaskListItem.init_check_box('MTF', lambda: self._toggle_mtf())
        self._spot_check_box = UITaskListItem.init_check_box('SPOT', lambda: self._toggle_spot())
        self._items_list = UITasksList(items)
        container.layout().addWidget(self._active_check_box)
        container.layout().addWidget(self._common_check_box)
        container.layout().addWidget(self._psf_check_box)
        container.layout().addWidget(self._mtf_check_box)
        container.layout().addWidget(self._spot_check_box)
        self.layout().addWidget(container)
        self.layout().addWidget(self._items_list)
        self.layout().setAlignment(Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def setup(self, items: Iterable[str] = None, items_callbacks: Iterable[Callable] = None):
        self._items_list.setup(items, items_callbacks)


def generate_color() -> str:
    color = QColor(*[random.randint(0, 255) for _ in range(3)])
    return "background-color: {}; color : white;".format(color.name())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UITasksListView(tuple(f"item: {str(i + 1):>3}" for i in range(16)))
    # window.setStyleSheet(generate_color())
    window.show()
    sys.exit(app.exec_())
