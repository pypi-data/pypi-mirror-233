from typing import Any, Dict

import numpy as np

from qtpy import QtCore, QtWidgets

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from ..icons import ICONS


class PreviewWidget(QtWidgets.QWidget):

    plot_sent_on_new_tab = QtCore.Signal()

    plot_sent_on_current_tab = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(PreviewWidget, self).__init__(parent)

        self._build()

        self._ndim = None

    def _build(self):
        """Builds the widget."""
        self._figure = Figure(figsize=(2, 2))
        self._canvas = FigureCanvasQTAgg(self._figure)

        self._canvas._axes = self._figure.add_axes([0.0, 0.0, 1.0, 1.0])
        self._canvas.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self._canvas.customContextMenuRequested.connect(self.on_open_contextual_menu)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self._canvas, 1)

        self.setLayout(main_layout)

        self._ndim = None

    def on_open_contextual_menu(self, event: QtCore.QPoint):
        """Pops up the contextual menu.

        Args:
            event: the right-click event
        """
        menu = QtWidgets.QMenu(self)
        plot_on_new_tab_action = menu.addAction(ICONS["data"], "Plot in new tab")
        plot_on_new_tab_action.triggered.connect(self.plot_sent_on_new_tab.emit)
        if self._ndim == 1:
            plot_on_current_tab_action = menu.addAction(ICONS["data"], "Plot in current tab")
            plot_on_current_tab_action.triggered.connect(self.plot_sent_on_current_tab.emit)
        menu.exec(self._figure.canvas.mapToGlobal(event))

    def update_plot(self, data_info: Dict[str, Any]):
        """Updates the plot.

        Args:
            data_info: the information about the data to preview
        """
        self._figure.axes[0].clear()

        if not data_info["plottable"]:
            self._figure.axes[0].text(0.2, 0.5, "Data not plottable")
        else:
            self._ndim = data_info["dimension"]
            if self._ndim == 1:
                self._figure.axes[0].plot(data_info["data"])
                self._figure.axes[0].legend([data_info["variable"]])

            elif self._ndim == 2:
                self._figure.axes[0].imshow(data_info["data"].T, interpolation="nearest", origin="lower")

            else:
                summed_data = np.sum(data_info["data"], axis=tuple(range(2, self._ndim)))
                self._figure.axes[0].imshow(summed_data.T, interpolation="nearest", origin="lower")

        self._figure.axes[0].set_aspect("auto")
        self._canvas.draw()
