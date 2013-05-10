__author__ = 'thornag'

from PyQt4 import QtCore, QtGui
from model import map as mapModel
from model.helper import container as di
from model.tools import enum

class Map(QtCore.QObject):

    __uiMapViewport=None
    __uiScenes=None
    __clickMode=None

    roomCreateRequest=QtCore.pyqtSignal(QtCore.QPoint)

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
        self.__uiScenes[mapModel.id()] = {}
        o = mapModel.levels()
        for level in mapModel.levels().itervalues():
            self.__uiScenes[mapModel.id()][level.id()] = QtGui.QGraphicsScene()

    def scenes(self):
        return self.__uiScenes

    def destroyMap(self, mapModel):

        if not self.__uiScenes.has_key(mapModel.id()):
            return

        del self.__uiScenes[mapModel.id()]

    def processMouseRelease(self, QMouseEvent):

        if self.__clickMode is None: return

        QMouseEvent.accept()

        eventPosition = QMouseEvent.pos()

        if self.__clickMode == self.CLICK_MODE.ROOM:
            self.roomCreateRequest.emit(eventPosition)








