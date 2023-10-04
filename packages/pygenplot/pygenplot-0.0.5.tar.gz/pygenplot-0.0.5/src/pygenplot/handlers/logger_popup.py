import logging

from qtpy import QtWidgets


class LoggerPopup(logging.Handler):

    def emit(self, record: logging.LogRecord):
        """Emits the message.

        Args:
            record: the log record
        """
        msg = self.format(record)
        message_box = QtWidgets.QMessageBox()
        message_box.setText(msg)
        message_box.setWindowTitle("Message")
        message_box.exec()

