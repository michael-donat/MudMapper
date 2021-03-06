from PyQt4 import QtCore
from uuid import uuid1


class Map(object):

    __id=None
    __rooms=None
    __zones=None
    __levels=None

    def __init__(self, **kwargs):
        self.__id = kwargs['id'] if kwargs.has_key('id') else uuid1()
        self.__zones={}
        self.__rooms={}
        self.__levels={}

    def id(self):
        return self.__id

    def zones(self):
        return self.__zones

    def levels(self):
        return self.__levels

    def rooms(self):
        return self.__rooms

    def addZone(self, mapZone):
        if not isinstance(mapZone, Zone):
            raise TypeError('mapZone is not an instance of Zone, %s given instead' % type(mapZone))

        self.__zones[mapZone.id()] = mapZone

    def addLevel(self, mapLevel):
        if not isinstance(mapLevel, Level):
            raise TypeError('mapLevel is not an instance of Level, %s given instead' % type(mapLevel))

        self.__levels[mapLevel.id()] = mapLevel


class Zone(object):
    __id=None
    __name=None

    def __init__(self, **kwargs):
        self.__id = kwargs['id'] if kwargs.has_key('id') else uuid1()
        self.__name = kwargs['name'] if kwargs.has_key('name') else 'Unnamed'

    def id(self):
        return self.__id

    def name(self):
        return self.__name



class Level(object):
    __id=None
    __index=None
    __zone=None

    def __init__(self, **kwargs):
        self.__id = kwargs['id'] if kwargs.has_key('id') else uuid1()
        self.__name = kwargs['index'] if kwargs.has_key('index') else 0

    def id(self):
        return self.__id

    def index(self):
        return self.__index

    def assignToZone(self, mapZone):
        if not isinstance(mapZone, Zone):
            raise TypeError('mapZone is not an instance of Zone, %s given instead' % type(mapZone))

        self.__zone = mapZone

    def zone(self):
        return self.__zone



class Factory(object):

    @staticmethod
    def createNewMap():
        newMap = Map()
        mapZone = Zone()
        newMap.addZone(mapZone)
        mapLevel = Level()
        mapLevel.assignToZone(mapZone)
        newMap.addLevel(mapLevel)
        return newMap