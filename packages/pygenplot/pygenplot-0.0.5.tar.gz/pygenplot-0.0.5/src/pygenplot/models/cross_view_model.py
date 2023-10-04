from typing import Optional, Tuple

from qtpy import QtCore, QtWidgets

from ..models.plot_nd_model import PlotNDModel


class CrossViewModel(QtCore.QObject):

    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the underlying ND plot model
            parent: the parent widget
        """
        super(CrossViewModel, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._horizontal_slicers = []
        self._vertical_slicers = []

        self._visible_horizontal_slicer = None
        self._visible_vertical_slicer = None

        self._artists_activated = True

        self._plot_nd_model.slice_artists_activated.connect(self.on_activate_artists)

    def add_horizontal_slicer(self, y: float, color: Optional[Tuple[float, float, float]] = (1, 0, 0)):
        """Adds a horizontal slicer.

        Args:
            y: the Y position of the horizontal slicer
            color: the color of the slicer
        """
        line = self._plot_nd_model.figure.axes[0].axhline(y=y, color=color, linewidth=3)
        self._horizontal_slicers.append(line)
        self.select_horizontal_slicer(self._visible_horizontal_slicer)

        self._plot_nd_model.get_canvas().draw()

    def add_vertical_slicer(self, x: float, color: Optional[Tuple[float, float, float]] = (1, 0, 0)):
        """Adds a vertical slicer.

        Args:
            x: the X position of the vertical slicer
            color: the color of the slicer
        """
        line = self._plot_nd_model.figure.axes[0].axvline(x=x, color=color, linewidth=3)
        self._vertical_slicers.append(line)
        self.select_vertical_slicer(self._visible_vertical_slicer)

        self._plot_nd_model.get_canvas().draw()

    @property
    def artists_activated(self) -> bool:
        """Returns whether the artists are activated.

        Returns:
            whether the artists are activated
        """
        return self._artists_activated

    def clear(self):
        """Clears the model."""
        self.clear_horizontal_slicers()
        self.clear_vertical_slicers()

    def clear_horizontal_slicers(self):
        """Clears the horizontal slicers."""
        for slicer in self._horizontal_slicers:
            slicer.remove()
        self._horizontal_slicers.clear()
        self._visible_horizontal_slicer = None

        self._plot_nd_model.get_canvas().draw()

    def clear_vertical_slicers(self):
        """Clears the vertical slicers."""
        for slicer in self._vertical_slicers:
            slicer.remove()
        self._vertical_slicers.clear()
        self._visible_vertical_slicer = None

        self._plot_nd_model.get_canvas().draw()

    def on_activate_artists(self, state: bool):
        """Sets whether the artists should be activated.

        Args:
            whether the artists should be activated
        """
        self._artists_activated = state

        if self._vertical_slicers and self._visible_vertical_slicer is not None:
            self._vertical_slicers[self._visible_vertical_slicer].set_visible(state)

        if self._horizontal_slicers and self._visible_horizontal_slicer is not None:
            self._horizontal_slicers[self._visible_horizontal_slicer].set_visible(state)

        self._plot_nd_model.get_canvas().draw()

    def remove_horizontal_slicer(self, index: int):
        """Removes a horizontal slicer.

        Args:
            index: the index of the slicer
        """
        try:
            self._horizontal_slicers[index].remove()
            del self._horizontal_slicers[index]
        except IndexError:
            return
        else:
            if index == self._visible_horizontal_slicer:
                self._visible_horizontal_slicer = None
            self._plot_nd_model.get_canvas().draw()

    def remove_vertical_slicer(self, index: int):
        """Removes a vertical slicer.

        Args:
            index: the index of the slicer
        """
        try:
            self._vertical_slicers[index].remove()
            del self._vertical_slicers[index]
        except IndexError:
            return
        else:
            if index == self._visible_vertical_slicer:
                self._visible_vertical_slicer = None
            self._plot_nd_model.get_canvas().draw()

    def select_horizontal_slicer(self, index: Optional[int]):
        """Selects a horizontal slicer.

        Args:
            index: the index of the slicer
        """
        self.unselect_horizontal_slicers()
        if index is None:
            return

        try:
            self._horizontal_slicers[index].set_visible(True)
        except IndexError:
            return
        else:
            self._visible_horizontal_slicer = index
            self._plot_nd_model.get_canvas().draw()

    def select_vertical_slicer(self, index: Optional[int]):
        """Selects a vertical slicer.

        Args:
            index: the index of the slicer
        """
        self.unselect_vertical_slicers()
        if index is None:
            return

        try:
            self._vertical_slicers[index].set_visible(True)
        except IndexError:
            return
        else:
            self._visible_vertical_slicer = index
            self._plot_nd_model.get_canvas().draw()

    def set_horizontal_slicer_color(self, index: int, color: Tuple[float, float, float]):
        """Sets the color of a horizontal slicer.

        Args:
            index: the index of the horizontal slicer
            color: the color
        """
        try:
            self._horizontal_slicers[index].set_color(color)
        except IndexError:
            return
        else:
            self._plot_nd_model.get_canvas().draw()

    def set_vertical_slicer_color(self, index: int, color: Tuple[float, float, float]):
        """Sets the color of a vertical slicer.

        Args:
            index: the index of the vertical slicer
            color: the color
        """
        try:
            self._vertical_slicers[index].set_color(color)
        except IndexError:
            return
        else:
            self._plot_nd_model.get_canvas().draw()

    def unselect_horizontal_slicers(self):
        """Unselects all horizontal slicers."""
        for slicer in self._horizontal_slicers:
            slicer.set_visible(False)
        self._visible_horizontal_slicer = None
        self._plot_nd_model.get_canvas().draw()

    def unselect_vertical_slicers(self):
        """Unselects all vertical slicers."""
        for slicer in self._vertical_slicers:
            slicer.set_visible(False)
        self._visible_vertical_slicer = None
        self._plot_nd_model.get_canvas().draw()

