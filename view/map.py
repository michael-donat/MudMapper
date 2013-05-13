__author__ = 'donatm'

from PyQt4 import QtGui, QtCore
from model.helper import ComponentRequest
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

    def keyPressEvent(self, QKeyEvent):

        if QKeyEvent.matches(QtGui.QKeySequence.ZoomIn):
            self.scale(1.2, 1.2)

        if QKeyEvent.matches(QtGui.QKeySequence.ZoomOut):
            self.scale(0.8, 0.8)


config = ComponentRequest('Config').instance.drawing()
coordinatesHelper = ComponentRequest('geometryHelper')

class RoomComponents(object):

    __boundingRect = None
    __roomRect = None
    __exits = None
    __arrowHeads={}

    __currentlyVisitedBrush=None

    def __calculateArrowHead(self, line):

        d = config.getExitSize()/1.25
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


    def __init__(self):
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

        self.__currentlyVisitedBrush = QtGui.QColor(123,051,123)


    def boundingRect(self): return self.__boundingRect
    def roomRect(self): return self.__roomRect
    def exits(self): return self.__exits
    def arrowHeads(self): return self.__arrowHeads

    def currentlyVisitedBrush(self):
        return self.__currentlyVisitedBrush


roomComponents = RoomComponents()

class Room(QtGui.QGraphicsItem):

    __modelId=None
    __currentlyVisited=None

    def __init__(self, modelId):
        super(Room, self).__init__()
        self.__modelId = modelId
        self.setFlags(QtGui.QGraphicsItem.ItemSendsGeometryChanges | QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)

    def modelId(self):
        return self.__modelId

    def boundingRect(self):
        return roomComponents.boundingRect()

    def setIsCurrentlyVisited(self, isVisited=False):
        self.__currentlyVisited = bool(isVisited)

    def paint(self, painter, option, widget):

        defaultBrush = painter.brush()

        if self.__currentlyVisited:
            painter.setBrush(roomComponents.currentlyVisitedBrush())
            painter.drawEllipse(self.boundingRect())

        painter.setBrush(defaultBrush)

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
            return coordinatesHelper.instance.snapToGrid(QVariant.toPoint() )

        if QGraphicsItem_GraphicsItemChange == QtGui.QGraphicsItem.ItemPositionHasChanged:
            changeEmitter.roomPositionChanged.emit(self) #can't emit signal as QGraphicsItem does not inherit form QObject


        return super(Room, self).itemChange(QGraphicsItem_GraphicsItemChange, QVariant)

    def mouseDoubleClickEvent(self, QGraphicsSceneMouseEvent):
        changeEmitter.roomDoubleClicked.emit(self)

class ChangeEmitter(QtCore.QObject):
    def __init__(self):
        super(ChangeEmitter, self).__init__()

    roomPositionChanged = QtCore.pyqtSignal(Room)
    roomDoubleClicked = QtCore.pyqtSignal(Room)

changeEmitter = ChangeEmitter()