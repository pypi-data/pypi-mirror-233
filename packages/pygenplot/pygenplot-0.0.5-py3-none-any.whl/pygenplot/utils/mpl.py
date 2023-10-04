from typing import Union

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from qtpy import QtCore, QtWidgets

from ..icons import ICONS
from ..widgets.plot_1d_widget import Plot1DWidget
from ..widgets.plot_nd_widget import PlotNDWidget


class PyGenPlotNavigationToolbar(NavigationToolbar2QT):

    plot_sent_on_new_tab = QtCore.Signal()

    plot_sent_on_current_tab = QtCore.Signal()

    def __init__(self, canvas: FigureCanvasQTAgg, widget: Union[Plot1DWidget, PlotNDWidget]):
        """Constructor.

        Args:
            canvas: the canvas to be bound to the toolbar
            widget: the widget containing the toolbar
        """
        super(PyGenPlotNavigationToolbar,self).__init__(canvas, widget)

        for action in self.actions():
            if action.text() == "Customize":
                self.removeAction(action)

        actions = self.actions()
        self.insertSeparator(actions[-1])

        plot_on_new_tab_action = QtWidgets.QAction(ICONS["new_tab"], "Send plot in new tab", widget)
        plot_on_new_tab_action.triggered.connect(self.plot_sent_on_new_tab.emit)
        self.insertAction(actions[-1],plot_on_new_tab_action)

        if isinstance(widget, Plot1DWidget):
            plot_on_current_tab_action = QtWidgets.QAction(ICONS["current_tab"], "Send plot in current tab", widget)
            plot_on_current_tab_action.triggered.connect(self.plot_sent_on_current_tab.emit)
            self.insertAction(actions[-1],plot_on_current_tab_action)    
