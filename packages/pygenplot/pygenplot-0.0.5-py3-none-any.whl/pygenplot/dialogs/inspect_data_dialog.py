from typing import Any, Dict, List

import numpy as np

from qtpy import QtCore, QtGui, QtWidgets

from pygenplot.icons import ICONS
from pygenplot.views.table_views import QTableViewWithoutRightClick
from pygenplot.widgets.range_slider import RangeSlider


class InspectDataDialog(QtWidgets.QDialog):
    def __init__(self, dataset_info: Dict[str, Any], parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            dataset_info: the information about the dataset to display
            parent : the parent widget
        """
        super(InspectDataDialog, self).__init__(parent)

        self._dataset_info = dataset_info

        self._build()

        self.setWindowTitle(f"PyGenPlot - Raw data {dataset_info['variable']}")

    def _build(self):
        """Build the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        self._data_tableview = QTableViewWithoutRightClick()
        self._data_tableview.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self._data_tableview.customContextMenuRequested.connect(self.on_open_contextual_menu)
        main_layout.addWidget(self._data_tableview)

        if self._dataset_info["dimension"] > 1:
            grid_layout = QtWidgets.QGridLayout()

            self._row_button_group = QtWidgets.QButtonGroup()
            self._row_button_group.setExclusive(True)

            self._col_button_group = QtWidgets.QButtonGroup()
            self._col_button_group.setExclusive(True)

            grid_layout.addWidget(QtWidgets.QLabel("Axis"), 0, 0)
            grid_layout.addWidget(QtWidgets.QLabel("X"), 0, 1)
            grid_layout.addWidget(QtWidgets.QLabel("Y"), 0, 2)

            self._lines = []
            for i in range(self._dataset_info["dimension"]):
                axis_label = QtWidgets.QLabel()
                grid_layout.addWidget(axis_label, i + 1, 0)

                x_axis_radio_button = QtWidgets.QRadioButton("")
                grid_layout.addWidget(x_axis_radio_button, i + 1, 1)
                self._row_button_group.addButton(x_axis_radio_button)
                self._row_button_group.setId(x_axis_radio_button, i)

                y_axis_radio_button = QtWidgets.QRadioButton("")
                grid_layout.addWidget(y_axis_radio_button, i + 1, 2)
                self._col_button_group.addButton(y_axis_radio_button)
                self._col_button_group.setId(y_axis_radio_button, i)

                range_label = QtWidgets.QLabel("Range")
                grid_layout.addWidget(range_label, i + 1, 3)

                sum_range_slider = RangeSlider(QtCore.Qt.Orientation.Horizontal)
                grid_layout.addWidget(sum_range_slider, i + 1, 4)

                min_range_spinbox = QtWidgets.QSpinBox()
                grid_layout.addWidget(min_range_spinbox, i + 1, 5)

                max_range_spinbox = QtWidgets.QSpinBox()
                grid_layout.addWidget(max_range_spinbox, i + 1, 6)

                range_label = QtWidgets.QLabel()
                grid_layout.addWidget(range_label, i + 1, 7)

                sum_range_slider.slider_moved.connect(lambda mini, maxi, index=i: self.on_select_sum_range_by_slider(mini, maxi, index))
                min_range_spinbox.valueChanged.connect(lambda value, index=i: self.on_select_min_range_by_spinbox(value, index))
                max_range_spinbox.valueChanged.connect(lambda value, index=i: self.on_select_max_range_by_spinbox(value, index))

                self._lines.append(
                    [
                        axis_label,
                        x_axis_radio_button,
                        y_axis_radio_button,
                        range_label,
                        sum_range_slider,
                        min_range_spinbox,
                        max_range_spinbox,
                        range_label,
                    ]
                )

            self.set_dimension(0, 1)

            self._row_button_group.buttonClicked.connect(self.on_select_row)
            self._col_button_group.buttonClicked.connect(self.on_select_col)

            main_layout.addLayout(grid_layout)

        else:
            self._update()

        self.setLayout(main_layout)

    def _update(self):
        """ """
        model = QtGui.QStandardItemModel()

        if self._dataset_info["dimension"] == 1:
            for v in self._dataset_info["data"]:
                model.appendRow(QtGui.QStandardItem(str(v)))
        else:
            data = self._dataset_info["data"]

            # This will setup the slice of the nd data in order to reduce it to a 2D data
            # that can be displayed on the table
            sli = []
            # This will store the dimensions for which a sum has to be performed if any
            summed_axis = []
            for i in range(self._dataset_info["dimension"]):
                # For the selected row and column take the complete slice
                if (i == self._current_row) or (i == self._current_col):
                    sli.append(slice(None))
                else:
                    # Case where a sum is performed for dimension i: create a slice out of the
                    # min and max values of the corresponding spinboxes
                    first = self._lines[i][5].value()
                    last = self._lines[i][6].value()
                    s = slice(first, last + 1, 1)
                    sli.append(s)
                    summed_axis.append(i)

            data = data[tuple(sli)]
            # Sum the data if necessary. summed_axis can be empty - in such case no sum is performed
            data = np.sum(data, axis=tuple(summed_axis))
            # Transpose the data if necessary
            if self._current_row > self._current_col:
                data = data.T
            for row in data:
                model.appendRow([QtGui.QStandardItem(str(c)) for c in row])

        self._data_tableview.setModel(model)

    def on_copy_to_clipboard(self):
        """Callback called when some data has been copied to the clipboard."""
        model = self._data_tableview.model()
        selection_model = self._data_tableview.selectionModel()

        selected_columns = set()
        for data_range in selection_model.selection():
            for i in range(data_range.top(), data_range.bottom() + 1):
                for j in range(data_range.left(), data_range.right() + 1):
                    selected_columns.add(j)
        selected_columns = sorted(selected_columns)

        copied_data = []
        for data_range in selection_model.selection():
            for i in range(data_range.top(), data_range.bottom() + 1):
                line = []
                for j in selected_columns:
                    if j in range(data_range.left(), data_range.right() + 1):
                        value = model.data(model.index(i, j), QtCore.Qt.ItemDataRole.DisplayRole)
                    else:
                        value = ""
                    line.append(value)
                line = ",".join(line)
                copied_data.append(line)

        copied_data = "\n".join(copied_data)

        QtWidgets.QApplication.clipboard().setText(copied_data)

    def on_open_contextual_menu(self, point: QtCore.QPoint):
        """Callback called when the contextual menu is opened by right-clicking on the data.

        Args:
            point: the right-click point
        """
        menu = QtWidgets.QMenu(self)
        copy_to_clipboard_action = menu.addAction(ICONS["clipboard"], "Copy to clipboard")
        copy_to_clipboard_action.triggered.connect(self.on_copy_to_clipboard)
        menu.exec(self._data_tableview.mapToGlobal(point))

    def on_select_col(self, states: List[bool]):
        """Callback called when the index of the col buttongroup is changed.

        Args:
            states: the states of the button group
        """
        row_id = self._row_button_group.checkedId()
        col_id = self._col_button_group.checkedId()
        if row_id == col_id:
            self._lines[self._current_col][1].setChecked(True)
            self._current_row = self._current_col
        else:
            for i in range(3, len(self._lines)):
                self._lines[row_id][i].setDisabled(True)
                self._lines[self._current_col][i].setDisabled(False)

        self._current_col = col_id

        self.set_dimension(self._current_row, self._current_col)

    def on_select_min_range_by_spinbox(self, mini:int, index:int):
        """Callback called when the value of the minimum of the sum range spinbox is changed for a given axis.

        Args:
            mini: the minimum value
            index: the index of the axis
        """
        self._lines[index][4].setLow(mini)
        self._lines[index][6].setMinimum(mini)
        self._update()

    def on_select_max_range_by_spinbox(self, maxi:int, index:int):
        """Callback called when the value of the maximum of the sum range spinbox is changed for a given axis.

        Args:
            maxi: the maximum value
            index: the index of the axis
        """
        self._lines[index][4].setHigh(maxi)
        self._lines[index][5].setMaximum(maxi)
        self._update()

    def on_select_row(self, states:List[bool]):
        """Callback called when the index of the row buttongroup is changed.

        Args:
            states: the states of the button group
        """
        row_id = self._row_button_group.checkedId()
        col_id = self._col_button_group.checkedId()
        if row_id == col_id:
            self._lines[self._current_row][2].setChecked(True)
            self._current_col = self._current_row
        else:
            self._lines[row_id][3].setDisabled(True)
            self._lines[self._current_row][3].setDisabled(self._lines[self._current_row][5].isChecked())
            self._lines[row_id][4].setDisabled(True)
            self._lines[self._current_row][4].setDisabled(self._lines[self._current_row][5].isChecked())
            self._lines[row_id][5].setDisabled(True)
            self._lines[self._current_row][5].setDisabled(False)
            self._lines[row_id][6].setDisabled(True)
            self._lines[self._current_row][6].setDisabled(not self._lines[self._current_row][5].isChecked())
            self._lines[row_id][7].setDisabled(True)
            self._lines[self._current_row][7].setDisabled(not self._lines[self._current_row][5].isChecked())

        self._current_row = row_id

        self.set_dimension(self._current_row, self._current_col)

    def on_select_slice_by_slider(self, index: int):
        """Callback called when the selected slice slider value is changed for a given axis.

        Args:
            index: the index of the axis
        """
        value = self._lines[index][3].value()
        self._lines[index][4].blockSignals(True)
        self._lines[index][4].setValue(value)
        self._lines[index][4].blockSignals(False)
        self._update()

    def on_select_slice_by_spinbox(self, value:int, index:int):
        """Callback called when the selected slice spinbox value is changed for a given axis.

        Args:
            value: the selected slice
            index: the index of the axis
        """
        self._lines[index][3].blockSignals(True)
        self._lines[index][3].setValue(value)
        self._lines[index][3].blockSignals(False)
        self._update()

    def on_select_sum_range_by_slider(self, mini:int, maxi:int, index:int):
        """Callback called when the sum range value is changed through the corresponding slider for a given axis.

        Args:
            mini: the minimum value
            maxi: the maximum value
            index: the index of the axis
        """
        self._lines[index][6].blockSignals(True)
        self._lines[index][6].setMaximum(maxi)
        self._lines[index][6].setValue(mini)
        self._lines[index][6].blockSignals(False)
        self._lines[index][7].blockSignals(True)
        self._lines[index][7].setMinimum(mini)
        self._lines[index][7].setValue(maxi)
        self._lines[index][7].blockSignals(False)
        self._update()

    def set_dimension(self, row:int, col:int):
        """Set the selected row and column of the data to display.

        Args:
            row: the row to select
            col: the col to select
        """
        self._current_row = row
        self._current_col = col
        self._lines[row][1].setChecked(True)
        self._lines[col][2].setChecked(True)

        self._lines[self._current_row][3].setDisabled(True)
        self._lines[self._current_col][3].setDisabled(True)

        self._lines[self._current_row][4].setDisabled(True)
        self._lines[self._current_col][4].setDisabled(True)

        self._lines[self._current_row][5].setDisabled(True)
        self._lines[self._current_col][5].setDisabled(True)

        self._lines[self._current_row][6].setDisabled(True)
        self._lines[self._current_col][6].setDisabled(True)

        self._lines[self._current_row][7].setDisabled(True)
        self._lines[self._current_col][7].setDisabled(True)

        self._lines[self._current_row][8].setDisabled(True)
        self._lines[self._current_col][8].setDisabled(True)

        self._update()
