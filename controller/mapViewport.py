__author__ = 'thornag'

from PyQt4 import QtCore, QtGui
from model import map as mapModel
from model.helper import container as di
from model.tools import enum
from view.map import Room as roomView
from model.helper import container as di, ComponentRequest
from uuid import UUID as typeUUID

class Map(QtCore.QObject):

    __uiMapViewport=None
    __uiScenes=None
    __clickMode=None

    roomCreateRequest=QtCore.pyqtSignal(QtCore.QPointF)

    __geometryHelper=ComponentRequest('geometryHelper')

    CLICK_MODE=enum('ROOM', 'LABEL', 'BACKGROUND')

    currentlySelectedRoom=None

    def __init__(self):
        super(Map, self).__init__()
        self.__uiScenes={}

    def clickMode(self, mode):
        self.__uiMapViewport.setCursor(QtCore.Qt.CrossCursor)
        self.__clickMode=mode

    def resetClickMode(self):
        self.__uiMapViewport.setCursor(QtCore.Qt.ArrowCursor)
        self.__clickMode=None

    def setView(self, uiMapViewport):
        self.__uiMapViewport=uiMapViewport
        uiMapViewport.setController(self)

    def createMap(self, mapModel):
        o = mapModel.levels()
        for level in mapModel.levels().itervalues():
            self.__uiScenes[level.id()] = QtGui.QGraphicsScene()

    def selectLevel(self, level):
        scene = self.__uiScenes[level.id()]
        self.__uiMapViewport.setScene(scene)

    def createRoom(self, room):
        newRoom = roomView(room.id())
        newRoom.setPos(room.geometry().getPoint())
        self.__uiMapViewport.scene().addItem(newRoom)

    def scenes(self):
        return self.__uiScenes

    def destroyMap(self, mapModel):
        self.__uiScenes={}

    def processMouseRelease(self, QMouseEvent):

        if self.__clickMode is None: return False

        QMouseEvent.accept()

        eventPosition = QMouseEvent.pos()
        eventPosition = self.__uiMapViewport.mapToScene(eventPosition)
        eventPosition = self.__geometryHelper.snapToGrid(eventPosition)

        if self.__clickMode == self.CLICK_MODE.ROOM:
            self.roomCreateRequest.emit(eventPosition)

    def markCurrentlyVisitedRoom(self, roomView):
        if self.currentlySelectedRoom:
            self.currentlySelectedRoom.setIsCurrentlyVisited(False)

        self.currentlySelectedRoom = roomView

        self.currentlySelectedRoom.setIsCurrentlyVisited(True)










