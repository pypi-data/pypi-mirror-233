from typing import Any, Dict

from qtpy import QtCore, QtWidgets

from matplotlib.backend_bases import KeyEvent, PickEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from ..icons import ICONS
from ..dialogs.data_viewer_1d_dialog import DataViewer1DDialog
from ..dialogs.plot_1d_axis_settings_dialog import Plot1DAxisSettingsDialog
from ..dialogs.plot_1d_general_settings_dialog import Plot1DGeneralSettingsDialog
from ..dialogs.plot_1d_lines_settings_dialog import Plot1DLinesSettingsDialog
from ..kernel.logger import log
from ..models.plot_1d_model import Plot1DModel, Plot1DModelError


class Plot1DWidget(QtWidgets.QWidget):

    plot_sent_on_new_tab = QtCore.Signal(list,list)

    plot_sent_on_current_tab = QtCore.Signal(list,list)

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(Plot1DWidget, self).__init__(parent)

        self._selected_line = None

        self._axis_settings_dialog = None
        self._lines_settings_dialog = None
        self._general_settings_dialog = None
        self._data_viewer_1d_dialog = None

        self._plot_1d_model = None

        self._build()

    def _build(self):
        """Builds the widget."""
        self._figure = Figure()
        self._canvas = FigureCanvasQTAgg(self._figure)
        self._canvas.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self._canvas.customContextMenuRequested.connect(self.on_open_contextual_menu)
        self._canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self._canvas.setFocus()

        self._figure.add_subplot(111, picker=True)

        self._plot_1d_model = Plot1DModel(self._figure, self)

        from ..utils.mpl import PyGenPlotNavigationToolbar
        self._toolbar = PyGenPlotNavigationToolbar(self._canvas, self)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self._canvas, 1)
        main_layout.addWidget(self._toolbar)

        self.setLayout(main_layout)

        self._canvas.mpl_connect("key_press_event", self.on_key_press)
        self._canvas.mpl_connect("pick_event", self.on_pick_line)

        self._toolbar.plot_sent_on_current_tab.connect(self.on_send_plot_on_current_tab)
        self._toolbar.plot_sent_on_new_tab.connect(self.on_send_plot_on_new_tab)

    def add_line(self, x_data_info: Dict[str, Any], y_data_info: Dict[str, Any]):
        """Adds a line to the plot.

        Args:
            x_data_info: the information about the X axis of the line to plot
            y_data_info: the information about the Y axis of the line to plot
        """
        try:
            self._plot_1d_model.add_line(x_data_info, y_data_info)
        except Plot1DModelError as e:
            log(str(e), ["main", "popup"], "error")

    def close(self):
        """Closes the widget."""
        self._plot_1d_model.clear()

        self.close_axis_settings_dialog()

        self.close_data_viewer_1d_dialog()

        self.close_general_settings_dialog()

        self.close_lines_settings_dialog()

    def close_axis_settings_dialog(self):
        """Closes the axis settings dialog."""
        if self._axis_settings_dialog is not None:
            self._axis_settings_dialog.close()
            self._axis_settings_dialog = None

    def close_data_viewer_1d_dialog(self):
        """Closes the data viewer dialog."""
        if self._data_viewer_1d_dialog is not None:
            self._data_viewer_1d_dialog.close()
            self._data_viewer_1d_dialog = None

    def close_general_settings_dialog(self):
        """Closes the general settings dialog."""
        if self._general_settings_dialog is not None:
            self._general_settings_dialog.close()
            self._general_settings_dialog = None

    def close_lines_settings_dialog(self):
        """Closes the lines settings dialog."""
        if self._lines_settings_dialog is not None:
            self._lines_settings_dialog.close()
            self._lines_settings_dialog = None

    def get_plot_1d_model(self) -> Plot1DModel:
        """Returns the model underlying the widget.

        Returns:
            the 1D data model
        """
        return self._plot_1d_model

    def on_clear_plot(self):
        """Clears the plots."""
        self._plot_1d_model.clear()

    def on_key_press(self, event: KeyEvent):
        """Event handler for keypress event.

        Args:
            event: the keypress event
        """
        if event.key == "delete":
            selected_line_index = self._plot_1d_model.get_selected_line_index()
            if selected_line_index is not None:
                choice = QtWidgets.QMessageBox.question(
                    self,
                    "Delete line",
                    "Do you really want to delete this line ?",
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                )

                if choice == QtWidgets.QMessageBox.StandardButton.No:
                    return False

                self._plot_1d_model.removeRow(selected_line_index)

    def on_open_axis_settings_dialog(self):
        """Opens axis settings dialog."""
        if self._axis_settings_dialog is None:
            self._axis_settings_dialog = Plot1DAxisSettingsDialog(self._plot_1d_model, self)

        self._axis_settings_dialog.show()

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
        lines_settings_action = menu.addAction(ICONS["line"], "Lines settings")
        lines_settings_action.triggered.connect(self.on_open_lines_settings_dialog)
        menu.addSeparator()
        clear_action = menu.addAction(ICONS["clear"], "Clear")
        clear_action.triggered.connect(self.on_clear_plot)
        menu.addSeparator()
        view_data_action = menu.addAction(ICONS["data"], "View data")
        view_data_action.triggered.connect(self.on_open_view_1d_data_dialog)
        menu.exec(self._figure.canvas.mapToGlobal(event))

    def on_open_general_settings_dialog(self):
        """Opens the general settings dialog."""
        if self._general_settings_dialog is None:
            self._general_settings_dialog = Plot1DGeneralSettingsDialog(self._plot_1d_model, self)
        self._general_settings_dialog.show()

    def on_open_lines_settings_dialog(self):
        """Opens the lines settings dialog."""
        if self._lines_settings_dialog is None:
            self._lines_settings_dialog = Plot1DLinesSettingsDialog(self._plot_1d_model, self)
        self._lines_settings_dialog.show()

    def on_open_view_1d_data_dialog(self):
        """Opens the data viewer dialog."""
        if self._data_viewer_1d_dialog is None:
            self._data_viewer_1d_dialog = DataViewer1DDialog(self._plot_1d_model, self)
        self._data_viewer_1d_dialog.show()

    def on_pick_line(self, event: PickEvent):
        """Picks a line of the plot.

        Args:
            event: the mouse pick event
        """
        if event.mouseevent.button == 1:
            if event.artist == self._figure.axes[0]:
                self._plot_1d_model.unselect_line()
            else:
                self._plot_1d_model.select_line(event.artist)

    def on_send_plot_on_current_tab(self):
        """Sends the plot on the current tab."""
        axis_info = self._plot_1d_model.get_axis_info()
        dataset_info = self._plot_1d_model.get_dataset_info()

        self.plot_sent_on_current_tab.emit(axis_info,dataset_info)

    def on_send_plot_on_new_tab(self):
        """Sends the plot on a new tab."""
        axis_info = self._plot_1d_model.get_axis_info()
        dataset_info = self._plot_1d_model.get_dataset_info()

        self.plot_sent_on_new_tab.emit(axis_info,dataset_info)

    def set_plot_1d_model(self, model: Plot1DModel):
        """Sets the 1D data model.

        Args:
            model: the 1D data model
        """
        self._plot_1d_model = model

    @property
    def toolbar(self) -> "PyGenPlotNavigationToolbar":
        """Returns the toolbar.

        Returns:
            the toolbar
        """
        return self._toolbar
