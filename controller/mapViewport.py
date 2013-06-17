__author__ = 'thornag'

from PyQt4 import QtCore, QtGui
from model import map as mapModel
from model.helper import container as di
from model.tools import enum
from view.map import Room as roomView
from view.map import Level as levelView

class Map(QtCore.QObject):

    __uiMapViewport=None
    __uiScenes=None
    __clickMode=None

    __mapModel=None

    roomCreateRequest=QtCore.pyqtSignal(QtCore.QPointF)

    CLICK_MODE=enum('ROOM', 'LABEL', 'BACKGROUND')

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
        self.__mapModel=mapModel
        o = mapModel.levels()
        for level in mapModel.levels().itervalues():
            self.__uiScenes[level.id()] = levelView(self)

    def selectLevel(self, level):
        scene = self.__uiScenes[level.id()]
        self.__uiMapViewport.setScene(scene)

    def createRoom(self, room):
        newRoom = roomView()
        newRoom.configure(room)
        self.__uiMapViewport.scene().addItem(newRoom)

    def scenes(self):
        return self.__uiScenes

    def map(self):
        """
        :return: mapModel
        """
        return self.__mapModel

    def destroyMap(self, mapModel):
        self.__uiScenes={}

    def processMouseRelease(self, QMouseEvent):

        if self.__clickMode is None: return False

        QMouseEvent.accept()

        eventPosition = QMouseEvent.pos()
        eventPosition = self.__uiMapViewport.mapToScene(eventPosition)

        if self.__clickMode == self.CLICK_MODE.ROOM:
            self.roomCreateRequest.emit(eventPosition)

    def itemPositionChanged(self, modelId, position, roomView):
        self.map().roomById(modelId).geometry().updateFromView(roomView)
        room = self.map().roomById(modelId)
        pass
