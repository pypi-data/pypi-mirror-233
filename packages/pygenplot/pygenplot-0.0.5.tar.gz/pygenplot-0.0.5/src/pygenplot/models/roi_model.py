from typing import Any, Optional

from matplotlib.backend_bases import KeyEvent, MouseEvent
from matplotlib.widgets import RectangleSelector

from qtpy import QtCore, QtGui, QtWidgets

from ..kernel.roi import ROI
from ..models.plot_nd_model import PlotNDModel


class ROIModelError(Exception):
    pass


class ROIModel(QtCore.QAbstractListModel):
    roi_selected = QtCore.Signal(QtCore.QModelIndex)

    roi_added = QtCore.Signal(QtCore.QModelIndex)

    roi_modified = QtCore.Signal(QtCore.QModelIndex)

    ROIRole = QtCore.Qt.ItemDataRole.UserRole

    ROIColorRole = QtCore.Qt.ItemDataRole.UserRole + 1

    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget = None):
        """Constructor.

        Args:
            plot_nd_model: the underlying ND plot model
            parent: the parent of the model
        """
        super(ROIModel, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._roi_selector = None

        self._rois = []

        self._artists_activated = True

        self._plot_nd_model.roi_artists_activated.connect(self.on_activate_artists)

        self._grab_tolerance = 10

    def _create_new_roi(self):
        """Creates a new ROI."""
        self._under_construction_roi = ROI(self._plot_nd_model)
        self._under_construction_roi.roi_added.connect(self.on_add_roi)
        self._under_construction_roi.roi_selected.connect(self.on_select_roi)
        self._under_construction_roi.roi_modified.connect(self.on_modify_roi)

    @property
    def artists_activated(self) -> bool:
        """Returns whether the artists are activated.

        Returns:
            whether the artists are activated
        """
        return self._artists_activated

    def clear(self):
        """Clears the model from the registered ROIs."""
        for roi in self._rois:
            roi.remove()
        self._rois = []

        if hasattr(self, "_roi_selector"):
            self._roi_selector.clear()
            delattr(self, "_roi_selector")

        self._plot_nd_model.get_canvas().draw()

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        """Returns the data for a given index and role.

        Args:
            index: the index
            role: the role

        Returns:
            the data
        """
        if not index.isValid():
            return None

        if not self._rois:
            return None

        row = index.row()
        roi = self._rois[row]

        if roi.state == roi.UNDER_CREATION:
            return None

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return roi.name
        elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
            r, g, b, _ = roi.get_facecolor()
            color = QtGui.QColor(r * 255, g * 255, b * 255)
            return color

        elif role == ROIModel.ROIRole:
            return roi

        else:
            return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        """Returns the flags of a given index.

        Args:
            index: the index

        Returns:
            the flag
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def get_selected_roi_index(self) -> Optional[int]:
        """Returns the selected roi index. None if no line is selected.

        Returns:
            the selected roi index.
        """
        for i, roi in enumerate(self._rois):
            if roi.state == roi.SELECTED:
                return i
        else:
            return None

    def init(self):
        """Initializes the model."""
        self._create_new_roi()

        dataset_info = self._plot_nd_model.get_dataset_info()
        min_dim = min(dataset_info[0]["shape"])
        self._grab_tolerance = min_dim/10.0

        self._roi_selector = RectangleSelector(
            self._plot_nd_model.figure.axes[0],
            self._under_construction_roi.draw_roi,
            useblit=False,
            button=[1],
            grab_range=self._grab_tolerance,
            spancoords="pixels",
            minspanx=10,
            minspany=10,
            interactive=True,
            drag_from_anywhere=True,
            ignore_event_outside=False,
        )

    def on_activate_artists(self, state: bool):
        """Sets whether the artists should be activated.

        Args:
            whether the ROi should be activated
        """
        self._artists_activated = state

        for roi in self._rois:
            roi.set_visible(state)

        self._plot_nd_model.get_canvas().draw()

    def on_add_roi(self, roi: ROI):
        """Adds a new roi to the model.

        Args:
            roi: the ROI to add
        """
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._rois.append(roi)
        self.endInsertRows()

        self._create_new_roi()
        self._roi_selector.clear()
        self._roi_selector.onselect = self._under_construction_roi.draw_roi

        self.roi_added.emit(self.index(len(self._rois) - 1, 0))

    def on_button_press(self, event: MouseEvent):
        """Event handler for mouse press event.
        
        Args:
            event: the mouse press event
        """
        canvas = self._plot_nd_model.get_canvas()
        canvas.setFocus(True)

        if not self._artists_activated:
            return

        if event.dblclick:
            return

        # Check if a ROI is selected
        selected_roi = None
        for roi in self._rois:
            if roi.state == roi.SELECTED:
                selected_roi = roi
                break

        if selected_roi:
            # If click is around selected ROI, do nothing
            if selected_roi.contains(event, tolerance=self._grab_tolerance):
                self._roi_selector.ignore_event_outside = True
                return
            else:
                self._roi_selector.ignore_event_outside = False

        # For non-selected ROIs, check if click is inside a ROI
        one_selected = False
        for roi in self._rois:
            if (roi.contains(event)) and (not one_selected) and (roi != selected_roi):
                roi.select_roi()
                if selected_roi:
                    selected_roi.unselect_roi()
                one_selected = True
                self._roi_selector.onselect = roi.draw_roi
                bbox = roi.get_bbox()
                self._roi_selector.extents = (bbox.x0, bbox.x1, bbox.y0, bbox.y1)
                self._roi_selector.set_visible(True)
                canvas.draw()
            else:
                roi.unselect_roi()

        if not one_selected:
            self._roi_selector.onselect = self._under_construction_roi.draw_roi
            self.on_select_roi(None)

    def on_key_press(self, event: KeyEvent):
        """Event handler for key press event.

        Args:
            event: the keypress event
        """
        if not self._artists_activated:
            return

        if not self._rois:
            return

        selected_roi = None
        for roi in self._rois:
            if roi.state == roi.SELECTED:
                selected_roi = roi
                break

        key = event.key
        if key == "n":
            index = self._rois.index(selected_roi) if selected_roi is not None else 0
            index = (index + 1) % len(self._rois)
            roi = self._rois[index]
            self.select_roi(roi)
            return
        elif key == "p":
            index = self._rois.index(selected_roi) if selected_roi is not None else 0
            index = (index - 1) % len(self._rois)
            roi = self._rois[index]
            self.select_roi(roi)
            return
        else:
            if selected_roi is None:
                return

            incr = None
            if key in ["shift+left", "shift+right", "shift+down", "shift+up"]:
                incr = 10
            elif key in ["left", "right", "down", "up"]:
                incr = 1
            else:
                pass

            if incr is not None:
                bbox = selected_roi.get_bbox()
                if key == "left":
                    x0 = bbox.x0 - incr
                    x1 = bbox.x1 - incr
                    y0 = bbox.y0
                    y1 = bbox.y1
                elif key == "right":
                    x0 = bbox.x0 + incr
                    x1 = bbox.x1 + incr
                    y0 = bbox.y0
                    y1 = bbox.y1
                elif key == "up":
                    x0 = bbox.x0
                    x1 = bbox.x1
                    y0 = bbox.y0 + incr
                    y1 = bbox.y1 + incr
                else:
                    x0 = bbox.x0
                    x1 = bbox.x1
                    y0 = bbox.y0 - incr
                    y1 = bbox.y1 - incr
                selected_roi.move_roi(x0, y0, x1, y1)
                self._roi_selector.extents = (x0, x1, y0, y1)

    def on_modify_roi(self, roi: ROI):
        """Emits that a ROI has been modified.

        Args:
            roi: the modified ROI
        """
        index = QtCore.QModelIndex()
        try:
            index = self.index(self._rois.index(roi), 0)
        except ValueError:
            pass
        finally:
            self.roi_modified.emit(index)

    def on_select_roi(self, roi: Optional[ROI]):
        """Emits that a ROI has been selected.
        
        Args:
            roi: the selected ROI
        """
        index = QtCore.QModelIndex()
        color = ROI.DEFAULT_COLOR
        try:
            index = self.index(self._rois.index(roi), 0)
            color = roi.get_facecolor()
        except ValueError:
            pass
        finally:
            self._roi_selector.artists[0].set_facecolor(color)
            self.roi_selected.emit(index)

    def removeRow(self, row: int, parent:QtCore.QModelIndex = None, *args, **kwargs) -> bool:
        """Removes a row from the model.

        Args:
            row: the index of the row to be removed
            parent: the parent

        Returns:
            whether the removal was successful
        """
        if row < 0 or row >= self.rowCount():
            return False

        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        self._rois[row].remove()
        del self._rois[row]
        self.endRemoveRows()

        self._roi_selector.clear()

        return True

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex(), *args, **kwargs) -> int:
        """Returns the number of ROIs stored in the model.

        Args:
            parent: the parent object

        Returns:
            the number of ROIs stored in the model
        """
        return len(self._rois)

    def select_roi(self, selected_roi):
        """Selects a ROI."""
        if selected_roi is None:
            # No ROI is selected
            self._roi_selector.clear()
            self.roi_selected.emit(QtCore.QModelIndex())
            self._roi_selector.onselect = self._under_construction_roi.draw_roi
        else:

            canvas = self._plot_nd_model.get_canvas()

            for roi in self._rois:
                if selected_roi == roi:
                    selected_roi.select_roi()
                    self._roi_selector.onselect = roi.draw_roi
                    bbox = roi.get_bbox()
                    self._roi_selector.extents = (bbox.x0, bbox.x1, bbox.y0, bbox.y1)
                    self._roi_selector.set_visible(True)
                    canvas.draw()
                else:
                    roi.unselect_roi()

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = QtCore.Qt.DisplayRole) -> bool:
        """Sets the data of the model.

        Args:
            index: the index
            value: the value
            role: the role

        Returns:
            whether settings the data was successful
        """
        if not index.isValid():
            return False

        row = index.row()
        if role == ROIModel.ROIColorRole:
            roi = self._rois[row]
            old_color = roi.get_facecolor()
            new_color = value + (old_color[3],)
            roi.set_facecolor(new_color)
            self._roi_selector.artists[0].set_facecolor(new_color)
            self._plot_nd_model.get_canvas().draw()
            return True
        return False
