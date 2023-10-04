import os
from typing import Any, Dict, Optional, List, Union

import numpy as np

import h5py

from qtpy import QtCore, QtGui, QtWidgets

from ..data.units import UnitError, UnitsManager
from ..icons import ICONS


class DataItemError(Exception):
    pass


class DataTreeModelError(Exception):
    pass


class NodeItem:

    def __init__(self, element: Optional[Union[h5py.Dataset, h5py.File, h5py.Group]]):
        """Constructor.

        Args:
            element: the HDF or NetCDF element
        """
        self._element = element
        if self._element is None:
            self._path = None
            self._group = None
            self._name = None
            self._is_group = True
        else:
            self._path = element.name
            self._group = os.path.dirname(self._path)
            self._name = os.path.basename(self._path)
            self._is_group = isinstance(element, h5py.Group)

        self._parent = None

        self._children = []

    def _parse(self, starting_node: Any):
        """Retrieves recursively all the variables stored in an HDF file and builds the tree out of this.

        Args:
            starting_node: the starting node
        """
        for element in starting_node.values():
            new_node = NodeItem(element)
            self.add_child(new_node)
            if isinstance(element, h5py.Group):
                new_node._parse(element)

    @property
    def children(self) -> List['NodeItem']:
        """Returns the children nodes of the node.

        Returns:
            the children
        """
        return self._children

    @property
    def element(self) -> Any:
        """Returns the HDF or NetCDF element underlying the node.

        Returns:
            the element
        """
        return self._element

    @property
    def group(self) -> str:
        """Returns the group to which belongs the node.

        Returns:
            the group
        """
        return self._group

    @property
    def name(self) -> str:
        """Returns the name of the node.

        Returns:
            the name
        """
        return self._name

    @property
    def parent(self) -> 'NodeItem':
        """Returns the parent node of the node.

        Returns:
            the parent node
        """
        return self._parent

    @property
    def path(self) -> str:
        """Returns the path of the node.

        Returns:
            the path
        """
        return self._path

    def add_child(self, child: 'NodeItem'):
        """Appends a child to the current node.

        Args:
            child: the child to append
        """
        child._parent = self
        self._children.append(child)

    def child(self, row: int) -> 'NodeItem':
        """Returns the child node matching a given row.

        Args:
            row: the row

        Returns:
            the child node
        """
        return self._children[row]

    def child_count(self) -> int:
        """Returns the number of child of the node.

        Returns:
            the number of child
        """
        return len(self._children)

    def column_count(self) -> int:
        """Returns the number of columns of the node.

        Returns:
            the number of columns
        """
        return 1

    def get_data_item(self) -> Optional['DataItem']:
        """Returns the data node at the root of the node.

        Returns:
            the data node
        """
        if self._parent is None:
            return None

        if isinstance(self, DataItem):
            return self
        else:
            return self.parent.get_data_item()

    def get_filename(self) -> str:
        """Returns the filename of the node.

        Returns:
            the filename
        """
        data_item = self.get_data_item()
        return data_item.filename

    def get_registered_datasets(self, datasets: Optional[List[str]] = None) -> List[str]:
        """Retrieves recursively all the datasets registered under this node.

        Args:
            datasets: the registered datasets.

        Returns:
            the registered datasets
        """
        if datasets is None:
            datasets = []

        for child in self._children:
            if child.is_group():
                child.get_registered_datasets(datasets)
            else:
                datasets.append(child.path)

        return datasets

    def is_group(self) -> bool:
        """Returns whether the node is a group.

        Returns:
            whether the node is a group
        """
        return self._is_group

    def remove_child(self, row: int):
        """Removes a child of the node.

        Args:
            row: the index of the child to remove
        """
        del self._children[row]

    def row(self) -> int:
        """Returns the row of this item regarding its parent.

        Returns:
            the row
        """
        return self._parent.children.index(self) if self._parent else 0


