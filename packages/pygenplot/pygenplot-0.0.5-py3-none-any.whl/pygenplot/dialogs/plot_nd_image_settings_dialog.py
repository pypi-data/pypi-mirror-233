from qtpy import QtWidgets

from ..models.plot_nd_model import PlotNDModel


class PlotNDImageSettingsDialog(QtWidgets.QDialog):
    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the ND data model
            parent: the parent widget
        """
        super(PlotNDImageSettingsDialog, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._build()

        self._update()

        self.setWindowTitle("PyGenPlot - Image settings dialog")

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        vlayout = QtWidgets.QVBoxLayout()
        image_groupbox = QtWidgets.QGroupBox("Image")
        image_layout = QtWidgets.QFormLayout()
        aspect_label = QtWidgets.QLabel("Aspect")
        self._aspect_combobox = QtWidgets.QComboBox()
        image_layout.addRow(aspect_label, self._aspect_combobox)
        interpolation_label = QtWidgets.QLabel("Interpolation")
        self._interpolation_combobox = QtWidgets.QComboBox()
        image_layout.addRow(interpolation_label, self._interpolation_combobox)
        cmap_label = QtWidgets.QLabel("Color map")
        self._cmap_combobox = QtWidgets.QComboBox()
        image_layout.addRow(cmap_label, self._cmap_combobox)
        show_colorbar_label = QtWidgets.QLabel("Add colorbar")
        self._show_colorbar_checkbox = QtWidgets.QCheckBox("")
        image_layout.addRow(show_colorbar_label, self._show_colorbar_checkbox)
        image_groupbox.setLayout(image_layout)
        vlayout.addWidget(image_groupbox)

        main_layout.addLayout(vlayout)

        self.setLayout(main_layout)

        self._aspect_combobox.activated.connect(self.on_change_aspect)
        self._interpolation_combobox.activated.connect(self.on_change_interpolation)
        self._cmap_combobox.activated.connect(self.on_change_cmap)

        self._show_colorbar_checkbox.stateChanged.connect(self.on_show_colorbar)

    def _update(self):
        """Updates the dialog."""
        self._aspect_combobox.clear()
        self._aspect_combobox.addItems(PlotNDModel.aspects)
        self._aspect_combobox.setCurrentText(self._plot_nd_model.get_aspect())

        self._interpolation_combobox.clear()
        self._interpolation_combobox.addItems(PlotNDModel.interpolations)
        self._interpolation_combobox.setCurrentText(self._plot_nd_model.get_interpolation())

        self._cmap_combobox.clear()
        self._cmap_combobox.addItems(PlotNDModel.cmaps)
        self._cmap_combobox.setCurrentText(self._plot_nd_model.get_cmap())

        self._show_colorbar_checkbox.setChecked(self._plot_nd_model.get_show_colorbar())

    def on_change_aspect(self):
        """Changes the aspect of the figure."""
        self._plot_nd_model.set_aspect(self._aspect_combobox.currentText())

    def on_change_cmap(self):
        """Changes the image colormap."""
        self._plot_nd_model.set_cmap(self._cmap_combobox.currentText())

    def on_change_interpolation(self):
        """Changes the image interpolation scheme."""
        self._plot_nd_model.set_interpolation(self._interpolation_combobox.currentText())

    def on_show_colorbar(self, state: bool):
        """Shows/unshows the colorbar.

        Args:
            state: whether the colorbar should be shown
        """
        self._plot_nd_model.set_show_colorbar(state)
