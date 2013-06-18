__author__ = 'thornag'

from PyQt4 import QtCore
from model import map as mapModel
from model import room as roomModel

from model.map import Factory

class Map(QtCore.QObject):

    mapModelCreated = QtCore.pyqtSignal(mapModel.Map)
    mapModelDestroyed = QtCore.pyqtSignal(mapModel.Map)

    mapRoomCreated = QtCore.pyqtSignal(roomModel.Room)

    mapLevelSelected = QtCore.pyqtSignal(mapModel.Level)

    __map=None
    __geometryHelper=None
    __factory = None

    def setGeometryHelper(self, helper):
        self.__geometryHelper = helper

    def setFactory(self, factory):
        self.__factory = factory

    def __init__(self):
        super(Map, self).__init__()

    def mapModel(self):
        return self.__map

    def createMap(self):

        self.destroyMap()

        newMap = self.__factory.createNewMap()

        self.mapModelCreated.emit(newMap)

        initialLevel = next(newMap.levels().itervalues())

        self.selectLevel(initialLevel)

        self.__map = newMap

    def selectLevel(self, level):
        self.mapLevelSelected.emit(level)


    def destroyMap(self):

        if self.mapModel() is None:
            return

        self.mapModelDestroyed.emit(self.mapModel())

        self.__map=None

    def createRoomAt(self, position):

        position = self.__geometryHelper.snapToGrid(position)

        newRoom = self.__factory.createNewRoom()
        newRoom.geometry().updateFromPoint(position)

        self.__map.addRoom(newRoom)

        #self.mapModel().

        self.mapRoomCreated.emit(newRoom)

        return newRoom