class DataItem(NodeItem):

    def __del__(self):
        """Deletes the object."""
        self._file.close()

    def __init__(self, filename: str):
        """Constructor.

        Args:
            filename: the HDF or NetCDF filename
        """
        try:
            self._file = h5py.File(filename, "r")
        except Exception as e:
            raise DataTreeModelError(str(e))

        super(DataItem, self).__init__(self._file)

        self._filename = filename

        self._name = os.path.basename(self._filename)

        self._parse(self._file)

    @staticmethod
    def _build_index_variable(size: int) -> Dict[str, Any]:
        """Builds an index variable of a given size. An index variable is a variable used to
        build axis of type 'index'.

        Args:
            size: the size of the index variable

        Returns:
            the information about the index variable
        """
        data = np.arange(size,dtype=np.float64)
        info = {
            "variable": "index",
            "plottable": True,
            "axis": ["index"],
            "units": "au",
            "dimension": data.ndim,
            "shape": data.shape,
            "path": None, "data": data
        }

        return info

    @property
    def filename(self) -> str:
        """Returns the filename stored in the DataItem.

        Returns:
            the filename
        """
        return self._filename

    def get_axis_data(self, variable_info: Dict[str,Any]) -> List[Dict[str, Any]]:
        """Gets the axis data info of a given variable.

        Args:
            variable_info: the information about the variable for which the axis should be obtained.

        Returns:
            the axis information for each axis of the given variable
        """
        registered_datasets = self.get_registered_datasets()

        axis = variable_info["axis"]
        shape = variable_info["shape"]

        axis_data = []
        for i, ax in enumerate(axis):
            if ax == "index":
                index_data = DataItem._build_index_variable(shape[i])
                axis_data.append(index_data)
            else:
                for d in registered_datasets:
                    dinfo = self.get_dataset_info(d, add_data=True)
                    if dinfo["variable"] == ax:
                        axis_data.append(dinfo)
                        break
                else:
                    index_data = DataItem._build_index_variable(shape[i])
                    axis_data.append(index_data)
        return axis_data

    def get_dataset_info(self, dataset: str, add_data: bool = False) -> Dict[str, Any]:
        """Returns the information about a given dataset.

        Args:
            dataset: the dataset
            add_data: whether the actual data will be added to the information

        Returns:
            the information about the dataset
        """
        hdf_variable = self._file[dataset]

        info = {"file": self._filename,
                "plottable": True,
                "path": dataset,
                "status": dataset,
                "variable": os.path.basename(hdf_variable.name),
                "units": hdf_variable.attrs.get("units", b"au").decode("utf-8")}

        # Check units
        try:
            _ = UnitsManager.measure(1.0,info["units"], equivalent=True)
        except UnitError:
            info["plottable"] = False
            info["status"] = "unknown unit"

        # Check shape
        info["original_shape"] = hdf_variable.shape
        if hdf_variable.ndim > 1:
            info["shape"] = tuple([s for s in hdf_variable.shape if s > 1])
            if not info["shape"]:
                info["shape"] = (1,)
        elif hdf_variable.ndim == 1:
            info["shape"] = hdf_variable.shape            
        else:
            info["shape"] = (1,)

        info["dimension"] = len(info["shape"])
        if "axis" in hdf_variable.attrs:
            if isinstance(hdf_variable.attrs["axis"],bytes):
                info["axis"] = hdf_variable.attrs["axis"].decode("utf-8").split("|")
            else:
                info["axis"] = hdf_variable.attrs["axis"].split("|")
        else:
            info["axis"] = ["index"] * info["dimension"]

        # Check type
        if np.issubdtype(hdf_variable.dtype,np.number):
            info["type"] = hdf_variable.dtype.name
        else:
            info["type"] = "str"
            info["plottable"] = False
            info["status"] = "invalid data type"

        if add_data:
            if hdf_variable.ndim > 1:
                info["data"] = np.squeeze(hdf_variable[:])
                if not info["data"].shape:
                    info["data"] = np.expand_dims(info["data"], axis=0)
            elif hdf_variable.ndim == 1:
                info["data"] = hdf_variable[:]
            else:
                info["data"] = np.expand_dims(hdf_variable[:], axis=0)

        return info


