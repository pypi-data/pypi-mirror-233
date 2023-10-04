from typing import Any, Dict, List

from qtpy import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from ..dialogs.cross_viewer_dialog import CrossViewerDialog
from ..dialogs.data_viewer_nd_dialog import DataViewerNDDialog
from ..dialogs.slice_viewer_dialog import SliceViewerDialog
from ..dialogs.plot_nd_axis_settings_dialog import PlotNDAxisSettingsDialog
from ..dialogs.plot_nd_general_settings_dialog import PlotNDGeneralSettingsDialog
from ..dialogs.plot_nd_image_settings_dialog import PlotNDImageSettingsDialog
from ..dialogs.radial_integration_dialog import RadialIntegrationDialog
from ..dialogs.roi_dialog import ROIDialog
from ..kernel.logger import log
from ..icons import ICONS
from ..models.plot_nd_model import PlotNDModel, PlotNDModelError


class PlotNDWidget(QtWidgets.QWidget):

    plot_sent_on_new_tab = QtCore.Signal(list,list)

    plot_sent_on_current_tab = QtCore.Signal(list,list)

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(PlotNDWidget, self).__init__(parent)

        self._general_settings_dialog = None
        self._axis_settings_dialog = None
        self._image_settings_dialog = None
        self._cross_viewer_dialog = None
        self._slice_viewer_dialog = None
        self._data_viewer_nd_dialog = None
        self._radial_integration_dialog = None
        self._roi_manager_dialog = None

        self._build()

    def _build(self):
        """Builds the widget."""
        self._figure = Figure()
        self._canvas = FigureCanvasQTAgg(self._figure)
        self._canvas.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self._canvas.customContextMenuRequested.connect(self.on_open_contextual_menu)

        self._plot_nd_model = PlotNDModel(self._figure)

        self._figure.add_subplot(111)

        from ..utils.mpl import PyGenPlotNavigationToolbar
        self._toolbar = PyGenPlotNavigationToolbar(self._canvas, self)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self._canvas, 1)
        main_layout.addWidget(self._toolbar)

        self.setLayout(main_layout)

        self._toolbar.plot_sent_on_new_tab.connect(self.on_send_plot_on_new_tab)
        self._toolbar.plot_sent_on_current_tab.connect(self.on_send_plot_on_current_tab)

    def close(self):
        """Closes the widget."""
        self.close_axis_settings_dialog()

        self.close_general_settings_dialog()

        self.close_image_settings_dialog()

        self.close_cross_viewer_dialog()

        self.close_slice_viewer_dialog()

        self.close_data_viewer_nd_dialog()

        self.close_radial_integration_dialog()

        self.close_roi_manager_dialog()

    def close_axis_settings_dialog(self):
        """Closes the axis settings dialog."""
        if self._axis_settings_dialog is not None:
            self._axis_settings_dialog.close()
            self._axis_settings_dialog = None

    def close_cross_viewer_dialog(self):
        """Closes the cross viewer dialog."""
        if self._cross_viewer_dialog is not None:
            self._cross_viewer_dialog.close()
            self._cross_viewer_dialog = None

    def close_data_viewer_nd_dialog(self):
        """Closes the data viewer dialog."""
        if self._data_viewer_nd_dialog is not None:
            self._data_viewer_nd_dialog.close()
            self._data_viewer_nd_dialog = None

    def close_general_settings_dialog(self):
        """Closes the general settings dialog."""
        if self._general_settings_dialog is not None:
            self._general_settings_dialog.close()
            self._general_settings_dialog = None

    def close_image_settings_dialog(self):
        """Closes the image settings dialog."""
        if self._image_settings_dialog is not None:
            self._image_settings_dialog.close()
            self._image_settings_dialog = None

    def close_radial_integration_dialog(self):
        """Closes the radial integration dialog."""
        if self._radial_integration_dialog is not None:
            self._radial_integration_dialog.close()
            self._radial_integration_dialog = None

    def close_roi_manager_dialog(self):
        """Closes the ROI manager dialog."""
        if self._roi_manager_dialog is not None:
            self._roi_manager_dialog.close()
            self._roi_manager_dialog = None

    def close_slice_viewer_dialog(self):
        """Closes the slice viewer dialog."""
        if self._slice_viewer_dialog is not None:
            self._slice_viewer_dialog.close()
            self._slice_viewer_dialog = None

    def on_open_contextual_menu(self, event: QtCore.QEvent):
        """Pops up the contextual menu.

        Args:
            event: the right-click event
        """
        menu = QtWidgets.QMenu(self)
        plot_settings_action = menu.addAction(ICONS["settings"], "General settings")
        plot_settings_action.triggered.connect(self.on_open_general_settings_dialog)
        axis_settings_action = menu.addAction(ICONS["axis"], "Axis settings")
        axis_settings_action.triggered.connect(self.on_open_axis_settings_dialog)
        image_settings_action = menu.addAction(ICONS["plot_2d"], "Image settings")
        image_settings_action.triggered.connect(self.on_open_image_settings_dialog)
        menu.addSeparator()
        view_data_action = menu.addAction(ICONS["data"], "View data")
        view_data_action.triggered.connect(self.on_open_view_nd_data_dialog)
        menu.addSeparator()
        cross_viewer_action = menu.addAction(ICONS["cross"], "Cross viewer")
        cross_viewer_action.triggered.connect(self.on_open_cross_viewer_dialog)
        slice_viewer_action = menu.addAction(ICONS["slice"], "Slice viewer")
        slice_viewer_action.triggered.connect(self.on_open_slice_viewer_dialog)
        radial_integration_action = menu.addAction(ICONS["radial_integration"], "Radial integration")
        radial_integration_action.triggered.connect(self.on_open_radial_integration_dialog)
        roi_manager_action = menu.addAction(ICONS["roi"], "ROI manager")
        roi_manager_action.triggered.connect(self.on_open_roi_manager_dialog)
        menu.exec(self._figure.canvas.mapToGlobal(event))

    def on_open_axis_settings_dialog(self):
        """Opens the axis settings dialog."""
        if self._axis_settings_dialog is None:
            self._axis_settings_dialog = PlotNDAxisSettingsDialog(self._plot_nd_model, self)
        self._axis_settings_dialog.show()

    def on_open_cross_viewer_dialog(self):
        """Opens the cross viewer dialog."""
        if self._cross_viewer_dialog is None:
            self._cross_viewer_dialog = CrossViewerDialog(self._plot_nd_model, self)
            self._cross_viewer_dialog.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)
            self._cross_viewer_dialog.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)
        self._cross_viewer_dialog.show()

    def on_open_general_settings_dialog(self):
        """Opens the general settings dialog."""
        if self._general_settings_dialog is None:
            self._general_settings_dialog = PlotNDGeneralSettingsDialog(self._plot_nd_model, self)
        self._general_settings_dialog.show()

    def on_open_image_settings_dialog(self):
        """Opens the image settings dialog."""
        if self._image_settings_dialog is None:
            self._image_settings_dialog = PlotNDImageSettingsDialog(self._plot_nd_model, self)
        self._image_settings_dialog.show()

    def on_open_radial_integration_dialog(self):
        """Opens the radial integration dialog."""
        if self._radial_integration_dialog is None:
            self._radial_integration_dialog = RadialIntegrationDialog(self._plot_nd_model, self)
            self._radial_integration_dialog.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)
            self._radial_integration_dialog.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)
        self._radial_integration_dialog.show()

    def on_open_roi_manager_dialog(self):
        """Opens the roi manager dialog."""
        if self._roi_manager_dialog is None:
            self._roi_manager_dialog = ROIDialog(self._plot_nd_model, self)
            self._roi_manager_dialog.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)
            self._roi_manager_dialog.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)
        self._roi_manager_dialog.show()

    def on_open_slice_viewer_dialog(self):
        """Opens the slice viewer dialog."""
        if self._slice_viewer_dialog is None:
            self._slice_viewer_dialog = SliceViewerDialog(self._plot_nd_model, self)
        self._slice_viewer_dialog.show()

    def on_open_view_nd_data_dialog(self):
        """Opens the data viewer dialog."""
        if self._data_viewer_nd_dialog is None:
            self._data_viewer_nd_dialog = DataViewerNDDialog(self._plot_nd_model, self)
        self._data_viewer_nd_dialog.show()

    def on_send_plot_on_current_tab(self):
        """Sends the plot to the current tab."""
        axis_info = self._plot_nd_model.get_axis_info()
        dataset_info = self._plot_nd_model.get_dataset_info()

        self.plot_sent_on_current_tab.emit(axis_info,dataset_info)

    def on_send_plot_on_new_tab(self):
        """Sends the plot to a new tab."""
        axis_info = self._plot_nd_model.get_axis_info()
        dataset_info = self._plot_nd_model.get_dataset_info()

        self.plot_sent_on_new_tab.emit(axis_info,dataset_info)

    @property
    def toolbar(self) -> "PyGenPlotNavigationToolbar":
        """Returns the toolbar.

        Returns:
            the toolbar
        """
        return self._toolbar

    def update_data(self, axis_info: List[Dict[str, Any]], data_info: Dict[str, Any]):
        """Updates the widget with new data.

        Args:
            axis_info: the data axis info
            data_info: the data info
        """
        try:
            self._plot_nd_model.add_data(axis_info, data_info)
        except PlotNDModelError as e:
            log(str(e), ["main", "popup"], "error")

