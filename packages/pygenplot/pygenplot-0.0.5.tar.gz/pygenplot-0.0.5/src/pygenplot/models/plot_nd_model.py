from typing import Any, Dict, List, Tuple

import numpy as np

from qtpy import QtCore

from matplotlib import colormaps
from matplotlib.backends.backend_qt import FigureCanvasQT
from matplotlib.colors import LogNorm, Normalize, SymLogNorm
from matplotlib.figure import Figure
from matplotlib.image import AxesImage

from ..data.units import UnitError, UnitsManager
from ..kernel.logger import log


class PlotNDModelError(Exception):
    pass


class PlotNDModel(QtCore.QObject):

    data_axis_changed = QtCore.Signal()

    radial_integration_artists_activated = QtCore.Signal(bool)

    roi_artists_activated = QtCore.Signal(bool)

    slice_artists_activated = QtCore.Signal(bool)

    model_updated = QtCore.Signal()

    x_axis_updated = QtCore.Signal(str)

    y_axis_updated = QtCore.Signal(str)

    aspects = ["auto", "equal"]

    cmaps = sorted(colormaps(), key=lambda v: v.lower())

    interpolations = [
        "none",
        "nearest",
        "bilinear",
        "bicubic",
        "spline16",
        "spline36",
        "hanning",
        "hamming",
        "hermite",
        "kaiser",
        "quadric",
        "catrom",
        "gaussian",
        "bessel",
        "mitchell",
        "sinc",
        "lanczos",
    ]

    normalizers = ["none", "linear", "log", "symlog"]

    def __init__(self, figure: Figure, *args, **kwargs):
        """Constructor.

        Args:
            figure: the figure that will display slices of the ND model
        """
        super(PlotNDModel, self).__init__(*args, **kwargs)

        self._figure = figure

        self._interpolation = "nearest"

        self._show_colorbar = True

        self._aspect = "auto"

        self._cmap = "viridis"

        self._colorbar = None

        self._norm = "none"

        self._x_index = None
        self._y_index = None

        self._transpose = False

        self._axis_info = None

        self._axis_current_units = None

        self._axis_conversion_factors = None

        self._data_info = None

        self._data_current_unit = None

        self._data_conversion_factor = 1.0

    def _plot(self):
        """Plots a slice of the ND data."""
        summed_dimensions = tuple([i for i, s in enumerate(self._slices) if s != slice(None)])
        try:
            data = np.sum(self._data_info["data"][self._slices], axis=summed_dimensions)
        except IndexError:
            raise PlotNDModelError("Invalid slices indices")

        data = np.squeeze(data)
        if data.ndim != 2:
            raise PlotNDModelError("Ill-formed data")

        if self._transpose:
            data = data.T

        self._figure.axes.clear()
        self._image = self._figure.axes[0].imshow(data.T, interpolation=self._interpolation, origin="lower",
                                                  cmap=self._cmap)

        self.update_extent()

        self.set_aspect(self._aspect)
        self.set_x_axis_label(self._axis_info[self._x_index]["variable"])
        self.set_y_axis_label(self._axis_info[self._y_index]["variable"])
        self.set_norm(self._norm)
        self.update_colorbar()

    def _set_slices(self, slices: Tuple[slice], transpose: bool) -> bool:
        """Sets the slices of the ND data.

        Args:
            slices: a tuple of slices indicating how the data should be sliced along each dimension
            transpose: whether the slices should be transposed

        Returns:
            whether the data axis changed
        """
        if len(slices) != self._data_info["dimension"]:
            raise PlotNDModelError("Invalid slices dimension")

        try:
            x_index, y_index = [i for i, s in enumerate(slices) if s == slice(None)]
        except (TypeError, ValueError):
            raise PlotNDModelError("Invalid number of selected dimensions")
        else:
            data_axis_changed = ((self._x_index is not None and x_index != self._x_index) or
                                 (self._y_index is not None and y_index != self._y_index))

            self._x_index, self._y_index = x_index, y_index

        self._transpose = transpose

        if self._transpose:
            self._x_index, self._y_index = self._y_index, self._x_index

        self._slices = tuple(slices)

        return data_axis_changed

    def activate_radial_integration_artists(self):
        """Activates the radial integration related artists."""
        self.radial_integration_artists_activated.emit(True)
        self.roi_artists_activated.emit(False)
        self.slice_artists_activated.emit(False)

    def activate_roi_artists(self):
        """Activates the roi related artists."""
        self.radial_integration_artists_activated.emit(False)
        self.roi_artists_activated.emit(True)
        self.slice_artists_activated.emit(False)

    def activate_slice_artists(self):
        """Activate the slice artists."""
        self.radial_integration_artists_activated.emit(False)
        self.roi_artists_activated.emit(False)
        self.slice_artists_activated.emit(True)

    def add_data(self, axis_info: List[Dict[str, Any]], data_info: Dict[str, Any]):
        """Add some data to the model.

        Args:
            axis_info: the info about the axis
            data_info: the info about the dataset
        """
        self._axis_info = axis_info
        if len(self._axis_info) != data_info["dimension"]:
            raise PlotNDModelError("Axis inconsistent with the data")

        try:
            self._axis_current_units = [axis["units"] for axis in self._axis_info]
        except KeyError:
            raise PlotNDModelError("No units defined in axis")

        try:
            _ = [UnitsManager.measure(1.0, unit, equivalent=True) for unit in self._axis_current_units]
        except UnitError as e:
            raise PlotNDModelError(str(e))

        self._axis_conversion_factors = [1.0] * len(self._axis_info)

        self._data_info = data_info
        try:
            self._data_current_unit = self._data_info["units"]
        except KeyError:
            raise PlotNDModelError("No units defined in data")

        try:
            _ = UnitsManager.measure(1.0, self._data_current_unit, equivalent=True)
        except UnitError as e:
            raise PlotNDModelError(str(e))

        self._data_conversion_factor = 1.0

        slices = [slice(None), slice(None)]
        for info in axis_info[2:]:
            slices.append(slice(0, info["shape"][0], 1))

        slices = tuple(slices)

        self.update_model(slices, self._transpose)

    @property
    def canvas(self) -> FigureCanvasQT:
        """Returns the canvas stored by the figure."""
        return self._figure.canvas

    @property
    def figure(self) -> Figure:
        """Returns the figure underlying the ND model.

        Returns:
            the figure
        """
        return self._figure

    @property
    def file(self) -> str:
        """Returns the name of the file underlying the plot.

        Returns:
            the filename
        """
        return self._data_info["file"]

    def get_aspect(self) -> str:
        """Returns the aspect of the image.

        Returns:
            the aspect of the image
        """
        return self._aspect

    def get_axis_info(self) -> List[Dict[str, Any]]:
        """ Returns the axis info.
        
        Returns:
            the axis info
        """
        return self._axis_info

    def get_axis_conversion_factors(self) -> List[float]:
        """Returns the axis conversion factors.

        Returns:
            the axis conversion factors
        """
        return self._axis_conversion_factors

    def get_axis_current_data(self) -> List[np.ndarray]:
        """Returns the axis data converted to the current unit.

        Returns:
            the axis current data
        """
        return [
            axis_info["data"] * conversion_factor for axis_info, conversion_factor in zip(self._axis_info,
                                                                                          self._axis_conversion_factors)
        ]

    def get_axis_current_units(self) -> List[str]:
        """Returns the axis current units.

        Returns:
            the axis current units
        """
        return self._axis_current_units

    def get_axis_variables(self) -> List[str]:
        """Returns the axis names.

        Returns:
            the axis names
        """
        return [axis_info["variable"] for axis_info in self._axis_info]

    def get_canvas(self) -> FigureCanvasQT:
        """Returns the canvas stored by the figure."""
        return self._figure.canvas

    def get_cmap(self) -> str:
        """Returns the current color map.

        Returns:
            the color map
        """
        return self._cmap

    def get_data(self) -> np.ndarray:
        """Returns the image data.

        Returns:
            the image data
        """
        return self._image.get_array()

    def get_data_current_unit(self) -> str:
        """Returns the current unit of the ND data.

        Returns:
            the current unit of the ND data
        """
        return self._data_current_unit

    def get_data_range(self) -> Tuple[float, float]:
        """Returns the range of the image.

        Returns:
            the range of the image
        """
        z_data = self._image.get_array()
        return z_data.min(), z_data.max()

    def get_data_shape(self) -> Tuple[int]:
        """Returns the shape of the ND data.

        Returns:
            the shape of the ND data
        """
        return self._data_info["shape"]

    def get_data_variable(self) -> str:
        """Returns the name of the ND data.

        Returns:
            the name of the ND data
        """
        return self._data_info["variable"]

    def get_dataset_info(self) -> List[Dict[str, Any]]:
        """Returns the dataset info.

        Returns:
            the dataset info
        """
        return [self._data_info]

    def get_extent(self) -> Tuple[float, float, float, float]:
        """Returns the extent of the image.

        Returns:
            the extent of the image
        """
        xmin = self._axis_info[self._x_index]["data"][0] * self._axis_conversion_factors[self._x_index]
        xmax = self._axis_info[self._x_index]["data"][-1] * self._axis_conversion_factors[self._x_index]
        ymin = self._axis_info[self._y_index]["data"][0] * self._axis_conversion_factors[self._y_index]
        ymax = self._axis_info[self._y_index]["data"][-1] * self._axis_conversion_factors[self._y_index]
        return xmin, xmax, ymin, ymax

    def get_figure_title(self) -> str:
        """Returns the figure title.

        Returns:
            the figure title
        """
        suptitle = self._figure._suptitle
        return suptitle.get_text() if suptitle is not None else ""

    def get_horizontal_slice_info(self, index: int) -> Tuple[Dict[str, Any],Dict[str, Any]]:
        """Returns the information about a slice through Y axis.

        Args:
            index: the Y index of the horizontal slice

        Returns:
            the X and Y information about the slice
        """
        y_data = self._axis_info[self._y_index]["data"] * self._axis_conversion_factors[self._y_index]
        y_value = np.format_float_positional(y_data[index], precision=3, unique=False, fractional=False, trim="k")

        x_data = self._axis_info[self._x_index]["data"] * self._axis_conversion_factors[self._x_index]

        z_data = self._image.get_array()
        try:
            y_slice = z_data[index, :]
            y_variable = f"{self._data_info['variable']} ({self._axis_info[self._y_index]['variable']}={y_value})"
        except IndexError:
            raise PlotNDModelError("Invalid Y slice")

        x_data_info = {
            "file": self._data_info["file"],
            "variable": self._axis_info[self._x_index]["variable"],
            "dimension":1,
            "plottable": True,
            "data": x_data,
            "units": self._axis_current_units[self._x_index],
            "axis": ["index"],
        }

        y_data_info = {
            "file": self._data_info["file"],
            "variable": y_variable,
            "dimension":1,
            "plottable": True,
            "data": y_slice,
            "units": self._data_current_unit,
            "axis": [self._axis_info[self._x_index]["variable"]],
        }

        return x_data_info, y_data_info

    def get_interpolation(self) -> str:
        """Returns the interpolation of the image.

        Returns:
            the interpolation of the image
        """
        return self._interpolation

    def get_n_dimensions(self) -> int:
        """Returns the number of dimensions of the ND data.

        Returns:
            the number of dimensions of the image
        """
        return self._data_info["dimension"]

    def get_norm(self) -> str:
        """Returns the norm used for normalizing the image.

        Returns:
            the norm
        """
        return self._norm

    def get_plot_title(self) -> str:
        """Returns the plot title.

        Returns:
            the plot title
        """
        return self._figure.axes[0].get_title()

    def get_show_colorbar(self) -> bool:
        """Returns whether the color bar is showed.

        Returns:
            whether the colorbar is shown
        """
        return self._show_colorbar

    def get_transpose(self) -> bool:
        """Returns whether the image should be transposed.

        Returns:
            whether the image should be transposed
        """
        return self._transpose

    def get_vertical_slice_info(self, index: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Returns the information about a slice through X axis.

        Args:
            index: the X index of the vertical slice

        Returns:
            the X and Y information about the slice
        """
        x_data = self._axis_info[self._x_index]["data"] * self._axis_conversion_factors[self._x_index]
        x_value = np.format_float_positional(x_data[index], precision=3, unique=False, fractional=False, trim="k")

        y_data = self._axis_info[self._y_index]["data"] * self._axis_conversion_factors[self._y_index]

        z_data = self._image.get_array()
        try:
            x_slice = z_data[:, index]
            y_variable = f"{self._data_info['variable']} ({self._axis_info[self._x_index]['variable']}={x_value})"
        except IndexError:
            raise PlotNDModelError("Invalid X slice")

        x_data_info = {
            "file": self._data_info["file"],
            "variable": self._axis_info[self._y_index]["variable"],
            "dimension":1,
            "plottable": True,
            "data": y_data,
            "units": self._axis_current_units[self._y_index],
            "axis": ["index"],
        }

        y_data_info = {
            "file": self._data_info["file"],
            "variable": y_variable,
            "dimension":1,
            "plottable": True,
            "data": x_slice,
            "units": self._data_current_unit,
            "axis": [self._axis_info[self._y_index]["variable"]],
        }

        return x_data_info, y_data_info

    def get_x_axis_current_info(self) -> Dict[str, Any]:
        """Returns the information about the current X axis.

        Returns:
            the X axis information
        """
        info = {"variable": self._axis_info[self._x_index]["variable"],
                "plottable": True,
                "shape": self._axis_info[self._x_index]["data"].shape,
                "units": self._axis_current_units[self._x_index],
                "data": self._axis_info[self._x_index]["data"] * self._axis_conversion_factors[self._x_index]}
        return info

    def get_x_axis_current_unit(self) -> str:
        """Returns the X axis current unit.

        Returns:
            the X axis current unit
        """
        return self._axis_current_units[self._x_index]

    def get_x_axis_data(self) -> np.ndarray:
        """Returns the X axis data converted to X axis unit.

        Returns:
            the current X axis data
        """
        return self._axis_info[self._x_index]["data"] * self._axis_conversion_factors[self._x_index]

    def get_x_index(self) -> int:
        """Returns the index of the current X axis.

        Returns:
            the index of the current X axis
        """
        return self._x_index

    def get_x_axis_variable(self) -> str:
        """Returns the X axis name.

        Returns:
            the X axis name
        """
        return self._axis_info[self._x_index]["variable"]

    def get_y_axis_current_info(self) -> Dict[str, Any]:
        """Returns the information about the current Y axis.

        Returns:
            the information about Y axis
        """
        info = {"variable": self._axis_info[self._y_index]["variable"],
                "plottable": True,
                "shape": self._axis_info[self._y_index]["data"].shape,
                "units": self._axis_current_units[self._y_index],
                "data": self._axis_info[self._y_index]["data"] * self._axis_conversion_factors[self._y_index]}
        return info

    def get_y_axis_current_unit(self) -> str:
        """Returns the Y axis current unit.

        Returns:
            the Y axis current unit
        """
        return self._axis_current_units[self._y_index]

    def get_y_axis_data(self) -> np.ndarray:
        """Returns the Y axis data converted to Y axis unit.

        Returns:
            the current Y axis data
        """
        return self._axis_info[self._y_index]["data"] * self._axis_conversion_factors[self._y_index]

    def get_y_index(self) -> int:
        """Returns the index of the current Y axis.

        Returns:
            the index of the current Y axis
        """
        return self._y_index

    def get_y_axis_variable(self) -> str:
        """Returns the Y axis name.

        Returns:
            the Y axis name
        """
        return self._axis_info[self._y_index]["variable"]

    @property
    def image(self) -> AxesImage:
        """Returns the image stored by the figure underlying the ND model.

        Returns:
            the image
        """
        return self._image

    def reset_x_axis(self, min_x: float, max_x: float, unit: str):
        """Resets the X axis from min to max values expressed in provided unit.

        Args:
            min_x: the minimum value
            max_x: the maximum value
            unit: the unit
        """
        if min_x >= max_x:
            raise PlotNDModelError("Invalid min/max values")

        unit = unit.strip()
        if not unit:
            raise PlotNDModelError("No unit provided")

        try:
            _ = UnitsManager.measure(1.0, unit, equivalent=True)
        except UnitError as e:
            raise PlotNDModelError(str(e))

        x_data = np.linspace(min_x, max_x, self._axis_info[self._x_index]["data"].size, True)

        self._axis_info[self._x_index]["data"] = x_data
        self._axis_info[self._x_index]["units"] = unit
        self._axis_current_units[self._x_index] = unit
        self._axis_conversion_factors[self._x_index] = 1.0

        self.update_extent()

        self.set_x_axis_label(self._axis_info[self._x_index]["variable"])

        self._figure.canvas.draw()

        self.model_updated.emit()

    def reset_y_axis(self, min_y: float, max_y: float, unit: str):
        """Resets the Y axis from min to max values expressed in provided unit.

        Args:
            min_y: the minimum value
            max_y: the maximum value
            unit: the unit
        """
        if min_y >= max_y:
            raise PlotNDModelError("Invalid min/max values")

        unit = unit.strip()
        if not unit:
            raise PlotNDModelError("No unit provided")

        try:
            _ = UnitsManager.measure(1.0, unit, equivalent=True)
        except UnitError as e:
            raise PlotNDModelError(str(e))

        y_data = np.linspace(min_y, max_y, self._axis_info[self._y_index]["data"].size, True)

        self._axis_info[self._y_index]["data"] = y_data
        self._axis_info[self._y_index]["units"] = unit
        self._axis_current_units[self._y_index] = unit
        self._axis_conversion_factors[self._y_index] = 1.0

        self.update_extent()

        self.set_y_axis_label(self._axis_info[self._y_index]["variable"])

        self._figure.canvas.draw()

        self.model_updated.emit()

    def set_aspect(self, aspect: str):
        """Sets the aspect of the image.

        Args:
            aspect: the aspect of the image
        """
        if aspect not in PlotNDModel.aspects:
            raise PlotNDModelError("Unknown aspect")

        self._aspect = aspect
        self._figure.axes[0].set_aspect(self._aspect)
        self._figure.canvas.draw()

    def set_cmap(self, cmap: str):
        """Sets the colormap of the image.

        Args:
            cmap: the colormap of the image
        """
        if cmap not in PlotNDModel.cmaps:
            raise PlotNDModelError("Unknown color map")
        self._cmap = cmap
        self._image.set_cmap(cmap)
        self._figure.canvas.draw()

    def set_data_current_unit(self, unit: str):
        """Sets the ND data unit.

        Args:
            unit: the ND data unit
        """
        initial_unit = self._data_info["units"]
        try:
            m = UnitsManager.measure(1.0, initial_unit, equivalent=True)
            self._data_conversion_factor = m.toval(unit)
        except UnitError:
            raise PlotNDModelError(f"Units {initial_unit} and {unit} are incompatible")
        else:
            self._data_current_unit = unit

            slices = tuple(self._slices)
            summed_dimensions = tuple([i for i, s in enumerate(self._slices) if s != slice(None)])
            try:
                data = np.sum(self._data_info["data"][slices], axis=summed_dimensions)
            except IndexError:
                raise PlotNDModelError("Invalid slices indices")

            data = np.squeeze(data)
            if data.ndim != 2:
                raise PlotNDModelError("Ill-formed data")

            scaled_data = data * self._data_conversion_factor
            if self._transpose:
                scaled_data = scaled_data.T
            self._image.set_data(scaled_data.T)
            self._image.set_clim(vmin=scaled_data.min(), vmax=scaled_data.max())
            self.set_data_label(self._data_info["variable"])
            self.update_colorbar()
            self.model_updated.emit()

    def set_data_label(self, label: str):
        """Sets the ND data label.

        Args:
            label: the new label
        """
        self._data_info["variable"] = label
        self.update_colorbar()
        self._figure.canvas.draw()

    def set_data_range(self, min_z: float, max_z: float):
        """Sets the ND data range.

        Args:
            min_z: the minimum value
            max_z: the maximum value
        """
        if min_z >= max_z:
            raise PlotNDModelError("Invalid min/max values")

        self._image.set_clim(vmin=min_z, vmax=max_z)
        self._figure.canvas.draw()

    def set_figure_title(self, title: str):
        """Sets the title of the figure.

        Args:
            title: the new title
        """
        self._figure.suptitle(title)
        self._figure.canvas.draw()

    def set_interpolation(self, interpolation: str):
        """Sets the interpolation of the image.

        Args:
            interpolation: the interpolation
        """
        if interpolation not in PlotNDModel.interpolations:
            raise PlotNDModelError("Unknown interpolation")
        self._interpolation = interpolation
        self._image.set_interpolation(interpolation)
        self._figure.canvas.draw()

    def set_norm(self, norm: str):
        """Sets the norm of the image.

        Args:
            norm: the norm
        """
        if norm not in PlotNDModel.normalizers:
            raise PlotNDModelError("Unknwon norm")

        data = self._image.get_array()
        if norm == "log" and data.min() <= 0.0:
            log("Data contains negative value", ["main", "popup"], "error")
            return

        if norm == "none":
            normalizer = Normalize(vmin=data.min(), vmax=data.max())
        elif norm == "linear":
            normalizer = Normalize(vmin=0.0, vmax=1)
        elif norm == "log":
            normalizer = LogNorm(vmin=data.min(), vmax=data.max())
        else:
            normalizer = SymLogNorm(vmin=data.min(), vmax=data.max(), linthresh=0.3, linscale=0.3)
        self._image.set_norm(normalizer)
        self._norm = norm
        self.update_colorbar()

    def set_plot_title(self, title: str):
        """Sets the title of the plot.

        Args:
            title: the new title
        """
        self._figure.axes[0].set_title(title)
        self._figure.canvas.draw()

    def set_show_colorbar(self, show_colorbar: bool):
        """Sets whether the colorbar should be showe.

        Args:
            show_colorbar: whether the colorbar should be shown
        """
        self._show_colorbar = show_colorbar
        self.update_colorbar()

    def set_x_axis_label(self, label: str):
        """Sets the X axis label.

        Args:
            label: the new label
        """
        self._axis_info[self._x_index]["variable"] = label
        self._figure.axes[0].set_xlabel(f"{label} ({self._axis_current_units[self._x_index]})")
        self._figure.canvas.draw()

        variable = self._axis_info[self._x_index]["variable"]
        self.x_axis_updated.emit(variable)

    def set_x_axis_unit(self, unit: str):
        """Sets the X axis unit.

        Args:
            unit: the X axis unit
        """
        initial_unit = self._axis_info[self._x_index]["units"]
        try:
            m = UnitsManager.measure(1.0, initial_unit, equivalent=True)
            self._axis_conversion_factors[self._x_index] = m.toval(unit)
        except UnitError:
            raise PlotNDModelError(f"Units {initial_unit} and {unit} are incompatible")
        else:
            self._axis_current_units[self._x_index] = unit
            self.update_extent()
            self.set_x_axis_label(self._axis_info[self._x_index]["variable"])
            self.model_updated.emit()

    def set_y_axis_label(self, label: str):
        """Sets the Y axis label.

        Args:
            label: the new label
        """
        self._axis_info[self._y_index]["variable"] = label
        self._figure.axes[0].set_ylabel(f"{label} ({self._axis_current_units[self._y_index]})")
        self._figure.canvas.draw()

        variable = self._axis_info[self._y_index]["variable"]
        self.y_axis_updated.emit(variable)

    def set_y_axis_unit(self, unit: str):
        """Sets the Y axis unit.

        Args:
            unit: the Y axis unit
        """
        initial_unit = self._axis_info[self._y_index]["units"]
        try:
            m = UnitsManager.measure(1.0, initial_unit, equivalent=True)
            self._axis_conversion_factors[self._y_index] = m.toval(unit)
        except UnitError:
            raise PlotNDModelError(f"Units {initial_unit} and {unit} are incompatible")
        else:
            self._axis_current_units[self._y_index] = unit
            self.update_extent()
            self.set_y_axis_label(self._axis_info[self._y_index]["variable"])
            self.model_updated.emit()

    @property
    def slices(self) -> Tuple[slice]:
        """Returns the slices sets for the ND model.

        Returns:
            the _slices attribute
        """
        return self._slices

    def update_colorbar(self):
        """Updates the colorbar."""
        if self._colorbar is not None:
            self._colorbar.remove()
            self._colorbar = None

        if self._show_colorbar:
            self._colorbar = self._figure.colorbar(self._image)
            self._colorbar.ax.get_yaxis().labelpad = 15
            self._colorbar.ax.set_ylabel(f"{self._data_info['variable']} ({self._data_current_unit})", rotation=270)

        self._figure.canvas.draw()

    def update_extent(self):
        """Updates the extent of the figure."""
        x_data = self.get_x_axis_data()
        dx = (x_data[1]-x_data[0])

        y_data = self.get_y_axis_data()
        dy = (y_data[1]-y_data[0])

        extent = self.get_extent()
        self._image.set_extent((extent[0]-dx/2.0, extent[1]+dx/2.0, extent[2]-dy/2.0, extent[3]+dy/2.0))
        self._figure.canvas.draw()

    def update_model(self, slices: Tuple[slice], transpose: bool):
        """Updates the model. This will produce a new image of the ND data for given slices and/or summed dimensions.

        Args:
            slices: a tuple of slices indicating how the data should be sliced along each dimension
            transpose: whether the data should be transposed
        """
        data_axis_changed = self._set_slices(slices, transpose)

        self._plot()

        if data_axis_changed:
            self.data_axis_changed.emit()
        else:
            self.model_updated.emit()

