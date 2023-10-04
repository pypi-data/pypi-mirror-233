from typing import List, Tuple

from qtpy import QtCore, QtWidgets

from ..kernel.logger import log
from ..models.plot_nd_model import PlotNDModel, PlotNDModelError
from ..widgets.range_slider import RangeSlider


class DataSlicerWidget(QtWidgets.QWidget):

    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the underlying ND plot model
            parent: the parent widget
        """
        super(DataSlicerWidget, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._current_x_index = 0
        self._current_y_index = 1

        self._build()

    def _build(self):
        """Builds the widget."""
        self._main_layout = QtWidgets.QVBoxLayout()

        grid_layout = QtWidgets.QGridLayout()

        self._x_axis_button_group = QtWidgets.QButtonGroup()
        self._x_axis_button_group.setExclusive(True)

        self._y_axis_button_group = QtWidgets.QButtonGroup()
        self._y_axis_button_group.setExclusive(True)

        grid_layout.addWidget(QtWidgets.QLabel("Axis"), 0, 0)
        grid_layout.addWidget(QtWidgets.QLabel("X"), 0, 1)
        grid_layout.addWidget(QtWidgets.QLabel("Y"), 0, 2)

        self._lines = []

        dataset_info = self._plot_nd_model.get_dataset_info()

        for i in range(dataset_info[0]["dimension"]):
            axis_label = QtWidgets.QLabel()
            grid_layout.addWidget(axis_label, i + 1, 0)

            x_axis_radio_button = QtWidgets.QRadioButton("")
            grid_layout.addWidget(x_axis_radio_button, i + 1, 1)
            self._x_axis_button_group.addButton(x_axis_radio_button)
            self._x_axis_button_group.setId(x_axis_radio_button, i)

            y_axis_radio_button = QtWidgets.QRadioButton("")
            grid_layout.addWidget(y_axis_radio_button, i + 1, 2)
            self._y_axis_button_group.addButton(y_axis_radio_button)
            self._y_axis_button_group.setId(y_axis_radio_button, i)

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

            sum_range_slider.slider_moved.connect(
                lambda mini, maxi, index=i: self.on_select_sum_range_by_slider(mini, maxi, index)
            )
            min_range_spinbox.valueChanged.connect(
                lambda value, index=i: self.on_select_min_range_by_spinbox(value, index)
            )
            max_range_spinbox.valueChanged.connect(
                lambda value, index=i: self.on_select_max_range_by_spinbox(value, index)
            )

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

        self._main_layout.addLayout(grid_layout)

        self.setLayout(self._main_layout)

        self._init_slices()

        self._update_selected_axis()

        self._x_axis_button_group.buttonClicked.connect(self.on_select_x_axis)
        self._y_axis_button_group.buttonClicked.connect(self.on_select_y_axis)

    def _get_slices(self) -> Tuple[slice]:
        """Builds and returns the slices.

        Returns:
            the slices for each axis of the dataset
        """
        slices = []
        for i, line in enumerate(self._lines):
            if (i == self._current_x_index) or (i == self._current_y_index):
                slices.append(slice(None))
            else:
                slices.append(slice(line[5].value(), line[6].value() + 1, 1))

        return tuple(slices)

    def _init_slices(self):
        """Initializes the slices."""
        self._lines[self._current_x_index][1].setChecked(True)
        self._lines[self._current_y_index][2].setChecked(True)

        for i in range(3, len(self._lines[0])):
            self._lines[self._current_x_index][i].setDisabled(True)
            self._lines[self._current_y_index][i].setDisabled(True)

        axis_info = self._plot_nd_model.get_axis_info()
        dataset_info = self._plot_nd_model.get_dataset_info()

        z_data_shape = dataset_info[0]["shape"]

        axis_variables = [axis["variable"] for axis in axis_info]
        axis_current_units = [axis["units"] for axis in axis_info]

        for i, (variable, unit) in enumerate(zip(axis_variables, axis_current_units)):
            self._lines[i][0].setText(f"{variable} ({unit})")

            self._lines[i][4].blockSignals(True)
            self._lines[i][4].setMinimum(0)
            self._lines[i][4].setMaximum(z_data_shape[i] - 1)
            self._lines[i][4].set_low(0)
            self._lines[i][4].set_high(z_data_shape[i] - 1)
            self._lines[i][4].blockSignals(False)

            self._lines[i][5].blockSignals(True)
            self._lines[i][5].setMinimum(0)
            self._lines[i][5].setMaximum(z_data_shape[i] - 1)
            self._lines[i][5].blockSignals(True)
            self._lines[i][5].setValue(0)
            self._lines[i][5].blockSignals(False)

            self._lines[i][6].blockSignals(True)
            self._lines[i][6].setMinimum(0)
            self._lines[i][6].setMaximum(z_data_shape[i] - 1)
            self._lines[i][6].blockSignals(True)
            self._lines[i][6].setValue(z_data_shape[i] - 1)
            self._lines[i][6].blockSignals(False)

        self._update_slices()

    def _update_range_labels(self):
        """Updates the sum range labels."""
        axis_data = self._plot_nd_model.get_axis_current_data()
        axis_units = self._plot_nd_model.get_axis_current_units()

        for i, (line, data, unit) in enumerate(zip(self._lines,axis_data,axis_units)):
            mini = line[5].value()
            maxi = line[6].value()
            first = data[mini]
            last = data[maxi]
            line[7].setText(f"from {first} {unit} to {last} {unit}")

    def _update_selected_axis(self):
        """Sets the selected X axis for performing the slice."""
        self._update_range_labels()
        self._update_range_labels()
        self._update_slices()

    def _update_slices(self):
        """Updates the slices."""
        slices = self._get_slices()
        transpose = self._current_x_index > self._current_y_index
        try:
            self._plot_nd_model.update_model(slices, transpose)
        except PlotNDModelError as e:
            log(str(e), ["main", "popup"], "error")

    @property
    def current_x_index(self) -> int:
        """Returns the current X index.

        Returns:
            the current x index
        """
        return self._current_x_index

    @property
    def current_y_index(self) -> int:
        """Returns the current Y index.

        Returns:
            the current y index
        """
        return self._current_y_index

    def on_select_min_range_by_spinbox(self, mini: int, index: int):
        """Selects the min range value for a given axis.

        Args:
            mini: the minimum value
            index: the index of the axis
        """
        self._lines[index][4].set_low(mini)
        self._lines[index][6].setMinimum(mini)
        self._update_range_labels()

        self._update_slices()

    def on_select_max_range_by_spinbox(self, maxi: int, index: int):
        """Selects the max range value for a given axis.

        Args:
            maxi: the maximum value
            index: the index of the axis
        """
        self._lines[index][4].set_high(maxi)
        self._lines[index][5].setMaximum(maxi)
        self._update_range_labels()

        self._update_slices()

    def on_select_sum_range_by_slider(self, mini: int, maxi: int, index: int):
        """Selects the range for a given axis.

        Args:
            mini: the minimum value
            maxi: the maximum value
            index: the index of the axis
        """
        self._lines[index][5].blockSignals(True)
        self._lines[index][5].setMaximum(maxi)
        self._lines[index][5].setValue(mini)
        self._lines[index][5].blockSignals(False)
        self._lines[index][6].blockSignals(True)
        self._lines[index][6].setMinimum(mini)
        self._lines[index][6].setValue(maxi)
        self._lines[index][6].blockSignals(False)

        self._update_range_labels()

        self._update_slices()

    def on_select_x_axis(self, states: List[bool]):
        """Selects an X axis.

        Args:
            states: the states of the button group
        """
        x_axis_id = self._x_axis_button_group.checkedId()
        y_axis_id = self._y_axis_button_group.checkedId()

        if x_axis_id == y_axis_id:
            self._lines[self._current_x_index][2].setChecked(True)
            self._current_x_index, self._current_y_index = self._current_y_index, self._current_x_index
        else:
            for i in range(3, len(self._lines[0])):
                self._lines[x_axis_id][i].setDisabled(False)
                self._lines[self._current_x_index][i].setDisabled(True)
            self._current_x_index = x_axis_id

        self._update_selected_axis()

    def on_select_y_axis(self, states: List[bool]):
        """Selects a Y axis.

        Args:
            states: the states of the button group
        """
        x_axis_id = self._x_axis_button_group.checkedId()
        y_axis_id = self._y_axis_button_group.checkedId()

        if x_axis_id == y_axis_id:
            self._lines[self._current_y_index][1].setChecked(True)
            self._current_x_index, self._current_y_index = self._current_y_index, self._current_x_index
        else:
            for i in range(3, len(self._lines[0])):
                self._lines[y_axis_id][i].setDisabled(True)
                self._lines[self._current_y_index][i].setDisabled(False)
            self._current_y_index = y_axis_id

        self._update_selected_axis()

    def on_x_axis_updated(self, variable: str):
        """Updates the labels when X axis has been updated.

        Args:
            variable: the selected variable
        """
        self._lines[self._current_x_index][0].setText(f"{variable}")
        self._update_range_labels()

    def on_y_axis_updated(self, variable):
        """Updates the labels when Y axis has been updated.

        Args:
            variable: the selected variable
        """
        self._lines[self._current_y_index][0].setText(f"{variable}")
        self._update_range_labels()
