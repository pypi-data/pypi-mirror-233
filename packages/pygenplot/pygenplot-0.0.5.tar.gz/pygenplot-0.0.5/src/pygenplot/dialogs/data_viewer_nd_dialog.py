from qtpy import QtCore, QtGui, QtWidgets

from ..icons import ICONS
from ..models.plot_nd_model import PlotNDModel
from ..views.table_views import QTableViewWithoutRightClick


class DataViewerNDDialog(QtWidgets.QDialog):
    def __init__(self, plot_nd_model: PlotNDModel,parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_nd_model: the ND data model
            parent: the parent widget
        """
        super(DataViewerNDDialog, self).__init__(parent)

        self._plot_nd_model = plot_nd_model

        self._build()

        self.setWindowTitle("PyGenPlot - Data viewer")

        self.resize(400, 400)

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        self._data_table_view = QTableViewWithoutRightClick()
        self._data_table_view.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self._data_table_view.customContextMenuRequested.connect(self.on_open_contextual_menu)
        self._data_table_view.installEventFilter(self)
        main_layout.addWidget(self._data_table_view)

        hlayout = QtWidgets.QHBoxLayout()
        self._add_horizontal_header = QtWidgets.QCheckBox("Add horizontal header")
        self._add_vertical_header = QtWidgets.QCheckBox("Add vertical header")
        hlayout.addWidget(self._add_horizontal_header)
        hlayout.addWidget(self._add_vertical_header)
        main_layout.addLayout(hlayout)

        self.setLayout(main_layout)

        self._plot_nd_model.data_axis_changed.connect(self.on_update_table)
        self._plot_nd_model.model_updated.connect(self.on_update_table)
        self._add_horizontal_header.clicked.connect(self.on_set_horizontal_header)
        self._add_vertical_header.clicked.connect(self.on_set_vertical_header)

        self.on_update_table()

    def eventFilter(self, source: QtWidgets.QWidget, event: QtCore.QEvent):
        """Event filter for the dialog.

        Args:
            source: the widget triggering whose event should be filtered
            event: the event

        Returns:
            whether the event has been successfully filtered
        """
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.matches(QtGui.QKeySequence.StandardKey.Copy):
                self.on_copy_to_clipboard()
                return True

        return super(DataViewerNDDialog, self).eventFilter(source, event)

    def on_copy_to_clipboard(self):
        """Copies some data to the clipboard."""
        model = self._data_table_view.model()
        selection_model = self._data_table_view.selectionModel()

        selected_columns = set()
        for data_range in selection_model.selection():
            for i in range(data_range.top(), data_range.bottom() + 1):
                for j in range(data_range.left(), data_range.right() + 1):
                    selected_columns.add(j)
        selected_columns = sorted(selected_columns)

        copied_data = []
        for data_range in selection_model.selection():
            for i in range(data_range.top(), data_range.bottom() + 1):
                line = []
                for j in selected_columns:
                    if j in range(data_range.left(), data_range.right() + 1):
                        value = model.data(model.index(i, j), QtCore.Qt.ItemDataRole.DisplayRole)
                    else:
                        value = ""
                    line.append(value)
                line = ",".join(line)
                copied_data.append(line)

        copied_data = "\n".join(copied_data)

        QtWidgets.QApplication.clipboard().setText(copied_data)

    def on_open_contextual_menu(self, point: QtCore.QPoint):
        """Pops up the contextual menu.

        Args:
            point: the right-click point
        """
        menu = QtWidgets.QMenu(self)
        copy_to_clipboard_action = menu.addAction(ICONS["clipboard"], "Copy to clipboard")
        copy_to_clipboard_action.triggered.connect(self.on_copy_to_clipboard)
        menu.exec(self._data_table_view.mapToGlobal(point))

    def on_set_horizontal_header(self):
        """Sets the horizontal header."""
        model = self._data_table_view.model()
        if model is None:
            return

        header_data = (self._plot_nd_model.get_x_axis_data() if self._add_horizontal_header.isChecked()
                       else range(model.columnCount()))
        model.setHorizontalHeaderLabels([str(v) for v in header_data])

    def on_set_vertical_header(self):
        """Sets the vertical header."""
        model = self._data_table_view.model()
        if model is None:
            return

        header_data = (self._plot_nd_model.get_y_axis_data() if self._add_vertical_header.isChecked()
                       else range(model.rowCount()))
        model.setVerticalHeaderLabels([str(v) for v in header_data])

    def on_update_table(self):
        """Updates the table with the data."""
        y_data = self._plot_nd_model.get_y_axis_data()
        z_data = self._plot_nd_model.get_data()

        model = QtGui.QStandardItemModel()
        for row in z_data:
            model.appendRow([QtGui.QStandardItem(str(c)) for c in row])

        self._data_table_view.setModel(model)
        self.on_set_horizontal_header()
        self.on_set_vertical_header()
