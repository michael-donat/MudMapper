import PyQt4

__author__ = 'thornag'

from PyQt4 import QtCore, QtGui
from model import map as mapModel
from model.tools import enum
from view.map import Room as roomView
from view.map import Level as levelView

class Map(QtCore.QObject):

    __uiMapViewport=None
    __uiScenes=None
    __clickMode=None
    __mapModel=None
    __mapRoomViewRoutine=None

    roomCreateRequest=QtCore.pyqtSignal(QtCore.QPointF)

    CLICK_MODE=enum('ROOM', 'LABEL', 'BACKGROUND')

    def __init__(self):
        super(Map, self).__init__()
        self.__uiScenes={}

    def setRoomViewRoutine(self, routine):
        self.__mapRoomViewRoutine = routine

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
        newRoom = self.__mapRoomViewRoutine()
        newRoom.configure(room)
        self.__uiMapViewport.scene().addItem(newRoom)

    @QtCore.pyqtSlot(str)
    def removeRoom(self, roomView):
        roomView.scene().removeItem(roomView)

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


class RoomContextMenu(QtCore.QObject):

    roomRemoveRequest = QtCore.pyqtSignal([str], [object])

    def __init__(self):
        super(RoomContextMenu, self).__init__()

    def delete(self, roomView):
        self.roomRemoveRequest[str].emit(roomView.modelId())
        self.roomRemoveRequest[object].emit(roomView)

    def properties(self, roomView):
        print 'properties request'

    def markActive(self, roomView):
        print 'mark request'

class Room(QtCore.QObject):

    __contextMenu=None

    def __init__(self):
        super(Room, self).__init__()
        self.__contextMenu = RoomContextMenu()

    def contextMenu(self):
        return self.__contextMenu
