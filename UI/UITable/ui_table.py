#  https://www.pythontutorial.net/pyqt/pyqt-qtablewidget/
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy
from typing import List, Iterable, Union, Tuple


class UITableWidget(QTableWidget):
    def __init__(self, parent, colons: int = 0):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.setColumnCount(colons)

    @property
    def rows(self) -> int:
        return self.rowCount()

    @property
    def cols(self) -> int:
        return self.columnCount()

    @rows.setter
    def rows(self, rows: int) -> None:
        self.setRowCount(rows)

    @cols.setter
    def cols(self, rows: int) -> None:
        self.setColumnCount(rows)

    @property
    def colons_widths(self) -> List[int]:
        return [self.columnWidth(col) for col in range(self.cols)]

    @property
    def rows_heights(self) -> List[int]:
        return [self.rowHeight(col) for col in range(self.rows)]

    @rows_heights.setter
    def rows_heights(self, heights: Iterable[int]) -> None:
        if isinstance(heights, Iterable):
            [self.setRowHeight(row, height) for row, height in enumerate(heights) if row < self.rows]
        if isinstance(heights, int):
            [self.setRowHeight(row, heights) for row in range(self.rows)]

    @colons_widths.setter
    def colons_widths(self, widths: Iterable[int]) -> None:
        if isinstance(widths, Iterable):
            [self.setColumnWidth(col, width) for col, width in enumerate(widths) if col < self.cols]
        if isinstance(widths, int):
            [self.setColumnWidth(col, widths) for col in range(self.cols)]

    @property
    def table_headers(self) -> List[str]:
        return [self.horizontalHeaderItem(column).text() for column in range(self.cols)]

    @table_headers.setter
    def table_headers(self, headers: Iterable[str]) -> None:
        self.setHorizontalHeaderLabels([header for col, header in enumerate(headers) if col < self.cols])

    @property
    def rows_selected_indices(self) -> Tuple[int, ...]:
        return tuple(cell.row() for cell in self.selectedIndexes())

    @property
    def cols_selected_indices(self) -> Tuple[int, ...]:
        return tuple(cell.column() for cell in self.selectedIndexes())

    def append_col(self, title: str = None, col_data: Iterable[str] = None) -> None:
        col = self.columnCount()
        self.insertColumn(col)
        col_title = QTableWidgetItem(str(title) if title else f"Column {col + 1:3}")
        self.setHorizontalHeaderItem(col, col_title)
        if col_data:
            [self.setItem(index, col, QTableWidgetItem(text))
             for index, text in enumerate(col_data) if index < self.rows]
        else:
            [self.setItem(index, col, QTableWidgetItem(f"cell [{index:3}, {col:3}]")) for index in range(self.rows)]

    def append_row(self, row_data: Iterable[str] = None) -> None:
        row = self.rowCount()
        self.insertRow(row)
        if row_data:
            [self.setItem(row, index, QTableWidgetItem(text))
             for index, text in enumerate(row_data) if index < self.cols]
        else:
            [self.setItem(row, index, QTableWidgetItem(f"cell [{row:3}, {index:3}]")) for index in range(self.cols)]

    def row_deletion_confirmation_dialog(self, text: str):
        return QMessageBox.question(self, 'Confirmation', text,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    def _remove_row(self, indices: Iterable[int]):
        if any(v < 0 for v in indices):
            return QMessageBox.warning(self, 'Warning', 'Please select a correct rows to delete')
        indices = sorted(indices, reverse=True)
        [self.removeRow(row_id) for row_id in indices]

    def _remove_col(self, indices: Iterable[int]):
        if any(v < 0 for v in indices):
            return QMessageBox.warning(self, 'Warning', 'Please select a correct cols to delete')
        indices = sorted(indices, reverse=True)
        [self.removeColumn(col_id) for col_id in indices]

    def remove_selection(self, show_confirm_dialog: bool = False) -> None:
        rows = set(self.rows_selected_indices)
        cols = set(self.cols_selected_indices)
        if show_confirm_dialog and (len(rows) != 1 or len(cols) != 1):
            if self.row_deletion_confirmation_dialog(
                    f'Are you sure that you want to delete the selected rows/cols?') == \
                    QMessageBox.StandardButton.Yes:
                self.remove_rows(rows, show_confirm_dialog=False)
                self.remove_cols(cols, show_confirm_dialog=False)
                return
        self.remove_rows(rows, show_confirm_dialog=False)
        self.remove_cols(cols, show_confirm_dialog=False)

    def remove_rows(self, indices: Union[int, Iterable[int]] = None, show_confirm_dialog: bool = False) -> None:
        indices =  indices if indices else set(self.rows_selected_indices)
        if show_confirm_dialog and len(indices) > 1:
            if self.row_deletion_confirmation_dialog(
                    f'Are you sure that you want to delete the selected {",".join(str(i + 1) for i in indices)} rows?') == \
                    QMessageBox.StandardButton.Yes:
                self._remove_row(indices)
                return
        self._remove_row(indices)

    def remove_cols(self, indices: Union[int, Iterable[int]] = None, show_confirm_dialog: bool = False) -> None:
        indices = indices if indices else set(self.cols_selected_indices)
        if show_confirm_dialog and len(indices) > 1:
            if self.row_deletion_confirmation_dialog(
                    f'Are you sure that you want to delete the selected {",".join(str(i + 1) for i in indices)} cols?') == \
                    QMessageBox.StandardButton.Yes:
                self._remove_col(indices)
                return
        self._remove_col(indices)

    @classmethod
    def make_table_from_iterable(cls, values: Union[List[Iterable], Tuple[Iterable, ...]],
                                 colons_withs: Iterable[int] = None,
                                 rows_heights: Iterable[int] = None) -> 'UITableWidget':
        table = cls(None, 0)
        if len(values) == 0:
            return table
        try:
            first = values[0]
            headers = tuple(header for header, _ in first)
            for header in headers:
                table.append_col(header)
        except Exception as ex:
            print(f"type {type(values[0])} is not iterable...\n{ex.args}")
            return table
        for value in values:
            params = tuple(str(val) if isinstance(val, int) or isinstance(val, str) else f"{val:>.4}" for _, val in value)
            table.append_row(params)
        table.colons_widths = tuple(v for v in colons_withs) if colons_withs else 100
        table.rows_heights = tuple(v for v in rows_heights) if rows_heights else 20
        return table
