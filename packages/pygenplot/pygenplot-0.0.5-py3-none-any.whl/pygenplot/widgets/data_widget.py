import re
from typing import Any, Dict, List, Optional

from qtpy import QtCore, QtWidgets

from ..icons import ICONS
from ..models.data_tree_model import DataTreeModel


class DataWidget(QtWidgets.QWidget):
    dataset_selected = QtCore.Signal(dict)

    plot_sent_on_new_tab = QtCore.Signal(list,list)

    plot_sent_on_current_tab = QtCore.Signal(list,list)

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(DataWidget, self).__init__(parent)

        self._build()

    def _build(self):
        """Builds the widget."""
        main_layout = QtWidgets.QVBoxLayout()

        self._data_treeview = QtWidgets.QTreeView()
        self._data_treeview.setHeaderHidden(True)
        self._data_treeview.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        data_model = DataTreeModel(self)
        self._data_treeview.setModel(data_model)

        main_layout.addWidget(self._data_treeview)

        self._selected_dataset_lineedit = QtWidgets.QLineEdit()
        main_layout.addWidget(self._selected_dataset_lineedit)

        self.setLayout(main_layout)

        data_model.layoutChanged.connect(self.on_update_completer)
        self._data_treeview.clicked.connect(self.on_select_tree_item)
        self._data_treeview.doubleClicked.connect(self.on_plot_on_new_tab)
        self._data_treeview.customContextMenuRequested.connect(self.on_open_contextual_menu)

    def eventFilter(self, source: QtWidgets.QWidget, event: QtCore.QEvent) -> bool:
        """Event filter for the dialog.

        Args:
            source: the widget triggering whose event should be filtered
            event: the event

        Returns:
            whether the event has been successfully filtered
        """
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Delete:
                if source == self._data_treeview:
                    current_index = self._data_treeview.currentIndex()
                    self._data_treeview.model().removeRow(current_index.row(), current_index.parent())
        return super(DataWidget, self).eventFilter(source, event)

    def get_selected_dataset_axis_info(self) -> List[Dict[str, Any]]:
        """Returns the axis info of a selected widget.

        Returns:
            the axis info
        """
        model = self._data_treeview.model()
        current_index = self._data_treeview.currentIndex()
        axis_dataset_info = model.data(current_index, DataTreeModel.AxisInfoRole)
        return axis_dataset_info

    def get_selected_dataset_info(self, add_data: bool = True) -> Optional[Dict[str, Any]]:
        """Returns the info about a selected dataset.

        Args:
            add_data: whether the data will be added to the info

        Returns:
            the information
        """
        model = self._data_treeview.model()
        current_index = self._data_treeview.currentIndex()
        node = current_index.internalPointer()
        if node.is_group():
            return None

        else:
            if add_data:
                dataset_info = model.data(current_index, DataTreeModel.DatasetInfoRole)
            else:
                dataset_info = model.data(current_index, DataTreeModel.DatasetShortInfoRole)
            return dataset_info

    def model(self) -> DataTreeModel:
        """Returns the model underlying the widget.

        Args:
            the model
        """
        return self._data_treeview.model()

    def on_dataset_autocomplete(self):
        """Selects the proposed autocompletion hint."""
        selected_dataset = self._selected_dataset_lineedit.text()
        if not selected_dataset:
            return

        match = re.match(r"^(.*) \((.*)\)$", selected_dataset)
        if match is None:
            return

        try:            
            dataset,filename = match.groups()
        except ValueError:
            return
        else:
            dataset = dataset.strip()
            filename = filename.strip()
        
        datatree_model = self._data_treeview.model()
        index = datatree_model.get_index_from_path_and_dataset(filename, dataset)
        if not index.isValid():
            return

        self._data_treeview.setCurrentIndex(index)

        dataset_info = self.get_selected_dataset_info()
        self.dataset_selected.emit(dataset_info)

        QtCore.QTimer.singleShot( 0, lambda: self._selected_dataset_lineedit.home(False))

    def on_dataset_highlighted(self):
        """Sets the selected dataset entry text to its beginning once a dataset has been selected through
        the completer."""
        QtCore.QTimer.singleShot(0, lambda: self._selected_dataset_lineedit.home(False))

    def on_open_contextual_menu(self, point: QtCore.QPoint):
        """Pops up a contextual menu.

        Args:
            point: the right-click point
        """
        current_index = self._data_treeview.currentIndex()
        node = current_index.internalPointer()
        if node is None or node.is_group():
            return

        dataset_info = self.get_selected_dataset_info(False)

        menu = QtWidgets.QMenu(self)
        plot_on_new_tab_action = menu.addAction(ICONS["data"], "Plot in new tab")
        plot_on_new_tab_action.triggered.connect(self.on_plot_on_new_tab)
        if dataset_info["dimension"] == 1:
            plot_on_current_tab_action = menu.addAction(ICONS["data"], "Plot in current tab")
            plot_on_current_tab_action.triggered.connect(self.on_plot_on_current_tab)
        menu.exec(self._data_treeview.mapToGlobal(point))

    def on_plot_on_current_tab(self):
        """Plots the data in a new tab."""
        dataset_info = self.get_selected_dataset_info()
        axis_info = self.get_selected_dataset_axis_info()
        self.plot_sent_on_current_tab.emit(axis_info,[dataset_info])

    def on_plot_on_new_tab(self):
        """Plots the data in a new tab."""
        dataset_info = self.get_selected_dataset_info()
        if dataset_info is None:
            return
        axis_info = self.get_selected_dataset_axis_info()
        self.plot_sent_on_new_tab.emit(axis_info,[dataset_info])

    def on_select_tree_item(self, index: QtCore.QModelIndex):
        """Selects a tree item.

        Args:
            index: the index of the item
        """
        node = index.internalPointer()
        if node.is_group():
            return
        else:
            dataset_info = self.get_selected_dataset_info()
            self._selected_dataset_lineedit.setText(f"{dataset_info['path']} ({dataset_info['file']})")
            self._selected_dataset_lineedit.setCursorPosition(0)
            self.dataset_selected.emit(dataset_info)

    def on_update_completer(self):
        """Updates the data completer."""
        data_model = self._data_treeview.model()
        root_item = data_model.get_root_item()
        data_nodes = root_item.children
        datasets = [f"{dataset} ({data_node.get_filename()})" for data_node in data_nodes for dataset in data_node.get_registered_datasets()]
        datasets.sort()
        completer = QtWidgets.QCompleter(datasets)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        completer.activated.connect(self.on_dataset_autocomplete)
        completer.highlighted.connect(self.on_dataset_highlighted)
        self._selected_dataset_lineedit.setCompleter(completer)

    def update_unit(self):
        """Updates the model according to a change in units."""
        data_model = self._data_treeview.model()
        data_model.layoutChanged.emit()