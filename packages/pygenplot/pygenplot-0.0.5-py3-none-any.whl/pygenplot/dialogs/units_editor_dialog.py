import bisect
import copy

import numpy as np

from qtpy import QtCore, QtGui, QtWidgets

from ..data.units import UnitsManager


class UnitsEditorDialog(QtWidgets.QDialog):

    units_updated = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(UnitsEditorDialog,self).__init__(parent)

        self._edited_units = copy.deepcopy(UnitsManager.get_units())

        self._build()

    def _build(self):
        """Builds the dialog."""
        main_layout = QtWidgets.QVBoxLayout()

        hlayout = QtWidgets.QHBoxLayout()

        vlayout = QtWidgets.QVBoxLayout()

        self._units_listview = QtWidgets.QListView()
        self._units_listview.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self._units_listview.installEventFilter(self)
        vlayout.addWidget(self._units_listview)

        units_model = QtGui.QStandardItemModel()
        units = sorted(self._edited_units.keys())
        for u in units:
            units_model.appendRow(QtGui.QStandardItem(u))
        self._units_listview.setModel(units_model)
        self._units_listview.selectionModel().currentRowChanged.connect(self.on_select_unit)

        self._new_unit_pushbutton = QtWidgets.QPushButton("New unit")
        vlayout.addWidget(self._new_unit_pushbutton)

        hlayout.addLayout(vlayout)

        unit_definition_groupbox = QtWidgets.QGroupBox()
        unit_definition_groupbox.setTitle("Definition")
        unit_definition_groupbox_layout = QtWidgets.QFormLayout()
        unit_definition_groupbox.setLayout(unit_definition_groupbox_layout)
        label = QtWidgets.QLabel("Factor")
        self._factor_doublespinbox = QtWidgets.QDoubleSpinBox()
        self._factor_doublespinbox.setMinimum(-np.inf)
        self._factor_doublespinbox.setMaximum(np.inf)
        self._factor_doublespinbox.setDecimals(20)
        self._factor_doublespinbox.setSingleStep(1.0e-20)
        self._factor_doublespinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self._factor_doublespinbox.setFixedWidth(200)
        self._factor_doublespinbox.editingFinished.connect(self.on_update_unit)
        unit_definition_groupbox_layout.addRow(label,self._factor_doublespinbox)
        self._dimension_spinboxes = {}
        for si_unit in UnitsManager.UNAMES:
            label = QtWidgets.QLabel(si_unit)
            self._dimension_spinboxes[si_unit] = QtWidgets.QSpinBox()
            self._dimension_spinboxes[si_unit].setMinimum(-100)
            self._dimension_spinboxes[si_unit].setMaximum(100)
            self._dimension_spinboxes[si_unit].editingFinished.connect(self.on_update_unit)
            unit_definition_groupbox_layout.addRow(label,self._dimension_spinboxes[si_unit])

        hlayout.addWidget(unit_definition_groupbox)

        main_layout.addLayout(hlayout)

        buttons_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        main_layout.addWidget(buttons_box)

        self.setLayout(main_layout)

        self.setWindowTitle("Units editor")
        self.resize(800,200)

        self._init_view()

        self._new_unit_pushbutton.clicked.connect(self.on_new_unit)

        buttons_box.accepted.connect(self.on_accept_settings)
        buttons_box.rejected.connect(self.reject)
        buttons_box.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.on_save_units)

    def _init_view(self):
        """Initializes the view."""
        self._units_listview.selectionModel().clearSelection()

        self._factor_doublespinbox.setValue(1.0)

        for si_unit in UnitsManager.UNAMES:
            self._dimension_spinboxes[si_unit].setValue(0)

    def accept(self):
        """Accepts and closes the dialog."""
        self.units_updated.emit()
        super(UnitsEditorDialog,self).accept()

    def eventFilter(self, source: QtWidgets.QWidget, event: QtCore.QEvent) -> bool:
        """Event filter for the dialog.

        Args:
            source: the widget from which the event is triggered
            event: the event

        Returns:
            whether the event has been successfully filtered
        """
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Delete:
                if source == self._units_listview:
                    index = self._units_listview.currentIndex()
                    model = self._units_listview.model()
                    unit = model.data(index,QtCore.Qt.ItemDataRole.DisplayRole)
                    del self._edited_units[unit]
                    model.removeRow(self._units_listview.currentIndex().row(),QtCore.QModelIndex())
                    return True

        return super(UnitsEditorDialog,self).eventFilter(source,event)

    def on_accept_settings(self):
        """Accepts the settings."""
        UnitsManager.set_units(self._edited_units)
        self.accept()

    def on_new_unit(self):
        """Adds a new unit."""
        unit_name, ok = QtWidgets.QInputDialog.getText(self, "New unit dialog", "Name")
        if not ok:
            return

        unit_name = unit_name.strip()
        if unit_name not in self._edited_units:
            units = sorted(self._edited_units.keys())
            idx = bisect.bisect(units,unit_name)
            model = self._units_listview.model()            
            self._edited_units[unit_name] = UnitsManager.Unit(unit_name)
            model.insertRow(idx,QtGui.QStandardItem(unit_name))
            self._units_listview.setCurrentIndex(model.index(idx,0))

    def on_save_units(self):
        """Saves a unit."""
        UnitsManager.set_units(self._edited_units)
        UnitsManager.save()
        self.accept()

    def on_select_unit(self, index: QtCore.QModelIndex):
        """Selects a unit.

        Args:
            index: the index of the selected unit
        """
        model = self._units_listview.model()
        selected_unit = model.data(index, QtCore.Qt.ItemDataRole.DisplayRole)
        factor = self._edited_units[selected_unit].factor
        dimension = self._edited_units[selected_unit].dimension
        self._factor_doublespinbox.setValue(factor)
        for k, v in zip(UnitsManager.UNAMES, dimension):
            self._dimension_spinboxes[k].setValue(v)
        
    def on_update_unit(self):
        """Updates a unit."""
        model = self._units_listview.model()
        selected_unit = model.data(self._units_listview.currentIndex(), QtCore.Qt.ItemDataRole.DisplayRole)
        selected_unit = self._edited_units[selected_unit]

        selected_unit.factor = self._factor_doublespinbox.value()
        selected_unit.dimension = [self._dimension_spinboxes[u].value() for u in UnitsManager.UNAMES]

    def reject(self):
        """Cancels the dialog."""
        self._edited_units = copy.deepcopy(UnitsManager.get_units())
        self._init_view()
        super(UnitsEditorDialog,self).reject()
