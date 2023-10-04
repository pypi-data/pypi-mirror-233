from typing import Any, Dict, Optional, Tuple

from qtpy import QtCore

import numpy as np

from matplotlib.backend_bases import MouseEvent
from matplotlib.patches import Rectangle
from matplotlib.transforms import Bbox

from ..models.plot_nd_model import PlotNDModel


class ROI(QtCore.QObject):
    roi_added = QtCore.Signal(object)
    roi_modified = QtCore.Signal(object)
    roi_selected = QtCore.Signal(object)

    UNDER_CREATION = 1
    CREATED = 2
    SELECTED = 3

    DEFAULT_COLOR = (1, 0, 0, 0.2)
    EDGE_COLOR = (0, 0, 0, 1)

    def __init__(self, plot_nd_model: PlotNDModel):
        """Constructor.

        Args:
            plot_nd_model: the underlying ND plot model
        """
        super(ROI, self).__init__()

        self._plot_nd_model = plot_nd_model
        self._roi_rectangle = None
        self._state = self.UNDER_CREATION
        self._name = "ROI"

    @property
    def name(self) -> str:
        """Returns the name of the ROI.

        Returns:
            the name of the ROI
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of the ROI.

        Args:
            name: the name of the ROI
        """
        self._name = name

    @property
    def state(self) -> int:
        """Returns the state of the ROI.

        Returns:
            the state of the ROI
        """
        return self._state

    def contains(self, event: MouseEvent, tolerance: float = 0) -> bool:
        """Returns whether a click event falls inside the ROI within a given tolerance.

        Args:
            event: the click event
            tolerance: the tolerance

        Returns:
            whether the event falls inside the ROI
        """
        if event.xdata is None or event.ydata is None:
            # xdata or ydata can be None if the click is outside the plot
            return False
        if self._roi_rectangle:
            bbox = self._roi_rectangle.get_bbox()
            if (
                    (event.xdata >= bbox.x0 - tolerance)
                    and (event.xdata <= bbox.x1 + tolerance)
                    and (event.ydata >= bbox.y0 - tolerance)
                    and (event.ydata <= bbox.y1 + tolerance)
            ):
                return True
            else:
                return False
        else:
            return False

    def draw_roi(self, click_point: MouseEvent, release_point: MouseEvent):
        """Draws the ROI.

        Args:
            click_point: the mouse click event
            release_point: the mouse release event
        """
        x0, y0 = click_point.xdata, click_point.ydata
        x1, y1 = release_point.xdata, release_point.ydata
        if x0 == x1 or y0 == y1:
            return

        if self._state == self.UNDER_CREATION:
            self._state = self.CREATED
            self._roi_rectangle = Rectangle(
                (x0, y0), x1 - x0, y1 - y0, facecolor=self.DEFAULT_COLOR, edgecolor=self.EDGE_COLOR, fill=True,
                linewidth=1, picker=False
            )
            self._plot_nd_model.figure.axes[0].add_patch(self._roi_rectangle)
            self._plot_nd_model.get_canvas().draw()
            self._name = f"ROI from ({int(x0)},{int(y0)}) to ({int(x1) + 1},{int(y1) + 1})"
            self.roi_added.emit(self)
        elif self._state == self.SELECTED:
            self.move_roi(x0, y0, x1, y1)

    def get_bbox(self) -> Optional[Bbox]:
        """Returns the bounding box of the ROI.

        Returns:
            the bounding box
        """
        if self._roi_rectangle is None:
            return None
        else:
            return self._roi_rectangle.get_bbox()

    def get_facecolor(self) -> Tuple[float, float, float, float]:
        """Returns the facecolor of the ROI.

        Returns:
            the facecolor
        """
        if self._roi_rectangle is None:
            return self.DEFAULT_COLOR
        else:
            return self._roi_rectangle.get_facecolor()

    def get_roi_info(self) \
            -> Optional[Tuple[Tuple[Dict[str, Any], Dict[str, Any]], Tuple[Dict[str, Any], Dict[str, Any]]]]:
        """Gets the information about the horizontal and vertical plots produced by a given ROI.

        Returns:
            the information about the horizontal and vertical plots
        """
        if self._roi_rectangle is None:
            return None

        bbox = self._roi_rectangle.get_bbox()

        x0 = int(bbox.x0)
        y0 = int(bbox.y0)
        x1 = int(bbox.x1) + 1
        y1 = int(bbox.y1) + 1

        x_axis_info = self._plot_nd_model.get_x_axis_current_info()
        x_data = x_axis_info["data"]
        x_unit = x_axis_info["units"]
        x_variable = x_axis_info["variable"]
        x_data_cropped = x_data[x0:x1]

        y_axis_info = self._plot_nd_model.get_y_axis_current_info()
        y_data = y_axis_info["data"]
        y_unit = y_axis_info["units"]
        y_variable = y_axis_info["variable"]
        y_data_cropped = y_data[y0:y1]

        z_data = self._plot_nd_model.image.get_array().T
        z_data_cropped = z_data[x0:x1, y0:y1]

        horizontal_integral = np.sum(z_data_cropped, axis=0)

        vertical_integral = np.sum(z_data_cropped, axis=1)

        self._name = f"ROI from ({x0},{y0}) to ({x1},{y1})"

        dataset_info = self._plot_nd_model.get_dataset_info()
        dataset_file = dataset_info[0]["file"]
        dataset_unit = dataset_info[0]["units"]

        horizontal_plot_x_info = {
            "file": dataset_file,
            "variable": y_variable,
            "dimension": 1,
            "plottable": True,
            "data": y_data_cropped,
            "units": y_unit,
            "axis": ["index"],
        }

        horizontal_plot_y_info = {
            "file": dataset_file,
            "variable": self._name,
            "dimension": 1,
            "plottable": True,
            "data": horizontal_integral,
            "units": dataset_unit,
            "axis": [y_variable],
        }

        vertical_plot_x_info = {
            "file": dataset_file,
            "variable": x_variable,
            "dimension": 1,
            "plottable": True,
            "data": x_data_cropped,
            "units": x_unit,
            "axis": ["index"],
        }

        vertical_plot_y_info = {
            "file": dataset_file,
            "variable": self._name,
            "dimension": 1,
            "plottable": True,
            "data": vertical_integral,
            "units": dataset_unit,
            "axis": [x_variable],
        }

        return (horizontal_plot_x_info, horizontal_plot_y_info), (vertical_plot_x_info, vertical_plot_y_info)

    def move_roi(self, x_from: float, y_from: float, x_to: float, y_to: float):
        """Moves the ROI.

        Args:
            x_from: the starting X position
            y_from: the starting Y position
            x_to: the ending X position
            y_to: the ending Y position
        """
        self._roi_rectangle.set_xy((x_from, y_from))
        self._roi_rectangle.set_width(x_to - x_from)
        self._roi_rectangle.set_height(y_to - y_from)
        self._plot_nd_model.get_canvas().draw()
        self.roi_modified.emit(self)

    def remove(self):
        """Removes the ROI."""
        self._roi_rectangle.remove()
        self._plot_nd_model.get_canvas().draw()

    def select_roi(self):
        """Selects the ROI."""
        if self._state == self.CREATED:
            self._state = self.SELECTED
            self._plot_nd_model.get_canvas().draw()
            self.roi_selected.emit(self)

    def set_facecolor(self, color: Tuple[float, float, float, float]):
        """Sets the facecolor of the ROI.

        Args:
            color: the facecolor
        """
        self._roi_rectangle.set_facecolor(color)

    def set_visible(self, state: bool):
        """Sets whether the ROI should be visible.

        Args:
            state: whether the ROI should be visible
        """
        if self._roi_rectangle is not None:
            self._roi_rectangle.set_visible(state)

    def unselect_roi(self):
        """Unselects the ROI."""
        if self._state == self.SELECTED:
            self._state = self.CREATED
            self._plot_nd_model.get_canvas().draw()
