from typing import Tuple

from qtpy import QtCore, QtWidgets

from ..models.plot_1d_model import Plot1DModel
from ..models.plot_nd_model import PlotNDModel
from ..models.roi_model import ROIModel
from ..widgets.plot_1d_widget import Plot1DWidget


class ROIDialog(QtWidgets.QDialog):

    plot_sent_on_current_tab = QtCore.Signal(list, list)

    plot_sent_on_new_tab = QtCore.Signal(list, list)

    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the plot ND model
            parent: the parent widget
        """
        super(ROIDialog, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._roi_model = ROIModel(self._plot_nd_model, self)

        self._key_press_event = None

        self._button_press_event = None

        self._build()

        self.setWindowTitle("PyGenPlot - ROI manager dialog")

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        vlayout = QtWidgets.QVBoxLayout()

        self._horizontal_integration_plot = Plot1DWidget(self)
        self._horizontal_integration_plot.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)
        self._horizontal_integration_plot.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)

        self._horizontal_plot_1d_model = self._horizontal_integration_plot.get_plot_1d_model()
        self._horizontal_plot_1d_model.set_figure_title("Horizontal integration")
        self._horizontal_plot_1d_model.line_selected.connect(self.on_select_line)
        self._horizontal_plot_1d_model.line_removed.connect(
            lambda row: self.on_remove_line(row, True)
        )
        self._horizontal_plot_1d_model.line_color_changed.connect(
            lambda row, color: self.on_change_line_color(row, color, True)
        )
        self._horizontal_plot_1d_model.line_label_changed.connect(
            lambda row, label: self.on_change_line_label(row, label, True)
        )
        vlayout.addWidget(self._horizontal_integration_plot)

        self._vertical_integration_plot = Plot1DWidget(self)
        self._vertical_integration_plot.plot_sent_on_new_tab.connect(self.plot_sent_on_new_tab.emit)
        self._vertical_integration_plot.plot_sent_on_current_tab.connect(self.plot_sent_on_current_tab.emit)

        self._vertical_plot_1d_model = self._vertical_integration_plot.get_plot_1d_model()
        self._vertical_plot_1d_model.set_figure_title("Vertical integration")
        self._vertical_plot_1d_model.line_selected.connect(self.on_select_line)
        self._vertical_plot_1d_model.line_removed.connect(
            lambda row, color: self.on_remove_line(row, False)
        )
        self._vertical_plot_1d_model.line_color_changed.connect(
            lambda row, color: self.on_change_line_color(row, color, False)
        )
        self._vertical_plot_1d_model.line_label_changed.connect(
            lambda row, label: self.on_change_line_label(row, label, False)
        )
        vlayout.addWidget(self._vertical_integration_plot)

        main_layout.addLayout(vlayout)

        self.setLayout(main_layout)

        self.installEventFilter(self)

        self.finished.connect(self.on_close)

        self._plot_nd_model.data_axis_changed.connect(lambda : self.on_clear(True))
        self._plot_nd_model.model_updated.connect(self.on_update)
        self._roi_model.roi_added.connect(self.on_plot_roi)
        self._roi_model.roi_modified.connect(self.on_update_roi)
        self._roi_model.roi_selected.connect(self.on_roi_selected)

    def eventFilter(self, source: QtWidgets.QWidget, event: QtCore.QEvent) -> bool:
        """Event filter for the dialog.

        Args:
            source: the widget triggering whose event should be filtered
            event: the event

        Returns:
            whether the event has been successfully filtered
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            self._plot_nd_model.activate_roi_artists()
            self.setFocus()
            return True
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            return True
        else:
            return super(ROIDialog,self).eventFilter(source,event)

    def on_change_line_color(self, row: int, color: Tuple[float], horizontal: bool):
        """Changes the line color.
        
        Args:
            row: the index of the line
            color: the new color
            horizontal: whether the line color should be changed on the horizontal plot
        """
        index = self._roi_model.index(row, 0)
        self._roi_model.setData(index, color, ROIModel.ROIColorRole)

        if horizontal:
            index = self._vertical_plot_1d_model.index(row, 0)
            self._vertical_plot_1d_model.blockSignals(True)
            self._vertical_plot_1d_model.setData(index, color, Plot1DModel.LineColorRole)
            self._vertical_plot_1d_model.blockSignals(False)
        else:
            index = self._horizontal_plot_1d_model.index(row, 0)
            self._horizontal_plot_1d_model.blockSignals(True)
            self._horizontal_plot_1d_model.setData(index, color, Plot1DModel.LineColorRole)
            self._horizontal_plot_1d_model.blockSignals(False)

    def on_change_line_label(self, row: int, label: str, horizontal: bool):
        """Changes the line label.

        Args:
            row: the index of the line
            label: the new label
            horizontal: whether the line label should be changed on the horizontal plot
        """
        if horizontal:
            index = self._vertical_plot_1d_model.index(row, 0)
            self._vertical_plot_1d_model.blockSignals(True)
            self._vertical_plot_1d_model.setData(index, label, QtCore.Qt.ItemDataRole.EditRole)
            self._vertical_plot_1d_model.blockSignals(False)
        else:
            index = self._horizontal_plot_1d_model.index(row, 0)
            self._horizontal_plot_1d_model.blockSignals(True)
            self._horizontal_plot_1d_model.setData(index, label, QtCore.Qt.ItemDataRole.EditRole)
            self._horizontal_plot_1d_model.blockSignals(False)

    def on_clear(self, init: bool = False):
        """Clears the ROIs.

        Args:
            init: whether the roi model should be reinit
        """
        self._roi_model.clear()
        if init:
            self._roi_model.init()
        self._horizontal_integration_plot.close()
        self._vertical_integration_plot.close()

    def on_close(self):
        """Closes the dialog."""
        self.on_clear(False)
        plot_nd_canvas = self._plot_nd_model.get_canvas()
        plot_nd_canvas.mpl_disconnect(self._button_press_event)
        plot_nd_canvas.mpl_disconnect(self._key_press_event)

    def on_plot_roi(self, index: QtCore.QModelIndex):
        """Plots a ROI.

        Args:
            index: the index of the selected ROI        
        """
        roi = self._roi_model.data(index, ROIModel.ROIRole)
        if roi is None:
            return

        row = index.row()
        roi_name = self._roi_model.data(index, QtCore.Qt.ItemDataRole.DisplayRole)

        color = self._roi_model.data(index, QtCore.Qt.ItemDataRole.ForegroundRole)
        color = tuple([v / 255.0 for v in color.getRgb()[:3]])

        horizontal_plot, vertical_plot = roi.get_roi_info()
        self._horizontal_integration_plot.add_line(*horizontal_plot)
        self._vertical_integration_plot.add_line(*vertical_plot)

        plot_1d_model = self._horizontal_integration_plot.get_plot_1d_model()
        plot_1d_model.setData(plot_1d_model.index(row, 0), color, Plot1DModel.LineColorRole)
        plot_1d_model.setData(plot_1d_model.index(row, 0), roi_name, QtCore.Qt.ItemDataRole.EditRole)

        plot_1d_model = self._vertical_integration_plot.get_plot_1d_model()
        plot_1d_model.setData(plot_1d_model.index(row, 0), color, Plot1DModel.LineColorRole)
        plot_1d_model.setData(plot_1d_model.index(row, 0), roi_name, QtCore.Qt.ItemDataRole.EditRole)

    def on_remove_line(self, row: int, horizontal: bool):
        """Removes a line.

        Args:
            row: the index of the line
            horizontal: whether the line color should be removed on the horizontal plot
        """
        self._roi_model.removeRow(row)

        if horizontal:
            self._vertical_plot_1d_model.blockSignals(True)
            self._vertical_plot_1d_model.removeRow(row)
            self._vertical_plot_1d_model.blockSignals(False)
        else:
            self._horizontal_plot_1d_model.blockSignals(True)
            self._horizontal_plot_1d_model.removeRow(row)
            self._horizontal_plot_1d_model.blockSignals(False)

    def on_roi_selected(self, index: QtCore.QModelIndex):
        """Selects a ROI.

        Args:
            index: the index of the selected ROI
        """
        horizontal_plot_1d_model = self._horizontal_integration_plot.get_plot_1d_model()
        vertical_plot_1d_model = self._vertical_integration_plot.get_plot_1d_model()

        if not index.isValid():
            horizontal_plot_1d_model.unselect_line()
            vertical_plot_1d_model.unselect_line()
        else:
            row = index.row()
            line = horizontal_plot_1d_model.data(horizontal_plot_1d_model.index(row, 0), Plot1DModel.LineRole)
            horizontal_plot_1d_model.select_line(line)

            line = vertical_plot_1d_model.data(vertical_plot_1d_model.index(row, 0), Plot1DModel.LineRole)
            vertical_plot_1d_model.select_line(line)

    def on_select_line(self, index: QtCore.QModelIndex):
        """Selects a line.

        Args:
            index: the index of the selected ROI        
        """
        if index.isValid():
            row = index.row()
            index = self._roi_model.index(row, 0)
            roi = self._roi_model.data(index, ROIModel.ROIRole)
            self._roi_model.select_roi(roi)
        else:
            self._roi_model.select_roi(None)

    def on_select_roi(self, index: QtCore.QModelIndex):
        """Selects a ROI.

        Args:
            index: the index of the selected roi
        """
        roi = self._roi_model.data(index, ROIModel.ROIRole)
        self._roi_model.select_roi(roi)

    def on_update(self):
        """Updates the dialog."""
        for row in range(self._roi_model.rowCount()):
            index = self._roi_model.index(row,0)
            self.on_update_roi(index)

    def on_update_roi(self, index: QtCore.QModelIndex):
        """Updates a given ROI.

        Args:
            index: the index of the selected ROI
        """
        roi = self._roi_model.data(index, ROIModel.ROIRole)
        if roi is None:
            return

        row = index.row()

        horizontal_plot, vertical_plot = roi.get_roi_info()
        self._horizontal_plot_1d_model.setData(
            self._horizontal_plot_1d_model.index(row, 0), (horizontal_plot[0], horizontal_plot[1]),
            Plot1DModel.DataRole
        )
        self._vertical_plot_1d_model.setData(
            self._vertical_plot_1d_model.index(row, 0), (vertical_plot[0], vertical_plot[1]),
            Plot1DModel.DataRole
        )

    def show(self):
        """Shows the dialog."""
        super(ROIDialog, self).show()
        plot_nd_canvas = self._plot_nd_model.get_canvas()
        self._key_press_event = plot_nd_canvas.mpl_connect("key_press_event", self._roi_model.on_key_press)
        self._button_press_event = plot_nd_canvas.mpl_connect("button_press_event", self._roi_model.on_button_press)
        self._roi_model.init()
