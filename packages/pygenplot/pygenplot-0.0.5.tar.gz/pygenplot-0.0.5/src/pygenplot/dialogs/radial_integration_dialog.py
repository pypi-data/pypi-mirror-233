from typing import Tuple

import numpy as np

from qtpy import QtCore, QtWidgets

from matplotlib.backend_bases import MouseEvent

from ..models.plot_nd_model import PlotNDModel
from ..models.radial_integration_model import RadialIntegrationModel
from ..widgets.plot_1d_widget import Plot1DWidget


class RadialIntegrationDialog(QtWidgets.QDialog):

    plot_sent_on_current_tab = QtCore.Signal(list, list)

    plot_sent_on_new_tab = QtCore.Signal(list, list)

    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the ND data model
            parent: the parent widget
        """
        super(RadialIntegrationDialog, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._radial_integration_model = RadialIntegrationModel(self._plot_nd_model, self)

        self._plot_nd_canvas = plot_nd_model.get_canvas()

        self._radial_profile = None

        self._current_plot = None

        self._in_a_click = False
        self._in_a_drag = False
        self._last_mouse_position = None

        self._button_press_event = None
        self._motion_notify_event = None
        self._button_release_event = None

        self._selected_pixel = None

        self._build()

        self.setWindowTitle("PyGenPlot - Radial integration dialog")

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QHBoxLayout()

        vlayout = QtWidgets.QVBoxLayout()

        selected_pixel_groupbox = QtWidgets.QGroupBox(self)
        selected_pixel_groupbox.setTitle("Selected pixel")
        selected_pixel_groupbox_layout = QtWidgets.QFormLayout()

        x_pixel_label = QtWidgets.QLabel("X")
        self._x_pixel_doublespinbox = QtWidgets.QDoubleSpinBox()
        self._x_pixel_doublespinbox.setMinimum(-np.inf)
        self._x_pixel_doublespinbox.setMaximum(np.inf)
        self._x_pixel_doublespinbox.setSingleStep(1.0)
        self._x_pixel_doublespinbox.setDecimals(4)
        selected_pixel_groupbox_layout.addRow(x_pixel_label, self._x_pixel_doublespinbox)

        y_pixel_label = QtWidgets.QLabel("Y")
        self._y_pixel_doublespinbox = QtWidgets.QDoubleSpinBox()
        self._y_pixel_doublespinbox.setMinimum(-np.inf)
        self._y_pixel_doublespinbox.setMaximum(np.inf)
        self._y_pixel_doublespinbox.setSingleStep(1.0)
        self._y_pixel_doublespinbox.setDecimals(4)
        selected_pixel_groupbox_layout.addRow(y_pixel_label, self._y_pixel_doublespinbox)

        selected_pixel_groupbox.setLayout(selected_pixel_groupbox_layout)
        vlayout.addWidget(selected_pixel_groupbox, 0)

        stretching_groupbox = QtWidgets.QGroupBox(self)
        stretching_groupbox.setTitle("Stretching")
        stretching_groupbox_layout = QtWidgets.QFormLayout()

        x_stretch_label = QtWidgets.QLabel("X")
        self._x_stretch_doublespinbox = QtWidgets.QDoubleSpinBox()
        self._x_stretch_doublespinbox.setMinimum(0)
        self._x_stretch_doublespinbox.setMaximum(np.inf)
        self._x_stretch_doublespinbox.setValue(1.0)
        self._x_stretch_doublespinbox.setSingleStep(1.0e-02)
        stretching_groupbox_layout.addRow(x_stretch_label, self._x_stretch_doublespinbox)

        y_stretch_label = QtWidgets.QLabel("Y")
        self._y_stretch_doublespinbox = QtWidgets.QDoubleSpinBox()
        self._y_stretch_doublespinbox.setMinimum(0)
        self._y_stretch_doublespinbox.setMaximum(np.inf)
        self._y_stretch_doublespinbox.setValue(1.0)
        self._y_stretch_doublespinbox.setSingleStep(1.0e-02)
        stretching_groupbox_layout.addRow(y_stretch_label, self._y_stretch_doublespinbox)

        stretching_groupbox.setLayout(stretching_groupbox_layout)
        vlayout.addWidget(stretching_groupbox, 0)

        shells_groupbox = QtWidgets.QGroupBox(self)
        shells_groupbox.setTitle("Shells")
        shells_groupbox_layout = QtWidgets.QFormLayout()

        n_shells_label = QtWidgets.QLabel("Number")
        self._n_shells_spinbox = QtWidgets.QSpinBox()
        self._n_shells_spinbox.setMinimum(1)
        self._n_shells_spinbox.setMaximum(1000000)
        self._n_shells_spinbox.setValue(10)
        shells_groupbox_layout.addRow(n_shells_label, self._n_shells_spinbox)

        shell_width_label = QtWidgets.QLabel("Shell width:")
        self._shell_width_doublespinbox = QtWidgets.QDoubleSpinBox()
        self._shell_width_doublespinbox.setMinimum(0.0)
        self._shell_width_doublespinbox.setMaximum(1000.0)
        self._shell_width_doublespinbox.setSingleStep(1.0e-02)
        self._shell_width_doublespinbox.setValue(10.0)
        shells_groupbox_layout.addRow(shell_width_label, self._shell_width_doublespinbox)

        shells_groupbox.setLayout(shells_groupbox_layout)
        vlayout.addWidget(shells_groupbox, 0)

        vlayout.addStretch()

        main_layout.addLayout(vlayout, 0)

        self._radial_integration_plot = Plot1DWidget(self)
        self._radial_integration_plot.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)
        self._radial_integration_plot.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)
        main_layout.addWidget(self._radial_integration_plot, 1)

        self.setLayout(main_layout)

        self.installEventFilter(self)

        self.finished.connect(self.on_close)
        self._plot_nd_model.data_axis_changed.connect(self.on_clear)
        self._plot_nd_model.model_updated.connect(self.on_update)
        self._x_pixel_doublespinbox.valueChanged.connect(self.on_update)
        self._y_pixel_doublespinbox.valueChanged.connect(self.on_update)
        self._x_stretch_doublespinbox.valueChanged.connect(self.on_update)
        self._y_stretch_doublespinbox.valueChanged.connect(self.on_update)
        self._n_shells_spinbox.valueChanged.connect(self.on_update)
        self._shell_width_doublespinbox.valueChanged.connect(self.on_update)

    def _compute_new_position_from_event(self, new_x: float, new_y: float) -> Tuple[float, float]:
        """Compute the new position.

        Args:
            new_x: the new X value
            new_y: the new Y value

        Returns:
            the new position
        """
        dx = new_x - self._selected_pixel[0]
        dy = new_y - self._selected_pixel[1]

        return self._x_pixel_doublespinbox.value() + dx, self._y_pixel_doublespinbox.value() + dy

    def eventFilter(self, source: QtWidgets.QWidget, event: QtCore.QEvent) -> bool:
        """Event filter for the dialog.

        Args:
            source: the widget triggering whose event should be filtered
            event: the event

        Returns:
            whether the event has been successfully filtered
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            self._plot_nd_model.activate_radial_integration_artists()
            self.setFocus()
            return True
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            return True
        else:
            return super(RadialIntegrationDialog,self).eventFilter(source,event)

    def on_clear(self):
        """Clears the dialog."""
        self._radial_integration_model.unset_integration_central_point()
        self._radial_integration_model.unset_integration_shells()
        self._radial_integration_plot.close()

    def on_close(self):
        """Closes the dialog."""
        self.on_clear()
        self._plot_nd_canvas.mpl_disconnect(self._button_press_event)
        self._plot_nd_canvas.mpl_disconnect(self._motion_notify_event)
        self._plot_nd_canvas.mpl_disconnect(self._button_release_event)

    def on_mouse_click(self, event: MouseEvent):
        """Event handler for the mouse press event.

        Args:
            event: the mouse press event
        """
        if not self._radial_integration_model.artists_activated:
            return

        if event.button != 1:
            return

        if event.xdata is None or event.ydata is None:
            return

        self._in_a_click = True
        self._last_mouse_position = (event.xdata, event.ydata)

        self._selected_pixel = (event.xdata, event.ydata)

    def on_mouse_click_released(self, event: MouseEvent):
        """Event handler for the mouse release event.

        Args:
            event: the mouse release event
        """
        if not self._radial_integration_model.artists_activated:
            return

        self._in_a_click = False

        if event.button != 1:
            return

        new_x = event.xdata
        new_y = event.ydata
        if self._in_a_drag:
            self._in_a_drag = False
            if new_x is None or new_y is None:
                new_x = self._last_mouse_position[0]
                new_y = self._last_mouse_position[1]
            new_x, new_y = self._compute_new_position_from_event(new_x, new_y)
        else:
            if new_x is None or new_y is None:
                return

        self._last_mouse_position = None

        self._x_pixel_doublespinbox.blockSignals(True)
        self._x_pixel_doublespinbox.setValue(new_x)
        self._x_pixel_doublespinbox.blockSignals(False)
        self._y_pixel_doublespinbox.blockSignals(True)
        self._y_pixel_doublespinbox.setValue(new_y)
        self._y_pixel_doublespinbox.blockSignals(False)

        self.on_update()

    def on_mouse_moved(self, event: MouseEvent):
        """Event handler for the mouse move event.

        Args:
            event: the mouse move event
        """
        if not self._radial_integration_model.artists_activated:
            return

        if self._in_a_click:
            self._in_a_drag = True
            if event.xdata is None or event.ydata is None:
                return
            self._last_mouse_position = (event.xdata, event.ydata)

            stretch_x = self._x_stretch_doublespinbox.value()
            stretch_y = self._y_stretch_doublespinbox.value()
            shell_width = self._shell_width_doublespinbox.value()
            n_shells = self._n_shells_spinbox.value()
            shells = shell_width * np.arange(0, n_shells + 1)

            new_x = event.xdata
            new_y = event.ydata
            new_x, new_y = self._compute_new_position_from_event(new_x, new_y)
            self._radial_integration_model.display_integration_shells(new_x, new_y, shells, stretch_x, stretch_y)

    def on_update(self):
        """Updates the dialog."""
        pixel_x = self._x_pixel_doublespinbox.value()
        pixel_y = self._y_pixel_doublespinbox.value()

        stretch_x = self._x_stretch_doublespinbox.value()
        stretch_y = self._y_stretch_doublespinbox.value()

        shell_width = self._shell_width_doublespinbox.value()
        n_shells = self._n_shells_spinbox.value()
        shells = shell_width * np.arange(0, n_shells + 1)

        self._radial_integration_model.display_integration_shells(pixel_x, pixel_y, shells, stretch_x, stretch_y)
        self._radial_profile = self._radial_integration_model.compute_radial_profile(pixel_x, pixel_y, shells,
                                                                                     stretch_x, stretch_y)

        self._radial_integration_plot.get_plot_1d_model().clear()
        self._radial_integration_plot.add_line(*self._radial_profile)

    def show(self):
        """Shows the dialog."""
        super(RadialIntegrationDialog, self).show()
        self._button_press_event = self._plot_nd_canvas.mpl_connect("button_press_event", self.on_mouse_click)
        self._motion_notify_event = self._plot_nd_canvas.mpl_connect("motion_notify_event", self.on_mouse_moved)
        self._button_release_event = self._plot_nd_canvas.mpl_connect("button_release_event",
                                                                      self.on_mouse_click_released)
