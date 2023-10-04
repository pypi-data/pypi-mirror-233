from typing import Tuple

from qtpy import QtWidgets

from ..kernel.logger import log
from ..models.plot_nd_model import PlotNDModel, PlotNDModelError
from ..widgets.data_slicer_widget import DataSlicerWidget


class SliceViewerDialog(QtWidgets.QDialog):
    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the ND data model
            parent: the parent widget
        """
        super(SliceViewerDialog, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._build()

        self.setWindowTitle("PyGenPlot - Slice viewer dialog")

    def _build(self):
        """Builds the dialog."""
        self._main_layout = QtWidgets.QVBoxLayout()

        self._data_slicer_widget = DataSlicerWidget(self._plot_nd_model, self)
        self._main_layout.addWidget(self._data_slicer_widget)

        self.setLayout(self._main_layout)

        self._plot_nd_model.x_axis_updated.connect(self._data_slicer_widget.on_x_axis_updated)
        self._plot_nd_model.y_axis_updated.connect(self._data_slicer_widget.on_y_axis_updated)

    def on_update(self, slices: Tuple[slice]):
        """Updates the dialog.

        Args:
            the updated slices
        """
        current_x_index = self._data_slicer_widget.current_x_index
        current_y_index = self._data_slicer_widget.current_y_index

        transpose = current_x_index > current_y_index

        try:
            self._plot_nd_model.update_model(slices, transpose)
        except PlotNDModelError as e:
            log(str(e), ["main", "popup"], "error")
