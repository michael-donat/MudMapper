from PyQt4 import QtCore
from uuid import uuid1
from model.helper import ComponentRequest
from model.helper import generateId
from model.room import Room

from model.errors import *

class Map(object):

    __id=None
    __rooms=None
    __zones=None
    __levels=None

    def __init__(self, **kwargs):
        self.__id = kwargs['id'] if kwargs.has_key('id') else generateId()
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

    def addRoom(self, mapRoom):
        if not isinstance(mapRoom, Room):
            raise TypeError('mapRoom is not an instance of Room, %s given instead' % type(mapRoom))

        self.__rooms[mapRoom.id()] = mapRoom


    def roomById(self, id):
        if not self.__rooms.has_key(id):
            raise UnknownRoomError('could not find registered room by id: %s' % id)

        return self.__rooms[id]




class Zone(object):
    __id=None
    __name=None

    def __init__(self, **kwargs):
        self.__id = kwargs['id'] if kwargs.has_key('id') else generateId()
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
        self.__id = kwargs['id'] if kwargs.has_key('id') else generateId()
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

config = ComponentRequest('Config').instance.drawing()

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

    @staticmethod
    def createNewRoom():
        newRoom = Room()
        newRoom.geometry().update(0,0,config.getBoxSize(),config.getBoxSize())
        return newRoom