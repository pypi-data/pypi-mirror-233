from qtpy import QtWidgets

from ..models.plot_nd_model import PlotNDModel


class PlotNDGeneralSettingsDialog(QtWidgets.QDialog):
    def __init__(self, plot_nd_model: PlotNDModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the ND data model
            parent: the parent widget
        """
        super(PlotNDGeneralSettingsDialog, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._build()

        self.on_update()

        self.setWindowTitle("PyGenPlot - General settings dialog")

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        titles_groupbox = QtWidgets.QGroupBox(self)
        titles_groupbox.setTitle("Titles")
        titles_groupbox_layout = QtWidgets.QFormLayout()
        figure_title_label = QtWidgets.QLabel("Figure")
        self._figure_title_lineedit = QtWidgets.QLineEdit()
        titles_groupbox_layout.addRow(figure_title_label, self._figure_title_lineedit)
        plot_title_label = QtWidgets.QLabel("Plot")
        self._plot_title_lineedit = QtWidgets.QLineEdit()
        titles_groupbox_layout.addRow(plot_title_label, self._plot_title_lineedit)
        titles_groupbox.setLayout(titles_groupbox_layout)
        main_layout.addWidget(titles_groupbox)

        self.setLayout(main_layout)

        self._figure_title_lineedit.textEdited.connect(self.on_editing_figure_title)
        self._plot_title_lineedit.textEdited.connect(self.on_editing_plot_title)

    def on_editing_figure_title(self, title: str):
        """Sets the figure title.

        Args:
            title: the new figure title
        """
        self._plot_nd_model.set_figure_title(title)

    def on_editing_plot_title(self, title: str):
        """Sets the plot title.

        Args:
            title: the new plot title
        """
        self._plot_nd_model.set_plot_title(title)

    def on_update(self):
        """Updates the dialog."""
        self._figure_title_lineedit.setText(self._plot_nd_model.get_figure_title())
        self._plot_title_lineedit.setText(self._plot_nd_model.get_plot_title())
