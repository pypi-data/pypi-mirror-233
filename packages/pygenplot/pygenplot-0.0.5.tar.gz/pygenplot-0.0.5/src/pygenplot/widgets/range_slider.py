# Code taken from https://stackoverflow.com/questions/67028200/pyqt5-qslider-two-positions

from qtpy import QtCore, QtGui, QtWidgets


class RangeSlider(QtWidgets.QSlider):
    """A slider for ranges.

    This class provides a dual-slider for ranges, where there is a defined
    maximum and minimum, as is a normal slider, but instead of having a
    single slider value, there are 2 slider values.

    This class emits the same signals as the QSlider base class, with the
    exception for valueChanged
    """

    slider_moved = QtCore.Signal(int, int)
    LOW_SLIDER = 1
    HIGH_SLIDER = 2
    BOTH_SLIDERS = 3

    def __init__(self, *args):
        super(RangeSlider, self).__init__(*args)

        self._low = self.minimum()
        self._high = self.maximum()

        self.pressed_control = QtWidgets.QStyle.SubControl.SC_None
        self.tick_interval = 0
        self.tick_position = QtWidgets.QSlider.TickPosition.NoTicks
        self.hover_control = QtWidgets.QStyle.SubControl.SC_None
        self.click_offset = 0

        self.active_slider = None
        self.action_on_release_if_no_move = None

    def _pick(self, point: QtCore.QPoint):
        """Picks the slider.

        Args:
            point: the point of click
        """
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            return point.x()
        else:
            return point.y()

    def _pixel_po_to_range_value(self, pos: int):
        """Converts the given pixel position to a logical value.

        Args:
            pos: the pixel position

        Returns: the logical value
        """
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        style = QtWidgets.QApplication.style()

        gr = style.subControlRect(style.ComplexControl.CC_Slider, opt, style.SubControl.SC_SliderGroove, self)
        sr = style.subControlRect(style.ComplexControl.CC_Slider, opt, style.SubControl.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            slider_length = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - slider_length + 1
        else:
            slider_length = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - slider_length + 1

        return style.sliderValueFromPosition(self.minimum(), self.maximum(), pos - slider_min, slider_max - slider_min, opt.upsideDown)

    def low(self) -> int:
        """Returns the low value of the slider.

        Returns:
            the low value
        """
        return self._low

    def high(self):
        """Returns the high value of the slider.

        Returns:
            the high value
        """
        return self._high

    def mouseMoveEvent(self, event: QtCore.QEvent):
        """Event handler for the mouse move event.

        Args:
            event: a mouse move event
        """
        self.action_on_release_if_no_move = None
        if self.pressed_control != QtWidgets.QStyle.SubControl.SC_SliderHandle or self.active_slider is None:
            event.ignore()
            return

        event.accept()
        new_pos = self._pixel_po_to_range_value(self._pick(event.pos()))
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)

        if self.active_slider == self.BOTH_SLIDERS:
            offset = new_pos - self.click_offset
            self._high += offset
            self._low += offset
            if self._low < self.minimum():
                diff = self.minimum() - self._low
                self._low += diff
                self._high += diff
            if self._high > self.maximum():
                diff = self.maximum() - self._high
                self._low += diff
                self._high += diff
        elif self.active_slider == self.LOW_SLIDER:
            if new_pos >= self._high:
                new_pos = self._high
            self._low = new_pos
        else:
            if new_pos <= self._low:
                new_pos = self._low
            self._high = new_pos

        self.click_offset = new_pos

        self.update()

    def mousePressEvent(self, event: QtCore.QEvent):
        """Event handler for mouse press event.

        Args:
            event: the mouse press event
        """
        event.accept()

        style = QtWidgets.QApplication.style()
        button = event.button()

        # In a normal slider control, when the user clicks on a point in the
        # slider's total range, but not on the slider part of the control
        # would jump the slider value to where the user clicked.
        # For this control, clicks which are not direct hits will slide both
        # slider parts

        if button:
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            # Check if one slider is hit
            self.active_slider = None
            for i, value in enumerate([self._low, self._high]):
                opt.sliderPosition = value
                hit = style.hitTestComplexControl(style.ComplexControl.CC_Slider, opt, event.pos(), self)
                if hit == style.SubControl.SC_SliderHandle:
                    if self._high == self._low:
                        # if a slider has been hit, but both were at the same position, consider none has been hit
                        self.active_slider = self.BOTH_SLIDERS
                    else:
                        self.active_slider = i + 1
                    self.pressed_control = hit
                    self.triggerAction(self.SliderAction.SliderMove)
                    self.setRepeatAction(self.SliderAction.SliderNoAction)
                    self.setSliderDown(True)
                    break

            if self.active_slider is None:
                # If no slider is hit, it can be a move closest slider from the clicking point, or a move of the slider
                self.active_slider = self.BOTH_SLIDERS
                self.pressed_control = QtWidgets.QStyle.SubControl.SC_SliderHandle
                self.click_offset = self._pixel_po_to_range_value(self._pick(event.pos()))
                self.triggerAction(self.SliderMove)
                self.setRepeatAction(self.SliderNoAction)
                middle = 0.5 * self._low + 0.5 * self._high
                if self.click_offset < middle:
                    self.action_on_release_if_no_move = self.LOW_SLIDER
                else:
                    self.action_on_release_if_no_move = self.HIGH_SLIDER
        else:
            event.ignore()

    def mouseReleaseEvent(self, event: QtCore.QEvent):
        """Event handler for the mouse release event.

        Args:
            event: the mouse release event
        """
        self.active_slider = None
        if self.action_on_release_if_no_move is not None:
            if self.action_on_release_if_no_move == self.LOW_SLIDER:
                self._low = self._pixel_po_to_range_value(self._pick(event.pos()))
            else:
                self._high = self._pixel_po_to_range_value(self._pick(event.pos()))
            self.action_on_release_if_no_move = None
            self.update()

        self.slider_moved.emit(self._low, self._high)

        return super().mouseReleaseEvent(event)

    def paintEvent(self, event: QtCore.QEvent):
        """Event handler for the paint event.

        Args:
            event: the paint event
        """
        # based on http://qt.gitorious.org/qt/qt/blobs/master/src/gui/widgets/qslider.cpp

        painter = QtGui.QPainter(self)
        style = QtWidgets.QApplication.style()

        # draw groove
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        opt.siderValue = 0
        opt.sliderPosition = 0
        opt.subControls = QtWidgets.QStyle.SubControl.SC_SliderGroove
        if self.tickPosition() != self.TickPosition.NoTicks:
            opt.subControls |= QtWidgets.QStyle.SubControl.SC_SliderTickmarks
        style.drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_Slider, opt, painter, self)
        groove = style.subControlRect(QtWidgets.QStyle.ComplexControl.CC_Slider, opt,
                                      QtWidgets.QStyle.SubControl.SC_SliderGroove, self)

        # drawSpan
        self.initStyleOption(opt)
        opt.subControls = QtWidgets.QStyle.SubControl.SC_SliderGroove
        if self.tickPosition() != self.TickPosition.NoTicks:
            opt.subControls |= QtWidgets.QStyle.SubControl.SC_SliderTickmarks
        opt.siderValue = 0
        opt.sliderPosition = self._low
        low_rect = style.subControlRect(QtWidgets.QStyle.ComplexControl.CC_Slider, opt,
                                        QtWidgets.QStyle.SubControl.SC_SliderHandle, self)
        opt.sliderPosition = self._high
        high_rect = style.subControlRect(QtWidgets.QStyle.ComplexControl.CC_Slider, opt,
                                         QtWidgets.QStyle.SubControl.SC_SliderHandle, self)

        low_pos = self._pick(low_rect.center())
        high_pos = self._pick(high_rect.center())

        min_pos = min(low_pos, high_pos)
        max_pos = max(low_pos, high_pos)

        c = QtCore.QRect(low_rect.center(), high_rect.center()).center()
        if opt.orientation == QtCore.Qt.Orientation.Horizontal:
            span_rect = QtCore.QRect(QtCore.QPoint(min_pos, c.y() - 2),
                                     QtCore.QPoint(max_pos, c.y() + 1))
        else:
            span_rect = QtCore.QRect(QtCore.QPoint(c.x() - 2, min_pos),
                                     QtCore.QPoint(c.x() + 1, max_pos))

        if opt.orientation == QtCore.Qt.Orientation.Horizontal:
            groove.adjust(0, 0, -1, 0)
        else:
            groove.adjust(0, 0, 0, -1)

        if self.isEnabled():
            highlight = self.palette().color(QtGui.QPalette.ColorRole.Highlight)
            painter.setBrush(QtGui.QBrush(highlight))
            painter.setPen(QtGui.QPen(highlight, 0))
            painter.drawRect(span_rect.intersected(groove))

        for i, value in enumerate([self._low, self._high]):
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            # Only draw the groove for the first slider so it doesn't get drawn
            # on top of the existing ones every time
            if i == 0:
                opt.subControls = QtWidgets.QStyle.SubControl.SC_SliderHandle  # | QtWidgets.QStyle.SC_SliderGroove
            else:
                opt.subControls = QtWidgets.QStyle.SubControl.SC_SliderHandle

            if self.tickPosition() != self.TickPosition.NoTicks:
                opt.subControls |= QtWidgets.QStyle.SubControl.SC_SliderTickmarks

            if self.pressed_control:
                opt.activeSubControls = self.pressed_control
            else:
                opt.activeSubControls = self.hover_control

            opt.sliderPosition = value
            opt.sliderValue = value
            style.drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_Slider, opt, painter, self)

    def set_high(self, high):
        """Sets the high value of the slider.

        Args:
            high: the high value
        """
        self._high = high
        self.update()

    def set_low(self, low: int):
        """Sets the low value of the slider.

        Args:
            low: the low value
        """
        self._low = low
        self.update()
