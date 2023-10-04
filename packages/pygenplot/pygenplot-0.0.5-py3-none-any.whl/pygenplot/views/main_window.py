import logging
import sys
from typing import Any, Dict, List, Optional

from qtpy import QtCore, QtGui, QtWidgets

from ..__pkginfo__ import __version__
from ..dialogs.about_dialog import AboutDialog
from ..dialogs.units_editor_dialog import UnitsEditorDialog
from ..data.units import UnitsManager
from ..kernel.logger import log, LOGGER
from ..icons import ICONS, load_icons
from ..handlers.logger_popup import LoggerPopup
from ..handlers.logger_widget import LoggerWidget
from ..models.data_tree_model import DATA_ITEMS, DataTreeModelError
from ..models.plot_1d_model import Plot1DModelError
from ..widgets.data_widget import DataWidget
from ..widgets.plot_1d_widget import Plot1DWidget
from ..widgets.plot_nd_widget import PlotNDWidget
from ..widgets.preview_widget import PreviewWidget


class MainWindow(QtWidgets.QMainWindow):

    units_updated = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget, filename: Optional[str] = None):
        """Constructor.
        
        Args:
            parent: the parent widget
            filename: the data filename
        """
        super(MainWindow, self).__init__(parent)

        load_icons()

        self._build()

        self._build_menu()

        self._build_toolbar()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.setWindowTitle(f"pygenplot ({__version__})")

        log("Welcome to pygenplot",["main"], "info")

        UnitsManager.load()

        self._units_dialog = None

        if filename is not None:
            self.add_data(filename)

    def _build(self):
        """Builds the main window."""
        self._tab_widget = QtWidgets.QTabWidget(self)
        self._tab_widget.setTabsClosable(True)
        self.setCentralWidget(self._tab_widget)

        self._data_dock_widget = QtWidgets.QDockWidget("Data",self)
        self._data_dock_widget.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)
        self._data_dock_widget.setFloating(False)
        self._data_dock_widget.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self._data_widget = DataWidget(self)
        self._data_dock_widget.setWidget(self._data_widget)

        self._preview_dock_widget = QtWidgets.QDockWidget("Preview",self)
        self._preview_dock_widget.setAllowedAreas(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)
        self._preview_dock_widget.setFloating(False)
        self._preview_dock_widget.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self._preview_widget = PreviewWidget(self)
        self._preview_dock_widget.setWidget(self._preview_widget)        

        self._logger_dock_widget = QtWidgets.QDockWidget("Logger",self)
        self._logger_dock_widget.setAllowedAreas(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea)
        self._logger_widget = LoggerWidget(self)
        self._logger_dock_widget.setWidget(self._logger_widget)
        self._logger_widget.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        LOGGER["main"].addHandler(self._logger_widget)
        LOGGER["main"].setLevel(logging.INFO)

        self._logger_popup = LoggerPopup()
        self._logger_popup.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        LOGGER["popup"].addHandler(self._logger_popup)
        LOGGER["popup"].setLevel(logging.ERROR)

        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,self._data_dock_widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,self._preview_dock_widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea,self._logger_dock_widget)

        self.resize(1000,1000)

        self._tab_widget.tabCloseRequested.connect(self.on_close_plot)

        self._data_widget.dataset_selected.connect(self.on_select_dataset)
        self._data_widget.plot_sent_on_current_tab.connect(self.on_plot_on_current_tab)
        self._data_widget.plot_sent_on_new_tab.connect(self.on_plot_on_new_tab)
        self._preview_widget.plot_sent_on_new_tab.connect(self.on_preview_sent_on_new_tab)
        self._preview_widget.plot_sent_on_current_tab.connect(self.on_preview_sent_on_current_tab)

    def _build_menu(self):
        """Builds the menu."""
        menubar = self.menuBar()
        file_menu = QtWidgets.QMenu("&File", self)
        load_files_action = file_menu.addAction(ICONS["load"],"Load Data")
        load_files_action.triggered.connect(self.on_load_data)
        units_action = file_menu.addAction(ICONS["units"], "Units editor")
        units_action.triggered.connect(self.on_open_units_editor_dialog)
        close_app_action = file_menu.addAction(ICONS["exit"], "Quit")
        close_app_action.triggered.connect(self.on_quit_application)
        menubar.addMenu(file_menu)

        help_menu = QtWidgets.QMenu("&Help", self)
        about_action = help_menu.addAction(ICONS["about"],"About")
        about_action.triggered.connect(self.on_open_about_dialog)
        menubar.addMenu(help_menu)

    def _build_toolbar(self):
        """Builds the toolbar."""
        toolbar = self.addToolBar("Main")
        toolbar.setIconSize(QtCore.QSize(32, 32))

        load_files_action = toolbar.addAction(ICONS["load"], "Load Data")
        load_files_action.triggered.connect(self.on_load_data)

        units_action = toolbar.addAction(ICONS["units"], "Units editor")
        units_action.triggered.connect(self.on_open_units_editor_dialog)

        about_action = toolbar.addAction(ICONS["about"], "About")
        about_action.triggered.connect(self.on_open_about_dialog)

        close_app_action = toolbar.addAction(ICONS["exit"], "Quit")
        close_app_action.triggered.connect(self.on_quit_application)

    def _close(self):
        """Closes the application."""
        LOGGER["main"].removeHandler(self._logger_widget)
        LOGGER["popup"].removeHandler(self._logger_popup)
        self.destroy()

    def _plot_on_current_tab(self, axis_info: List[Dict[str, Any]], dataset_info: List[Dict[str, Any]]):
        """Plots some data in the current tab.

        Args:
            axis_info: the axis info of the data
            dataset_info: the dataset info
        """
        current_widget = self._tab_widget.currentWidget()
        if current_widget is None:
            return

        if not isinstance(current_widget, Plot1DWidget):
            log("Only 1D data can be overplotted", ["main", "popup"], "error")
            return

        if not dataset_info:
            return

        if dataset_info[0]["dimension"] >= 2:
            log("Incompatible plot types", ["main", "popup"], "error")
            return

        try:
            for x_info,y_info in zip(axis_info,dataset_info):
                current_widget.add_line(x_info, y_info)
        except Plot1DModelError as e:
            log(str(e), ["main", "popup"], "error")

    def _plot_on_new_tab(self, axis_info: List[Dict[str, Any]], dataset_info: List[Dict[str, Any]]):
        """Plots some data in a new tab.

        Args:
            axis_info: the axis info of the data
            dataset_info: the dataset info
        """
        if not dataset_info:
            return
                
        dimension = dataset_info[0]["dimension"]
        if dimension == 0:
            return
        else:
            try:
                if dimension == 1:
                    plot_widget = Plot1DWidget(self)
                    for x_info,y_info in zip(axis_info,dataset_info):
                        plot_widget.add_line(x_info, y_info)
                    icon = ICONS["plot_1d"]
                else:
                    plot_widget = PlotNDWidget(self)
                    plot_widget.update_data(axis_info, dataset_info[0])
                    icon = ICONS["plot_2d"]
            except Exception as e:
                log(str(e), ["main", "popup"], "error")
            else:
                plot_widget.plot_sent_on_current_tab.connect(self.on_update_current_tab)
                plot_widget.plot_sent_on_new_tab.connect(self.on_create_new_tab)
                self._tab_widget.addTab(plot_widget, icon, dataset_info[0]["variable"])
                self._tab_widget.setTabToolTip(self._tab_widget.count() - 1, f"Path: {dataset_info[0]['file']}")

    def add_data(self, filename: str):
        """Adds data to the data tree  of loaded files.

        Args:
            filename: the name of the file
        """
        try:
            data_model = self._data_widget.model()
            data_model.add_data(filename)
        except DataTreeModelError as e:
            log(str(e), ["main", "popup"], "error")
        else:
            log(f"File {filename} successfully opened for reading", ["main"], "info")

    def closeEvent(self, event: QtGui.QCloseEvent = None):
        """Handler for the close event.

        Args:
            event: the close event
        """
        self._close()
        sys.exit(0)

    def on_close_plot(self, index: int):
        """Closes a plot tab.

        Args:
            index: the index of the plot tab
        """
        widget = self._tab_widget.widget(index)
        widget.close()
        self._tab_widget.removeTab(index)

    def on_create_new_tab(self, axis_info: List[Dict[str, Any]], dataset_info: List[Dict[str, Any]]):
        """Creates a new tab.
        
        Args:
            axis_info: the axis info of the data
            dataset_info: the dataset info
        """
        self._plot_on_new_tab(axis_info, dataset_info)

    def on_load_data(self):
        """Loads some data."""
        extensions = " ".join([f"*{k}" for k in DATA_ITEMS.keys()])
        filter_mask = f"Data files {extensions}"
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                              "Open Data File(s)", "", filter_mask)
        for filename in filenames:
            self.add_data(filename)

    def on_open_about_dialog(self):
        """Opens the About dialog."""
        dlg = AboutDialog(self)
        dlg.exec()

    def on_open_units_editor_dialog(self):
        """Opens the units dialogs."""
        if self._units_dialog is None:
            self._units_dialog = UnitsEditorDialog(self)
            self._units_dialog.units_updated.connect(self.units_updated.emit)
        self._units_dialog.show()

    def on_plot_on_current_tab(self, axis_info: List[Dict[str, Any]], dataset_info: List[Dict[str, Any]]):
        """Plots data on the current tab.

        Args:
            axis_info: the axis info of the data
            dataset_info: the dataset info
        """
        self._plot_on_current_tab(axis_info,dataset_info)

    def on_plot_on_new_tab(self, axis_info: List[Dict[str, Any]], dataset_info: List[Dict[str, Any]]):
        """Plots data on a new tab.

        Args:
            axis_info: the axis info of the data
            dataset_info: the dataset info
        """
        self._plot_on_new_tab(axis_info,dataset_info)

    def on_preview_sent_on_current_tab(self):
        """Plots the preview on the current tab."""
        axis_info = self._data_widget.get_selected_dataset_axis_info()
        dataset_info = self._data_widget.get_selected_dataset_info()
        self._plot_on_current_tab(axis_info,[dataset_info])

    def on_preview_sent_on_new_tab(self):
        """Plots the preview on a new tab."""
        axis_info = self._data_widget.get_selected_dataset_axis_info()
        dataset_info = self._data_widget.get_selected_dataset_info()
        self._plot_on_new_tab(axis_info,[dataset_info])

    def on_quit_application(self):
        """Quits the application."""
        choice = QtWidgets.QMessageBox.question(
            self, "Quit", "Do you really want to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            self._close()

    def on_select_dataset(self, dataset_info: Dict[str, Any]):
        """Selects a dataset.

        Args:
            dataset_info: the information about the selected dataset
        """
        self._preview_widget.update_plot(dataset_info)

    def on_update_current_tab(self, axis_info: List[Dict[str, Any]], dataset_info: List[Dict[str, Any]]):
        """Updates the current tab.

        Args:
            axis_info: the axis info of the data
            dataset_info: the dataset info
        """
        self._plot_on_current_tab(axis_info, dataset_info)
