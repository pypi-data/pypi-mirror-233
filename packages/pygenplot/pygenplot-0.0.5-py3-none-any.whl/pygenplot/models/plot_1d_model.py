import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from qtpy import QtCore, QtGui, QtWidgets

from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.markers import MarkerStyle

from ..data.units import UnitError, UnitsManager


class Plot1DModelError(Exception):
    pass


class Plot1DModel(QtCore.QAbstractListModel):
    line_styles = ["-", "--", "-.", ":", "None"]

    legend_locations = [
        "best",
        "upper right",
        "upper left",
        "lower left",
        "lower right",
        "right",
        "center left",
        "center right",
        "lower center",
        "upper center",
        "center",
    ]

    markers = list([marker for marker in MarkerStyle.markers.keys() if isinstance(marker, str)])

    scales = ["linear", "symlog", "ln", "log 10", "log 2"]

    model_cleared = QtCore.Signal()

    model_updated = QtCore.Signal()

    line_removed = QtCore.Signal(int)

    line_selected = QtCore.Signal(QtCore.QModelIndex)

    line_color_changed = QtCore.Signal(int, tuple)

    line_label_changed = QtCore.Signal(int, str)

    LineRole = QtCore.Qt.ItemDataRole.UserRole

    XDataRole = QtCore.Qt.ItemDataRole.UserRole + 1

    YDataRole = QtCore.Qt.ItemDataRole.UserRole + 2

    LineStyleRole = QtCore.Qt.ItemDataRole.UserRole + 3

    LineWidthRole = QtCore.Qt.ItemDataRole.UserRole + 4

    LineColorRole = QtCore.Qt.ItemDataRole.UserRole + 5

    MarkerStyleRole = QtCore.Qt.ItemDataRole.UserRole + 6

    DataRole = QtCore.Qt.ItemDataRole.UserRole + 7

    def __init__(self, figure: Figure, parent: Optional[QtWidgets.QWidget] = None):
        """Constructor.

        Args:
            figure: the figure that will display slices of the ND model
            parent: the parent of the model
        """
        super(Plot1DModel, self).__init__(parent)

        self._figure = figure

        self._selected_line = None

        self._show_legend = True
        self._legend_location = "best"
        self._legend_frameon = True
        self._legend_shadow = True
        self._legend_fancybox = False

        self._show_grid = False
        self._grid_line_style = "-"
        self._grid_width = 1.0
        self._grid_color = (0, 0, 0)

        self._x_label = ""
        self._y_label = ""

        self._x_scale = "linear"
        self._y_scale = "linear"

        self._x_conversion_factor = 1.0
        self._y_conversion_factor = 1.0

        self._line_splitter_maximum_offset = 0.0
        self._line_splitter_factor = 0.0

        self._lines = []

    def _reset_x_axis_info(self, x_axis_info: Dict[str, Any]):
        """Resets the X axis info.

        Args:
            x_axis_info: the new X axis info
        """
        self._x_axis_info = x_axis_info
        self._x_conversion_factor = 1.0
        self._x_scale = "linear"
        self.set_x_axis_label(f"{self._x_axis_info['variable']}")

    def _reset_y_axis_info(self, y_axis_info: Dict[str, Any]):
        """Resets the X axis info.

        Args:
            x_axis_info: the new X axis info
        """
        self._y_axis_info = y_axis_info
        self._y_conversion_factor = 1.0
        self._y_scale = "linear"
        self.set_y_axis_label(f"{self._y_axis_info['variable']}")

    def add_line(self, x_data_info: Dict[str, Any], y_data_info: Dict[str, Any]):
        """Adds a new line to the model.

        Args:
            x_data_info (list): the information about the X of the line
            y_data_info (dict): the information about the Y of the line

        """
        if not x_data_info["plottable"]:
            raise Plot1DModelError(f"The dataset is not plottable: {x_data_info['status']}")

        if not y_data_info["plottable"]:
            raise Plot1DModelError(f"The dataset is not plottable: {y_data_info['status']}")

        axis = y_data_info["axis"]
        if len(axis) != 1:
            raise Plot1DModelError("Can not add line: incompatible number of X axis")
        else:
            if axis[0] != x_data_info["variable"]:
                raise Plot1DModelError("Can not add line: incompatible X axis")

        if not self._lines:
            self._reset_x_axis_info(x_data_info)
            self._reset_y_axis_info(y_data_info)

        y_variable = f"{y_data_info['variable']}_{os.path.basename(y_data_info['file'])}"
        line_names = [line.get_label() for line in self._lines]
        comp = 1
        while y_variable in line_names:
            y_variable = f"{y_data_info['variable']}_{os.path.basename(y_data_info['file'])}_{comp}"
            comp += 1

        if x_data_info["data"].ndim != 1 and y_data_info["data"].ndim != 1:
            raise Plot1DModelError("Invalid dimension for X/Y data")

        if x_data_info["data"].size != y_data_info["data"].size:
            raise Plot1DModelError("Incompatible size between X and Y data")

        # The unit of the line to add must be compatible with the internal one
        try:
            m = UnitsManager.measure(1.0, self._x_axis_info["units"], equivalent=True)
            x_conversion_factor = m.toval(x_data_info["units"])
        except UnitError:
            raise Plot1DModelError("Can not add line: incompatible X unit")

        try:
            m = UnitsManager.measure(1.0, self._y_axis_info["units"], equivalent=True)
            y_conversion_factor = m.toval(y_data_info["units"])
        except UnitError:
            raise Plot1DModelError("Can not add line: incompatible Y unit")

        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        line = self._figure.axes[0].plot(x_data_info["data"] * x_conversion_factor, y_data_info["data"] * y_conversion_factor, picker=3)[
            0
        ]
        line.set_label(y_variable)
        self._lines.append(line)
        self.endInsertRows()

        self.update_legend()
        self.adjust_axes()

    def adjust_axes(self) -> Tuple[float, float, float, float]:
        """Adjusts the axes of the figure such that they match the global min/max values of the
        X and Y axis respectively."""
        x_min = self.get_x_axis_min_value()
        x_max = self.get_x_axis_max_value()
        self._figure.axes[0].set_xlim([x_min, x_max])

        y_min = self.get_y_axis_min_value()
        y_max = self.get_y_axis_max_value()
        self._figure.axes[0].set_ylim([y_min, y_max])

        self._figure.canvas.draw()

        return x_min, x_max, y_min, y_max

    def clear(self):
        """Clears the figure."""
        self._lines.clear()
        self._figure.axes[0].clear()
        self._figure.canvas.draw()
        self.model_cleared.emit()
        self.layoutChanged.emit()

    def data(self, index: QtCore.QModelIndex = QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        """Returns the data for a given index and role.

        Args:
            index: the index
            role: the role

        Returns:
            the data
        """
        row = index.row()
        try:
            line = self._lines[row]
        except IndexError:
            return None

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return line.get_label()

        elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
            matplotlib_color = line.get_color()
            r, g, b = 1, 0, 0
            try:
                color = matplotlib_color.lstrip("#")
                r, g, b = tuple(int(color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
            except AttributeError:
                r, g, b = matplotlib_color
            finally:
                color = QtGui.QColor( r * 255,  g * 255,  b * 255)
            return color

        elif role == Plot1DModel.LineRole:
            return line

        elif role == Plot1DModel.XDataRole:
            return line.get_xdata()

        elif role == Plot1DModel.YDataRole:
            return line.get_ydata()

        else:
            return QtCore.QVariant()

    def flags(self, index: QtCore.QModelIndex) -> int:
        """Returns the flags of a given index.

        Args:
            index: the index

        Returns:
            the flag
        """
        return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEditable)

    def get_figure_title(self) -> str:
        """Returns the figure title.

        Returns:
            str: the figure title
        """
        suptitle = self._figure._suptitle
        return suptitle.get_text() if suptitle is not None else ""

    def get_grid_color(self) -> Tuple[float, float, float]:
        """Returns the grid color. The color is expressed as 3-tuple in matplotlib convention ([0,1])

        Returns:
            the grid color
        """
        return self._grid_color

    def get_grid_line_style(self) -> str:
        """Returns the grid style.

        Returns:
            the grid style
        """
        return self._grid_line_style

    def get_grid_width(self) -> float:
        """Returns the grid width.

        Returns:
            the grid width
        """
        return self._grid_width

    def get_legend_fancybox(self) -> bool:
        """Returns whether the legend fancybox should be showed.

        Returns:
            whether the legend fancybox should be showed
        """
        return self._legend_fancybox

    def get_legend_frameon(self) -> bool:
        """Returns whether the legend frame should be showed.

        Returns:
            whether the legend frame should be showed
        """
        return self._legend_frameon

    def get_legend_location(self) -> str:
        """Returns the legend location.

        Returns:
            the legend location
        """
        return self._legend_location

    def get_legend_shadow(self) -> bool:
        """Returns whether the legend shadow should be showed.

        Returns:
            whether the legend shadow should be showed
        """
        return self._legend_shadow

    def get_line_splitter_factor(self) -> float:
        """Returns the line splitter factor.

        Returns:
            the line splitter factor
        """
        return self._line_splitter_factor

    def get_line_splitter_maximum_offset(self) -> float:
        """Returns the line splitter maximum offset.

        Returns:
            the line splitter maximum offset
        """
        return self._line_splitter_maximum_offset

    def get_line_full_names(self) -> List[str]:
        """Returns the names of the lines.

        Returns:
            the names of the lines
        """
        return [f"{line.get_label()} ({self._y_axis_info['units']})" for line in self._lines]

    def get_line_names(self) -> List[str]:
        """Returns the line names.

        Returns:
            the line names
        """
        return [line.get_label() for line in self._lines]

    def get_plot_title(self) -> str:
        """Returns the plot title.

        Returns:
            the plot title
        """
        return self._figure.axes[0].get_title()

    def get_selected_line_index(self) -> Optional[int]:
        """Returns the selected line index. None if no line is selected.

        Returns:
            the selected line index.
        """
        if self._selected_line is None:
            return None

        for i, line in enumerate(self._lines):
            if line == self._selected_line:
                return i
        else:
            return None

    def get_show_grid(self) -> bool:
        """Returns whether the grid should be showed.

        Returns:
            whether the grid should be showed
        """
        return self._show_grid

    def get_show_legend(self) -> bool:
        """Returns whether the legend should be showed.

        Returns:
            whether the legend should be showed
        """
        return self._show_legend
    
    def get_axis_info(self) -> Optional[List[Dict[str, Any]]]:
        """Returns the axis info.

        Returns:
            the axis info
        """
        if not self._lines:
            return None

        x_axis_info = []
        for line in self._lines:
            info = self._x_axis_info
            info["data"] = line.get_xdata()
            x_axis_info.append(info)

        return x_axis_info

    def get_dataset_info(self) -> List[Dict[str, Any]]:
        """Returns the dataset info.

        Returns:
            the dataset info
        """
        dataset_info = []
        for line in self._lines:
            info = self._y_axis_info
            info["data"] = line.get_ydata()
            dataset_info.append(info)
            
        return dataset_info

    def get_x_axis_current_unit(self) -> str:
        """Returns the X axis current unit.

        Returns:
            the X axis current unit
        """
        return self._x_axis_info["units"]

    def get_x_axis_full_name(self) -> str:
        """Returns the X axis full name
        
        Returns:
            the X axis full name
        """
        return f"{self._x_label} ({self._x_axis_info['units']})"

    def get_x_axis_label(self) -> str:
        """Returns the X axis label.

        Returns:
            the X axis label
        """
        return self._x_label

    def get_x_axis_max_value(self) -> float:
        """Returns the global maximum of the X data of all lines.

        Returns:
            the global maximum
        """
        max_value = 0.0
        try:
            max_value = max([line.get_xdata().max() for line in self._lines])
        except ValueError:
            pass
        finally:
            return max_value

    def get_x_axis_min_value(self) -> float:
        """Returns the global minimum of the X data of all lines.

        Returns:
            the global minimum
        """
        min_value = 0.0
        try:
            min_value = min([line.get_xdata().min() for line in self._lines])
        except ValueError:
            pass
        finally:
            return min_value

    def get_x_axis_scale(self) -> str:
        """Returns the X axis scale.

        Returns:
            the X axis scale
        """
        return self._x_scale

    def get_x_axis_variable(self) -> str:
        """Returns the X axis underlying variable name.

        Returns:
            the X axis variable name
        """
        return self._x_axis_info["variable"]

    def get_y_axis_current_unit(self) -> str:
        """Returns the Y axis current unit.

        Returns:
            the Y axis current unit
        """
        return self._y_axis_info["units"]

    def get_y_axis_data(self) -> List[np.ndarray]:
        """Returns the Y axis data for all lines converted to the current Y axis unit.

        Returns:
            list of 1D-array: all the Y axis data
        """
        return [line.get_ydata() for line in self._lines]

    def get_y_axis_label(self) -> str:
        """Returns the label of the Y axis.

        Returns:
            the label of the Y axis
        """
        return self._y_label

    def get_y_axis_max_value(self) -> float:
        """Returns the global maximum of the Y data of all lines.

        Returns:
            the global maximum
        """
        max_value = 0.0
        try:
            max_value = max([line.get_ydata().max() for line in self._lines])
        except ValueError:
            pass
        finally:
            return max_value

    def get_y_axis_min_value(self) -> float:
        """Returns the global minimum of the Y data of all lines.

        Returns:
            the global minimum
        """
        min_value = 0.0
        try:
            min_value = min([line.get_ydata().min() for line in self._lines])
        except ValueError:
            pass
        finally:
            return min_value

    def get_y_axis_scale(self) -> str:
        """Returns the Y axis scale.

        Returns:
            the Y axis scale
        """
        return self._y_scale

    def removeRow(self, row: int, parent:QtCore.QModelIndex = QtCore.QModelIndex, *args, **kwargs) -> bool:
        """Removes a row from the model.

        Args:
            row: the index of the row to be removed
            parent: the parent

        Returns:
            whether the removal was successful
        """
        if row < 0 or row >= self.rowCount():
            return False

        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        self._lines[row].remove()
        del self._lines[row]
        self.endRemoveRows()

        if not self._lines:
            self._figure.axes[0].set_prop_cycle(None)
            self._figure.canvas.draw()
        else:
            self.adjust_axes()

        self.update_legend()

        self.model_updated.emit()

        self.line_removed.emit(row)

        return True

    def reset_axes(self):
        """Resets the axes."""
        self.unselect_line()
        self._figure.axes[0].clear()
        self._lines = []
        self._figure.canvas.draw()

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex(), *args, **kwargs) -> int:
        """Returns the number of lines stored in the model.

        Args:
            parent: the parent index

        Returns:
            the number of lines stored in the model
        """
        return len(self._lines)

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = QtCore.Qt.DisplayRole) -> bool:
        """Sets the data of the model.

        Args:
            index: the index
            value: the value
            role: the role

        Returns:
            whether setting the data was successful
        """
        if not index.isValid():
            return False

        row = index.row()
        if role == QtCore.Qt.ItemDataRole.EditRole:
            self._lines[row].set_label(value)
            self.update_legend()
            self.line_label_changed.emit(row, value)
            self.model_updated.emit()
            return True
        elif role == Plot1DModel.LineStyleRole:
            line = self._lines[row]
            if value not in Plot1DModel.line_styles:
                raise Plot1DModelError("Invalid line style")
            line.set_linestyle(value)
            self.update_legend()
            return True
        elif role == Plot1DModel.LineWidthRole:
            line = self._lines[row]
            line.set_linewidth(value)
            self.update_legend()
            return True
        elif role == Plot1DModel.LineColorRole:
            line = self._lines[row]
            line.set_color(value)
            self.line_color_changed.emit(row, value)
            self.update_legend()
            return True
        elif role == Plot1DModel.MarkerStyleRole:
            line = self._lines[row]
            if value not in Plot1DModel.markers:
                raise Plot1DModelError("Invalid marker")
            line.set_marker(value)
            self.update_legend()
            return True
        elif role == Plot1DModel.DataRole:
            x_data_info, y_data_info = value
            line = self._lines[row]
            line.set_xdata(x_data_info["data"])
            line.set_ydata(y_data_info["data"])
            self.adjust_axes()
            self.update_legend()
            self.layoutChanged.emit()
            return True
        return False

    def select_line(self, line: Line2D):
        """Selects a line of the figure.

        Args:
            line: the line to select
        """
        if line not in self._lines:
            return QtCore.QModelIndex()

        # If there was a previously selected line, set back its alpha value to 1.0
        if self._selected_line is not None:
            self._selected_line.set_alpha(1.0)

        self._selected_line = line
        self._selected_line.set_alpha(0.4)
        self._figure.canvas.draw()

        index = self.index(self._lines.index(line), 0)

        self.update_legend()

        self.line_selected.emit(index)

    def set_figure_title(self, title: str):
        """Sets the figure title.

        Args:
            title: the new title
        """
        self._figure.suptitle(title)
        self._figure.canvas.draw()

    def set_grid_color(self, color: Tuple[float, float, float]):
        """Sets the grid color. The color must be set in the matplotlib RGB convention i.e. a 3-tuple of floats
        between 0 and 1.

        Args:
            color: the grid color
        """
        self._grid_color = color
        self.update_grid()

    def set_grid_line_style(self, style: str):
        """Sets the grid style.

        Args:
            style: the grid style
        """
        if style not in Plot1DModel.line_styles:
            raise Plot1DModelError("Invalid style")
        self._grid_line_style = style
        self.update_grid()

    def set_grid_width(self, width: float):
        """Sets the grid width.

        Args:
            width: the grid width
        """
        self._grid_width = width
        self.update_grid()

    def set_legend_fancybox(self, state: bool):
        """Sets whether the legend fancybox should be shown.

        Args:
            state: whether the legend fancybox should be shown
        """
        self._legend_fancybox = state
        self.update_legend()

    def set_legend_frameon(self, state: bool):
        """Sets whether the legend frame should be shown.

        Args:
            state: whether the legend frame should be shown
        """
        self._legend_frameon = state
        self.update_legend()

    def set_legend_location(self, location: str):
        """Sets the legend location.

        Args:
            location: the legend location
        """
        if location not in Plot1DModel.legend_locations:
            raise Plot1DModelError("Invalid location")
        self._legend_location = location
        self.update_legend()

    def set_legend_shadow(self, state: bool):
        """Sets whether the legend shadow should be shown.

        Args:
            state: whether the legend shadow should be shown
        """
        self._legend_shadow = state
        self.update_legend()

    def set_line_splitter_factor(self, factor: float):
        """Sets the line splitter factor.

        Args:
            factor: the line splitter factor
        """
        self._line_splitter_factor = factor
        self.split_lines()

    def set_line_splitter_maximum_offset(self, offset: float):
        """Sets the line splitter maximum offset.

        Args:
            offset: the line splitter maximum offset
        """
        self._line_splitter_maximum_offset = offset
        self.split_lines()

    def set_plot_title(self, title: str):
        """Sets the plot title.

        Args:
            title: the new title
        """
        self._figure.axes[0].set_title(title)
        self._figure.canvas.draw()

    def set_show_grid(self, state: bool):
        """Sets whether the grid should be shown.

        Args:
            state: whether the grid should be shown
        """
        self._show_grid = state
        self.update_grid()

    def set_show_legend(self, state: bool):
        """Sets whether the legend should be shown.

        Args:
            state: whether the legend should be shown
        """
        self._show_legend = state
        self.update_legend()

    def set_x_axis_label(self, label: str):
        """Sets the X axis label.

        Args:
            label: the X axis label
        """
        self._x_label = label
        self._figure.axes[0].set_xlabel(f"{self._x_label} ({self._x_axis_info['units']})")
        self._figure.canvas.draw()
        self.model_updated.emit()

    def set_x_axis_range(self, x_min: float, x_max: float):
        """Sets the X axis range.

        Args:
            x_min: the minimum value
            x_max: the maximum value
        """
        if x_min >= x_max:
            raise Plot1DModelError("Invalid min/max values")

        self._figure.axes[0].set_xlim([x_min, x_max])
        self._figure.canvas.draw()

    def set_x_axis_scale(self, scale: str):
        """Sets the X axis scale.

        Args:
            scale: the X axis scale
        """
        if scale not in Plot1DModel.scales:
            raise Plot1DModelError("Invalid X axis scale")

        self._x_scale = scale
        if scale == "linear":
            self._figure.axes[0].set_xscale("linear")
        elif scale == "symlog":
            self._figure.axes[0].set_xscale("symlog")
        elif scale == "ln":
            self._figure.axes[0].set_xscale("log", base=np.exp(1))
        elif scale == "log 10":
            self._figure.axes[0].set_xscale("log", base=10)
        elif scale == "log 2":
            self._figure.axes[0].set_xscale("log", base=2)
        self._figure.canvas.draw()

    def set_x_axis_unit(self, x_unit: str):
        """Sets the X axis current unit.

        Args:
            x_unit: the X axis unit
        """
        try:
            m = UnitsManager.measure(1.0, self._x_axis_info["units"], equivalent=True)
            x_conversion_factor = m.toval(x_unit)
        except UnitError:
            raise Plot1DModelError(f"Units {self._x_axis_info['units']} and {x_unit} are incompatible")
        else:
            self._x_axis_info["units"] = x_unit
            self._x_conversion_factor = x_conversion_factor
            for _, line in self._lines:
                line.set_xdata(line.get_xdata() * self._x_conversion_factor)
            self.set_x_axis_label(self._x_label)
            self.adjust_axes()
            self.model_updated.emit()

    def set_y_axis_label(self, label: str):
        """Sets the Y axis label.

        Args:
            label: the Y axis label
        """
        self._y_label = label
        self._figure.axes[0].set_ylabel(f"({self._y_axis_info['units']})")
        self._figure.canvas.draw()

    def set_y_axis_range(self, y_min: float, y_max: float):
        """Sets the Y axis range.

        Args:
            y_min: the minimum value
            y_max: the maximum value
        """
        if y_min >= y_max:
            raise Plot1DModelError("Invalid min/max values")
        self._figure.axes[0].set_ylim([y_min, y_max])
        self._figure.canvas.draw()

    def set_y_axis_scale(self, scale: str):
        """Sets the Y axis scale.

        Args:
            scale: the Y axis scale
        """
        if scale not in Plot1DModel.scales:
            raise Plot1DModelError("Invalid Y axis scale")
        self._y_scale = scale
        if scale == "linear":
            self._figure.axes[0].set_yscale("linear")
        elif scale == "symlog":
            self._figure.axes[0].set_yscale("symlog")
        elif scale == "ln":
            self._figure.axes[0].set_yscale("log", base=np.exp(1))
        elif scale == "log 10":
            self._figure.axes[0].set_yscale("log", base=10)
        elif scale == "log 2":
            self._figure.axes[0].set_yscale("log", base=2)
        self.adjust_axes()

    def set_y_axis_unit(self, y_unit: str):
        """Sets the Y axis current unit.

        Args:
            y_unit: the Y axis unit
        """
        try:
            m = UnitsManager.measure(1.0, self._y_axis_info["units"], equivalent=True)
            y_conversion_factor = m.toval(y_unit)
        except UnitError:
            raise Plot1DModelError(f"Units {self._y_axis_info['units']} and {y_unit} are incompatible")
        else:
            self._y_axis_info["units"] = y_unit
            self._y_conversion_factor = y_conversion_factor
            for i, (_, line) in enumerate(self._lines):
                offset = i * self._line_splitter_maximum_offset * self._line_splitter_factor
                line.set_ydata(line.get_ydata() * self._y_conversion_factor + offset)
            self.set_y_axis_label(self._y_label)
            self.adjust_axes()
            self.model_updated.emit()

    def split_lines(self):
        """Splits the lines according the current offset."""
        if not self._lines:
            return

        for i, line in enumerate(self._lines):
            offset = i * self._line_splitter_maximum_offset * self._line_splitter_factor
            line.set_ydata(line.get_ydata() + offset)

        self.adjust_axes()
        self.model_updated.emit()

    def unselect_line(self):
        """Unselects the selected line if any."""
        if self._selected_line is not None:
            self._selected_line.set_alpha(1.0)
            self._selected_line = None
            self.update_legend()
            self._figure.canvas.draw()
            self.line_selected.emit(QtCore.QModelIndex())

    def update_grid(self):
        """Updates the grid."""
        if not self._show_grid:
            self._figure.axes[0].grid(False)
        else:
            self._figure.axes[0].grid(True, linestyle=self._grid_line_style, linewidth=self._grid_width,
                                      color=self._grid_color)
        self._figure.canvas.draw()

    def update_legend(self):
        """Updates the legend."""
        axes = self._figure.axes[0]

        legend = axes.get_legend()
        if legend is not None:
            legend.remove()

        if self._lines:
            if self._show_legend:
                line_names = [line.get_label() for line in self._lines]
                axes.legend(
                    line_names, loc=self._legend_location, frameon=self._legend_frameon, shadow=self._legend_shadow,
                    fancybox=self._legend_fancybox
                )

        self._figure.canvas.draw()
