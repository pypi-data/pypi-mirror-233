from qtpy import sip

from qtpy import QtWidgets


def delete_layout(layout: QtWidgets.QLayout):
    """Deletes a layout. This will delete all the inner layouts and widgets.

    Args:
        layout: the layout to delete
    """
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                delete_layout(item.layout())
        sip.delete(layout)
