import logging

from qtpy import QtCore, QtWidgets


class LoggerWidget(QtWidgets.QPlainTextEdit,logging.Handler):
    def __init__(self, parent: QtWidgets.QWidget):
        """Constructor.

        Args:
            parent: the parent widget
        """
        super(LoggerWidget,self).__init__(parent)
        self.setReadOnly(True)

    def contextMenuEvent(self, event: QtCore.QEvent):
        """Opens a contextual menu.

        Args:
            event: the event
        """
        popup_menu = self.createStandardContextMenu()

        popup_menu.addSeparator()
        popup_menu.addAction("Clear", self.on_clear_logger)
        popup_menu.addSeparator()
        popup_menu.addAction("Save as ...", self.on_save_logger)
        popup_menu.exec_(event.globalPos())

    def emit(self,record:logging.LogRecord):
        """Emits the message.

        Args:
            record: the log record
        """
        msg = self.format(record)
        self.appendPlainText(msg)

    def on_clear_logger(self):
        """Clears the logger."""
        self.clear()

    def on_save_logger(self):
        """Saves the logger contents to a file."""
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save File")
        if not filename:
            return

        with open(filename, "w") as fin:
            fin.write(self.toPlainText())