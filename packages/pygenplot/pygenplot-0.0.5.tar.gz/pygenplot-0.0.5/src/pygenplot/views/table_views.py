from qtpy import QtCore, QtWidgets


class QTableViewWithoutRightClick(QtWidgets.QTableView):

    def mousePressEvent(self, event: QtCore.QEvent):
        """Event handler for a mouse press event.

        Args:
            event: the mouse press event
        """
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            return
        return super(QTableViewWithoutRightClick,self).mousePressEvent(event)
