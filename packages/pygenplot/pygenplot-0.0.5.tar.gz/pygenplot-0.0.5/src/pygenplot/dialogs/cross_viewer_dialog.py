from typing import Tuple

from qtpy import QtCore, QtWidgets

from matplotlib.backend_bases import MouseEvent

from ..kernel.logger import log
from ..models.cross_view_model import CrossViewModel
from ..models.plot_1d_model import Plot1DModel, Plot1DModelError
from ..models.plot_nd_model import PlotNDModel
from ..widgets.plot_1d_widget import Plot1DWidget


class CrossViewerDialog(QtWidgets.QDialog):

    plot_sent_on_current_tab = QtCore.Signal(list, list)

    plot_sent_on_new_tab = QtCore.Signal(list, list)

    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the ND data model
            parent: the parent widget
        """
        super(CrossViewerDialog, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._cross_view_model = CrossViewModel(self._plot_nd_model, self)

        self._build()

        self._button_press_event = None

        self.setWindowTitle("PyGenPlot - Cross viewer dialog")

        self.resize(900, 1000)

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        self._horizontal_axis_slice = Plot1DWidget(self)
        self._horizontal_axis_slice.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)
        self._horizontal_axis_slice.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)
        main_layout.addWidget(self._horizontal_axis_slice)

        self._vertical_axis_slice = Plot1DWidget(self)
        self._vertical_axis_slice.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)
        self._vertical_axis_slice.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)
        main_layout.addWidget(self._vertical_axis_slice)

        self.setLayout(main_layout)

        self.installEventFilter(self)

        self.finished.connect(self.on_close)

        self._plot_nd_model.data_axis_changed.connect(self.on_clear)

        horizontal_plot_1d_model = self._horizontal_axis_slice.get_plot_1d_model()
        horizontal_plot_1d_model.line_removed.connect(
            lambda row: self.on_remove_line(row, True)
        )
        horizontal_plot_1d_model.line_selected.connect(
            lambda index: self.on_select_line(index, True)
        )
        horizontal_plot_1d_model.model_cleared.connect(self._cross_view_model.clear_horizontal_slicers)

        vertical_plot_1d_model = self._vertical_axis_slice.get_plot_1d_model()
        vertical_plot_1d_model.line_removed.connect(
            lambda row: self.on_remove_line(row, True)
        )
        vertical_plot_1d_model.line_selected.connect(
            lambda index: self.on_select_line(index, False)
        )
        vertical_plot_1d_model.model_cleared.connect(self._cross_view_model.clear_vertical_slicers)

    def _select_horizontal_slice(self, index: int):
        """Selects a horizontal slice.

        Args:
            index: the selected index
        """
        if not self._cross_view_model.artists_activated:
            return

        self._cross_view_model.select_horizontal_slicer(index)

    def _select_vertical_slice(self, index: int):
        """Selects a vertical slice.

        Args:
            index: the selected index
        """
        if not self._cross_view_model.artists_activated:
            return

        self._cross_view_model.select_vertical_slicer(index)

    def eventFilter(self, source: QtWidgets.QWidget, event: QtCore.QEvent) -> bool:
        """Event filter for the widget.

        Args:
            source: the widget triggering the event.
            event: the event

        Returns:
            whether the event was filtered
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            self._plot_nd_model.activate_slice_artists()
            self.setFocus()
            return True
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            return True
        else:
            return super(CrossViewerDialog,self).eventFilter(source,event)

    def on_button_press(self, event: MouseEvent):
        """Event handler for button press event.

        Args:
            event: the button press event
        """
        if not self._cross_view_model.artists_activated:
            return

        if event.button != 1:
            return

        if event.xdata is None:
            return

        if event.ydata is None:
            return

        x = event.xdata
        y = event.ydata

        self.on_plot_vertical_slice(x)
        self.on_plot_horizontal_slice(y)

    def on_change_line_color(self, row: int, color: Tuple[float, float, float], horizontal: bool):
        """Changes the color of a line.

        Args:
            row: the index of the line
            color: the new color
            horizontal: whether the line color should be changed on the horizontal plot
        """
        if horizontal:
            self._cross_view_model.set_horizontal_slicer_color(row, color)
        else:
            self._cross_view_model.set_vertical_slicer_color(row, color)

    def on_clear(self):
        """Clear the cross viewer and its associated artists.        """
        self._vertical_axis_slice.on_clear_plot()
        self._horizontal_axis_slice.on_clear_plot()

    def on_close(self):
        """Closes the dialog."""
        self._vertical_axis_slice.close()
        self._horizontal_axis_slice.close()
        self._plot_nd_model.get_canvas().mpl_disconnect(self._button_press_event)

    def on_plot_vertical_slice(self, x: float):
        """Plots a vertical slice.

        Args;
            x: the X value of the vertical slice
        """
        vertical_plot_1d_model = self._vertical_axis_slice.get_plot_1d_model()

        x_axis_info, y_axis_info = self._plot_nd_model.get_vertical_slice_info(int(x))
        try:
            vertical_plot_1d_model.add_line(x_axis_info, y_axis_info)
        except Plot1DModelError as e:
            log(str(e), ["main", "popup"], "error")
        else:
            last_index = vertical_plot_1d_model.index(vertical_plot_1d_model.rowCount() - 1,0)
            line = vertical_plot_1d_model.data(last_index, Plot1DModel.LineRole)
            self._cross_view_model.add_vertical_slicer(x, line.get_color())

    def on_plot_horizontal_slice(self, y: float):
        """Plots a horizontal slice.

        Args:
            y: the Y value of the horizontal slice
        """
        horizontal_plot_1d_model = self._horizontal_axis_slice.get_plot_1d_model()

        x_axis_info, y_axis_info = self._plot_nd_model.get_horizontal_slice_info(int(y))
        try:
            horizontal_plot_1d_model.add_line(x_axis_info, y_axis_info)
        except Plot1DModelError as e:
            log(str(e), ["main", "popup"], "error")
        else:
            last_index = horizontal_plot_1d_model.index(horizontal_plot_1d_model.rowCount() - 1,0)
            line = horizontal_plot_1d_model.data(last_index, Plot1DModel.LineRole)
            self._cross_view_model.add_horizontal_slicer(y, line.get_color())

    def on_remove_line(self, index: int, horizontal: bool):
        """Selects a line.

        Args:
            index: the index of the line
            horizontal: whether the line should be removed on the horizontal plot
        """
        if horizontal:
            self._cross_view_model.remove_horizontal_slicer(index)
        else:
            self._cross_view_model.remove_vertical_slicer(index)

    def on_select_line(self, index: QtCore.QModelIndex, horizontal: bool):
        """Selects a line.

        Args:
            index: the index of the line
            horizontal: whether the line is selected on the horizontal plot
        """
        if horizontal:
            horizontal_plot_1d_model = self._horizontal_axis_slice.get_plot_1d_model()
            if index.isValid():
                row = index.row()
                self._cross_view_model.select_horizontal_slicer(row)
                line = horizontal_plot_1d_model.data(index, Plot1DModel.LineRole)
                self._cross_view_model.set_horizontal_slicer_color(row, line.get_color())
            else:
                self._cross_view_model.unselect_horizontal_slicers()

        else:
            vertical_plot_1d_model = self._vertical_axis_slice.get_plot_1d_model()
            if index.isValid():
                column = index.row()
                self._cross_view_model.select_vertical_slicer(column)
                line = vertical_plot_1d_model.data(index, Plot1DModel.LineRole)
                self._cross_view_model.set_vertical_slicer_color(column, line.get_color())
            else:
                self._cross_view_model.unselect_vertical_slicers()

    def show(self):
        """Shows the dialog."""
        super(CrossViewerDialog, self).show()
        self._button_press_event = self._plot_nd_model.get_canvas().mpl_connect("button_press_event",
                                                                                self.on_button_press)
