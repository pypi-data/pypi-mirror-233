import numpy as np

from typing import Any, Dict, List, Tuple

from qtpy import QtCore, QtWidgets

from matplotlib.patches import Ellipse

from ..models.plot_nd_model import PlotNDModel


class RadialIntegrationModel(QtCore.QObject):

    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the underlying ND plot model
            parent: the parent widget
        """

        super(RadialIntegrationModel,self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._integration_central_point = None

        self._integration_shells = []

        self._artists_activated = True

        self._plot_nd_model.radial_integration_artists_activated.connect(self.on_activate_artists)

    @property
    def artists_activated(self) -> bool:
        """Returns whether the artists are activated.

        Returns:
            whether the artists are activated
        """
        return self._artists_activated

    def compute_radial_profile(self, pixel_x: float, pixel_y: float, shells: np.ndarray, stretch_x: float,
                               stretch_y: float) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Computes the radial profile.

        Returns:
            the axis and dataset info of the computed radial profile
        """
        data = self._plot_nd_model.image.get_array()
        y, x = np.indices(data.shape)
        r = np.sqrt((x / stretch_x - pixel_x) ** 2 + (y / stretch_y - pixel_y) ** 2).ravel()
        weighted_hist, _ = np.histogram(r, bins=shells, density=False, weights=data.ravel())
        hist, _ = np.histogram(r, bins=shells)

        radial_profile = weighted_hist / hist

        radial_profile = np.nan_to_num(radial_profile, nan=0.0)

        axis_info = {"variable": "r",
                     "dimension": 1,
                     "plottable": True,
                     "units": "au",
                     "data": shells[:-1]}

        data_info = {"file": self._plot_nd_model.file,
                     "variable": "radial profile",
                     "dimension": 1,
                     "plottable": True,
                     "units": "au",
                     "axis": "r",
                     "data": radial_profile}

        return axis_info, data_info

    def display_integration_shells(self, pixel_x: float, pixel_y: float, shells: np.ndarray, stretch_x: float,
                                   stretch_y: float):
        """Displays the integration shells.

        Args:
            pixel_x: the X center of pixel
            pixel_y: the Y center of pixel
            shells: the shell radii
            stretch_x: the stretching factor over X
            stretch_y: the stretching factor over Y
        """
        self.unset_integration_central_point()

        figure = self._plot_nd_model.figure

        self._integration_central_point = figure.axes[0].scatter(pixel_x, pixel_y, color="r")

        self.unset_integration_shells()
        for shell in shells:
            ellipse = Ellipse((pixel_x, pixel_y), 2 * shell * stretch_x, 2 * shell * stretch_y,
                              fill=False, color="r")
            self._integration_shells.append(ellipse)
            figure.axes[0].add_patch(ellipse)

        image = self._plot_nd_model.image
        extent = self._plot_nd_model.get_extent()
        image.set_extent(extent)
        figure.canvas.draw()

    def on_activate_artists(self, state: bool):
        """Sets whether the artists should be activated.

        Args:
            whether the artists should be activated
        """
        self._artists_activated = state

        if self._integration_central_point is not None:
            self._integration_central_point.set_visible(state)

        for shell in self._integration_shells:
            shell.set_visible(state)

        self._plot_nd_model.get_canvas().draw()

    def unset_integration_central_point(self):
        """Unsets the radial integration center."""
        if self._integration_central_point is not None:
            self._integration_central_point.remove()
            self._integration_central_point = None
            self._plot_nd_model.get_canvas().draw()

    def unset_integration_shells(self):
        """Unsets the radial integration shells."""
        if self._integration_shells:
            for shell in self._integration_shells:
                shell.remove()
            self._integration_shells = []
            self._plot_nd_model.get_canvas().draw()
