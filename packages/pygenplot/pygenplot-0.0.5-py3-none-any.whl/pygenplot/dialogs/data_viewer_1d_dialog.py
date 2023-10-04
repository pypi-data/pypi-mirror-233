import itertools

from qtpy import QtCore, QtGui, QtWidgets

from ..icons import ICONS
from ..models.plot_1d_model import Plot1DModel
from ..views.table_views import QTableViewWithoutRightClick


class DataViewer1DDialog(QtWidgets.QDialog):
    def __init__(self, plot_1d_model: Plot1DModel, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            plot_1d_model: the 1D data model
            parent: the parent widget
        """
        super(DataViewer1DDialog, self).__init__(parent)

        self._plot_1d_model = plot_1d_model

        self._build()

        self.setWindowTitle("PyGenPlot - Data viewer")

        self.resize(400, 400)

        self.on_update_table()

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        self._data_table_view = QTableViewWithoutRightClick()
        self._data_table_view.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self._data_table_view.customContextMenuRequested.connect(self.on_open_contextual_menu)
        self._data_table_view.installEventFilter(self)

        main_layout.addWidget(self._data_table_view)

        self.setLayout(main_layout)

        self._plot_1d_model.model_updated.connect(self.on_update_table)

    def eventFilter(self, source: QtWidgets.QWidget, event: QtCore.QEvent) -> bool:
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

        return super(DataViewer1DDialog, self).eventFilter(source, event)

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

        copied_data = [",".join([model.headerData(c, QtCore.Qt.Orientation.Horizontal) for c in selected_columns])]
        for data_range in selection_model.selection():
            for i in range(data_range.top(), data_range.bottom() + 1):
                line = []
                for j in selected_columns:
                    if j in range(data_range.left(), data_range.right() + 1):
                        value = model.data(model.index(i, j), QtCore.Qt.ItemDataRole.DisplayRole)
                    else:
                        value = ""
                    line.append(value)
                line = [l if l is not None else "" for l in line]
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

    def on_update_table(self):
        """Updates the table with the data."""
        n_lines = self._plot_1d_model.rowCount()

        x_data_labels = [self._plot_1d_model.get_x_axis_full_name()] * n_lines
        y_data_labels = self._plot_1d_model.get_line_full_names()
        column_names = list(itertools.chain(*zip(x_data_labels, y_data_labels)))

        model = QtGui.QStandardItemModel()
        for i in range(n_lines):
            x_data = self._plot_1d_model.data(self._plot_1d_model.index(i, 0), Plot1DModel.XDataRole)
            model.appendColumn([QtGui.QStandardItem(str(x)) for x in x_data])
            y_data = self._plot_1d_model.data(self._plot_1d_model.index(i, 0), Plot1DModel.YDataRole)
            model.appendColumn([QtGui.QStandardItem(str(y)) for y in y_data])
        model.setHorizontalHeaderLabels(column_names)

        self._data_table_view.setModel(model)
