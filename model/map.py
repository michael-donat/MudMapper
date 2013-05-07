from PyQt4 import QtCore
from uuid import uuid1

class Level(object):
    __id=None

    def __init__(self):
        self.__id=str(uuid1())

    def id(self):
        return self.__id

class Map(object):

    __levels=None

    def __init__(self):
        self.__levels={}

    def levels(self):
        return self.__levels

    def addLevel(self, level, index=0):
        index = str(index)
        if hasattr(self.__levels, index):
            raise ValueError('Level %s already exists' % index)
        self.__levels[index] = level
        return level

    def destroy(self):
        pass

class MapRegistry(QtCore.QObject):

    mapCreated = QtCore.pyqtSignal(Map)
    levelCreated = QtCore.pyqtSignal(Level)
    levelSwitched = QtCore.pyqtSignal(Level)
    mapDestroyed = QtCore.pyqtSignal()

    __currentLevel=None

    __map=None

    def createMap(self):
        if isinstance(self.map(), Map):
            self.map().destroy()
            self.mapDestroyed.emit()
        self.__map = Map()
        self.mapCreated.emit(self.__map)
        level = Level()
        self.__map.addLevel(level)
        self.levelCreated.emit(level)
        self.setLevel(level)

    def setLevel(self, level):
        self.__currentLevel = level
        self.levelSwitched.emit(level)

    def map(self):
        return self.__map