class DataTreeModel(QtCore.QAbstractItemModel):

    DatasetInfoRole = QtCore.Qt.ItemDataRole.UserRole

    DatasetShortInfoRole = QtCore.Qt.ItemDataRole.UserRole + 1

    AxisInfoRole = QtCore.Qt.ItemDataRole.UserRole + 2

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(DataTreeModel, self).__init__(parent)

        self._root = NodeItem(None)

    def _search_node(self, node: NodeItem, filename: str, dataset: str) -> Optional[NodeItem]:
        """Searches recursively for a node whose path matches a given filename and dataset.

        Args:
            node: the current node
            filename: the filename
            dataset: the dataset

        Returns:
            the node item if one that matches the path if found, None otherwise
        """
        if node.is_group():
            for child in node.children:
                temp = self._search_node(child, filename, dataset)
                if temp is not None:
                    return temp
        else:
            if node.get_filename() == filename and node.path == dataset:
                return node
        
        return None

    def add_data(self, filename: str):
        """Adds a data to the model.

        Args:
            filename: the filename of the data to add
        """
        ext = os.path.splitext(filename)[1]
        data_tree_item_class = DATA_ITEMS.get(ext, None)
        if data_tree_item_class is None:
            return

        try:
            data_item = data_tree_item_class(filename)
        except DataItemError:
            raise DataTreeModelError(f"The file {filename} could not be opened for reading")
        else:
            self._root.add_child(data_item)
            self.layoutChanged.emit()

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex(), *args, **kwargs) -> int:
        """Returns the number of columns of the model.

        Args:
            parent: the parent model

        Returns:
            the number of columns
        """
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self._root.column_count()

    def data(self, index: QtCore.QModelIndex = QtCore.QModelIndex(), role: int = QtCore.Qt.DisplayRole) -> Any:
        """Returns the data for a given index and role

        Args:
            index: the index
            role: the role

        Returns:
            the data
        """
        if not index.isValid():
            return None

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            node = index.internalPointer()
            return node.name

        elif role == QtCore.Qt.ItemDataRole.DecorationRole:
            node = index.internalPointer()
            if node.is_group():
                return ICONS["group"]
            else:
                return ICONS["data"]

        elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
            node = index.internalPointer()
            if node.is_group():
                return None
            else:
                data_item = self.get_data_item(node)
                variable_info = data_item.get_dataset_info(node.path,False)
                return QtGui.QColor("black") if variable_info["plottable"] else QtGui.QColor("red")

        elif role == QtCore.Qt.ItemDataRole.ToolTipRole:
            node = index.internalPointer()
            if node.is_group():
                return node.path
            else:
                data_item = self.get_data_item(node)
                variable_info = data_item.get_dataset_info(node.path,False)
                info = "\n".join([f"{k}: {v}" for k, v in variable_info.items()])
                return info

        elif role == DataTreeModel.DatasetInfoRole:
            node = index.internalPointer()
            if node.is_group():
                return None
            data_item = self.get_data_item(node)
            variable_info = data_item.get_dataset_info(node.path, True)
            return variable_info
        
        elif role == DataTreeModel.DatasetShortInfoRole:
            node = index.internalPointer()
            if node.is_group():
                return None
            data_item = self.get_data_item(node)
            variable_info = data_item.get_dataset_info(node.path, False)
            return variable_info

        elif role == DataTreeModel.AxisInfoRole:
            node = index.internalPointer()
            if node.is_group():
                return None
            else:
                data_item = self.get_data_item(node)
                variable_info = data_item.get_dataset_info(node.path, False)
                axis_data = data_item.get_axis_data(variable_info)
                return axis_data

        else:
            return None

    def get_data_item(self, node: Union[DataItem, NodeItem]) -> DataItem:
        """Returns the data item of a given node.

        Args:
            node: the node

        Returns:
            the data item
        """
        if node.parent == self._root:
            return node
        else:
            return self.get_data_item(node.parent)

    def get_index_from_path_and_dataset(self, filename: str, dataset: str) -> QtCore.QModelIndex:
        """Returns the index of the node matching a given filename and dataset.

        Args:
            filename: the filename
            dataset: the dataset

        Returns:
            the matching index
        """
        node = self._search_node(self._root, filename, dataset)
        if node is None:
            index = QtCore.QModelIndex()
        else:
            index = self.createIndex(node.row(), 0, node)
        return index

    def get_root_item(self) -> NodeItem:
        """Returns the root item.

        Returns:
            the root item
        """
        return self._root

    def index(self, row: int, column: int, _parent: QtCore.QModelIndex = None, *args, **kwargs) -> QtCore.QModelIndex:
        """Returns the index of an item matching a given row and column.

        Args:
            row: the row
            column: the column
            _parent: the parent of the item

        Returns:
            the index matching the given row and column
        """
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()

        if not QtCore.QAbstractItemModel.hasIndex(self,row,column,_parent):
            return QtCore.QModelIndex()

        child = parent.child(row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex = QtCore.QModelIndex()) -> QtCore.QModelIndex:
        """Returns the index of the parent of an item matching a given index.

        Args:
            index: the index of the item

        Returns:
            the index of the parent
        """
        if index.isValid():
            p = index.internalPointer().parent
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def removeRow(self, row: int, parent: QtCore.QModelIndex = QtCore.QModelIndex, *args, **kwargs) -> bool:
        """Removes a row of the model according to a given parent.

        Args:
            row: the row to remove
            parent: the index of the parent

        Returns:
             whether the removal was successful
        """
        if not parent.isValid():
            return False

        parent_node = parent.internalPointer()
        if parent_node != self._root:
            return False

        self.beginRemoveRows(parent,row,row)
        parent_node.remove_child(row)
        self.endRemoveRows()

        return True

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex(), *args, **kwargs) -> int:
        """Returns the number of rows under a given parent.

        Args:
            parent: the parent index

        Returns:
            the number of rows
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()    


DATA_ITEMS = {'.hdf': DataItem,
              '.h5': DataItem,
              '.nxs': DataItem,
              '.nc': DataItem,
              '.cdf': DataItem,
              '.netcdf': DataItem}
