__author__ = 'donatm'

from PyQt4 import QtGui


class Viewport(QtGui.QGraphicsView):

    __controller=None

    def __init__(self):
        super(Viewport, self).__init__()
        #self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    def setController(self, controller):
        self.__controller = controller

    def mouseReleaseEvent(self, QMouseEvent):
        """
        :param QMouseEvent: QtGui.QMouseEvent
        """
        self.__controller.processMouseRelease(QMouseEvent)