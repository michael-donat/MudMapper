__author__ = 'thornag'

from PyQt4 import QtCore
from model import map as mapModel
from model import room as roomModel
from model.helper import container as di

from model.map import Factory

class Map(QtCore.QObject):

    mapModelCreated = QtCore.pyqtSignal(mapModel.Map)
    mapModelDestroyed = QtCore.pyqtSignal(mapModel.Map)

    mapRoomCreated = QtCore.pyqtSignal(roomModel.Room)

    mapLevelSelected = QtCore.pyqtSignal(mapModel.Level)

    __map=None

    def __init__(self):
        super(Map, self).__init__()

    def mapModel(self):
        return self.__map

    def createMap(self):

        self.destroyMap()

        newMap = Factory.createNewMap()

        self.mapModelCreated.emit(newMap)

        initialLevel = next(newMap.levels().itervalues())

        self.mapLevelSelected.emit(initialLevel)

        self.__map = newMap

    def destroyMap(self):

        if self.mapModel() is None:
            return

        self.mapModelDestroyed.emit(self.mapModel())

        self.__map=None

    def createRoomAt(self, position):

        newRoom = roomModel.Room()
        newRoom.geometry().updateFromPoint(position)

        #self.mapModel().

        self.mapRoomCreated.emit(newRoom)








