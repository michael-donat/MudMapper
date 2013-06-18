__author__ = 'donatm'

from PyQt4 import QtGui, QtCore
from model.room import Directions
import math

class Viewport(QtGui.QGraphicsView):

    __controller=None

    def __init__(self):
        super(Viewport, self).__init__()
        #self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing | QtGui.QPainter.SmoothPixmapTransform | QtGui.QPainter.HighQualityAntialiasing)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setViewportUpdateMode(QtGui.QGraphicsView.SmartViewportUpdate)


    def setController(self, controller):
        self.__controller = controller

    def mouseReleaseEvent(self, QMouseEvent):
        """
        :param QMouseEvent: QtGui.QMouseEvent
        """

        if not self.__controller.processMouseRelease(QMouseEvent):
            return super(Viewport, self).mouseReleaseEvent(QMouseEvent)

class Level(QtGui.QGraphicsScene):

    __controller=None

    def __init__(self, controller):
        super(Level, self).__init__()
        self.setController(controller)

    def setController(self, controller):
        self.__controller = controller

    def controller(self):
        return self.__controller

class RoomComponents(object):

    __boundingRect = None
    __roomRect = None
    __exits = None
    __arrowHeads={}
    __config=None

    def __calculateArrowHead(self, line):

        d = self.__config.getExitSize()/1.25
        theta = math.pi / 7

        lineAngle = math.atan2(line.dy(), line.dx())
        h = math.fabs(d/math.cos(theta))

        angle1 = lineAngle + theta
        angle2 = lineAngle - theta

        angle1 = math.pi + lineAngle + theta
        angle2 = math.pi + lineAngle - theta

        P1 = QtCore.QPoint(line.x2()+math.cos(angle1)*h,line.y2()+math.sin(angle1)*h)
        P2 = QtCore.QPoint(line.x2()+math.cos(angle2)*h,line.y2()+math.sin(angle2)*h)

        return QtGui.QPolygon([line.p2(), P1, P2])


    def __init__(self, config):
        self.__config = config
        self.__boundingRect = config.getBoundingRect()
        self.__roomRect = QtCore.QRect(config.getExitSize(), config.getExitSize(), config.getRoomSize(), config.getRoomSize())
        self.__exits = {
            Directions.N: QtCore.QLine(config.getMidPoint(),0,config.getMidPoint(), 0+config.getExitSize()),
            Directions.NE: QtCore.QLine(config.getBoxSize()-0, 0, config.getBoxSize()-0-config.getExitSize(), 0+config.getExitSize()),
            Directions.E: QtCore.QLine(config.getBoxSize()-0,config.getMidPoint(), config.getBoxSize()-0-config.getExitSize(), config.getMidPoint()),
            Directions.SE: QtCore.QLine(config.getBoxSize()-0,config.getBoxSize()-0, config.getBoxSize()-0-config.getExitSize(), config.getBoxSize()-0-config.getExitSize(),),
            Directions.S: QtCore.QLine(config.getMidPoint(),config.getBoxSize()-0,config.getMidPoint(), config.getBoxSize()-0-config.getExitSize()),
            Directions.SW: QtCore.QLine(0, config.getBoxSize()-0, 0+config.getExitSize(), config.getBoxSize()-0-config.getExitSize()),
            Directions.W: QtCore.QLine(0, config.getMidPoint(), 0+config.getExitSize(), config.getMidPoint()),
            Directions.NW: QtCore.QLine(0, 0, 0+config.getExitSize(), 0+config.getExitSize())
        }
        self.__arrowHeads = {}
        for direction in self.__exits:
            self.__arrowHeads[direction] = self.__calculateArrowHead(self.__exits[direction])

    def boundingRect(self): return self.__boundingRect
    def roomRect(self): return self.__roomRect
    def exits(self): return self.__exits
    def arrowHeads(self): return self.__arrowHeads

class Room(QtGui.QGraphicsItem):

    DATA_ID = 0

    __geometryHelper=None
    __roomComponents = None

    def setGeometryHelper(self, helper):
        self.__geometryHelper = helper

    def setRoomComponents(self, components):
        self.__roomComponents = components

    def __init__(self):
        super(Room, self).__init__()
        self.setFlags(QtGui.QGraphicsItem.ItemSendsGeometryChanges | QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)

    def boundingRect(self):
        return self.__roomComponents.boundingRect()

    def configure(self, roomModel):
        self.setData(self.DATA_ID, QtCore.QVariant(roomModel.id()))
        self.setPos(roomModel.geometry().getPoint())

    def modelId(self):
        return str(self.data(self.DATA_ID).toString())

    def paint(self, painter, option, widget):

        roomComponents = self.__roomComponents

        painter.drawRect(roomComponents.roomRect())
        painter.drawLine(roomComponents.exits()[Directions.N])
        painter.drawLine(roomComponents.exits()[Directions.NE])
        painter.drawLine(roomComponents.exits()[Directions.E])
        painter.drawLine(roomComponents.exits()[Directions.SE])
        painter.drawLine(roomComponents.exits()[Directions.S])
        painter.drawLine(roomComponents.exits()[Directions.SW])
        painter.drawLine(roomComponents.exits()[Directions.W])
        painter.drawLine(roomComponents.exits()[Directions.NW])
        painter.setBrush(QtGui.QColor(0,0,0))
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.N])
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.NE])
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.E])
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.SE])
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.S])
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.SW])
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.W])
        painter.drawPolygon(roomComponents.arrowHeads()[Directions.NW])

    def itemChange(self, QGraphicsItem_GraphicsItemChange, QVariant):
        if QGraphicsItem_GraphicsItemChange == QtGui.QGraphicsItem.ItemPositionChange:
            point = QVariant.toPoint()

            QPointPosition = self.__geometryHelper.snapToGrid(QVariant.toPoint())

            self.notifyPositionChanged()

            return QPointPosition

        return super(Room, self).itemChange(QGraphicsItem_GraphicsItemChange, QVariant)

    def notifyPositionChanged(self):
        if not self.scene(): return

        self.scene().controller().itemPositionChanged(self.modelId(), self.pos(), self)
