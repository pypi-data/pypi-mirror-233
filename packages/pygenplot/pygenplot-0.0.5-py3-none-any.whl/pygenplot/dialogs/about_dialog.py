import platform

import h5py

from qtpy import QtCore, QtWidgets

from ..__pkginfo__ import __version__


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(AboutDialog,self).__init__(parent)

        self._build()

        self.setWindowTitle("About pygenplot")

    def _build(self):
        """Builds the dialog"""
        main_layout = QtWidgets.QVBoxLayout()

        message = """
        <dl>
            <dt><b>pygenplot version</b></dt><dd>{pygenplot_version}</dd>
            <dt><b>HDF5 version</b></dt><dd>{hdf5_version}</dd>
            <dt><b>h5py version</b></dt><dd>{h5py_version}</dd>
            <dt><b>Qt version</b></dt><dd>{qt_version}</dd>
            <dt><b>PyQt version</b></dt><dd>{pyqt_version}</dd>
            <dt><b>Python version</b></dt><dd>{python_version}</dd>
            <dt><b>System</b></dt><dd>{system}</dd>
            <dt><b>Distribution</b></dt><dd>{distribution}</dd>
            <dt><b>Processor</b></dt><dd>{processor}</dd>
        </dl>
        <hr>
        <p>
        Copyright (C) <a href="{ill_url}">Institut Laue Langevin</a>
        </p>
        <hr>
        Bug report/feature request: pellegrini[at]ill.fr, perenon[at]ill.fr
        """

        uname = platform.uname()

        info = {
            "pygenplot_version" : __version__,
            "h5py_version" : h5py.version.version,
            "hdf5_version" : h5py.version.hdf5_version,
            "qt_version" : QtCore.qVersion(),
            "pyqt_version" : QtCore.PYQT_VERSION_STR,
            "python_version" : platform.python_version(),
            "ill_url" : "http://www.ill.eu",
            "system" : uname.system,
            "processor" : uname.processor,
            "distribution" : uname.version,
        }

        label = QtWidgets.QLabel()
        label.setOpenExternalLinks(True)
        label.setText(message.format(**info))

        main_layout.addWidget(label)

        self.setLayout(main_layout)
