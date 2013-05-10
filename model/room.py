__author__ = 'donatm'

from PyQt4 import QtCore
from model.tools import enum
from uuid import uuid1
from model.errors import *
import types

Directions = enum('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'U', 'D')

class Room(object):
    __id=None
    __properties=None
    __geometry=None
    __exits=None
    __level=None

    def __init__(self):
        self.__id=uuid1()
        self.__properties = Properties()
        self.__geometry = Geometry()
        self.__exits = Exits()

    def id(self):
        return self.__id

    def properties(self):
        return self.__properties

    def geometry(self):
        return self.__geometry

    def addExit(self, exit_):
        """
        :param exit_: Exit
        """
        exit_.setRoom(self)
        self.exits().addExit(exit_)

    def exits(self):
        """
        :rtype: Exits
        """
        return self.__exits

    def setLevel(self, level):
        self.__level=level


class Properties(object):
    __name=None
    __label=None
    __description=None
    __textReturn=None
    __terrainClass=None
    __color=None
    __disabled=False

    def name(self): return self.__name
    def label(self): return self.__label
    def description(self): return self.__description
    def textReturn(self): return self.__textReturn
    def terrainClass(self): return self.__terrainClass
    def color(self): return self.__color
    def disabled(self): return self.__disabled

    def setName(self, name):
        self.__name = name

    def setLabel(self, label):
        self.__label = label

    def setDescription(self, description):
        self.__description = description

    def setTextReturn(self, textReturn):
        self.__textReturn = textReturn

    def setTerrainClass(self, terrainClass):
        self.__terrainClass = terrainClass

    def setColor(self, color):
        self.__color = color

    def setDisabled(self, disabled):
        self.__disabled = bool(disabled)


class Exits(object):
    __exits=None
    __byDirectionHash=None
    __byLabelHash=None

    def __init__(self):
        self.__exits={}
        self.__byDirectionHash={}
        self.__byLabelHash={}

    def addExit(self, exit_):
        if not isinstance(exit_, Exit):
            raise RuntimeError('Instance of %s required instance of %s given' % (Exit, exit_))

        self.__exits[exit_.id()] = exit_
        if exit_.direction() is not None:
            self.__byDirectionHash[exit_.direction()] = exit_.id()

        if exit_.label() is not None:
            self.__byLabelHash[exit_.label()] = exit_.id()

    def hasExit(self, exitId):
        return self.__exits.has_key(exitId)

    def getExit(self, exitId):
        if not self.hasExit(exitId):
            raise RuntimeError('There is no exit with given id, possibly a hash sync error')

        return self.__exits[exitId]

    def hasExitInDirection(self, direction):
        return self.__byDirectionHash.has_key(direction)

    def getExitByDirection(self, direction):
        if not self.hasExitInDirection(direction):
            raise NoExitError('Requested non existing exit by direction')

        return self.getExit(self.__byDirectionHash[direction])

    def hasExitByLabel(self, label):
        return self.__byLabelHash.has_key(label)

    def getExitByLabel(self, label):
        if not self.hasExitByLabel(label):
            raise NoExitError('Requested non existing exit by label')

        return self.getExit(self.__byLabelHash[label])



class Exit(object):
    __id=None
    __direction=None
    __label=None
    __masks=None
    __destination=None
    __blocked=False
    __oneWay=False
    __room=None

    def __init__(self, **kwargs):
        self.__masks=[]
        self.__id=uuid1()
        if kwargs.has_key('direction'):
            self.__direction = kwargs['direction']
        if kwargs.has_key('label'):
            self.__label = kwargs['label']
        if kwargs.has_key('oneWay'):
            self.__oneWay = bool(kwargs['oneWay'])
        if kwargs.has_key('blocked'):
            self.__blocked = bool(kwargs['blocked'])
        if kwargs.has_key('masks'):
            if not isinstance(kwargs['masks'], types.ListType): raise ValueError('Mask needs to be of type list, %s given' % type(kwargs['masks']))
            self.__masks = kwargs['masks']
        if kwargs.has_key('room'):
            self.setRoom(kwargs['room'])

    def id(self):
        return self.__id

    def setRoom(self, room):
        if not isinstance(room, Room): raise ValueError('Mask needs to be of type model.Room, %s given' % type(room))
        self.__room = room

    def room(self):
        return self.__room

    def direction(self):
        return self.__direction

    def label(self):
        return self.__label

    def oneWay(self):
        return self.__oneWay

    def blocked(self):
        return self.__blocked

    def masks(self):
        return self.__masks


class Geometry(object):
    __x1=0
    __y1=0
    __x2=0
    __y2=0

    def update(self, x1, y1, x2, y2):
        self.__x1 = float(x1)
        self.__y1 = float(y1)
        self.__x2 = float(x2)
        self.__y2 = float(y2)
        return self

    #slot
    def updateFromView(self, QGraphicsItem):
        x1 = QGraphicsItem.x()
        y1 = QGraphicsItem.y()
        x2 = x1 + QGraphicsItem.rect().width()
        y2 = y1 + QGraphicsItem.rect().height()

        return self.update(x1, y1, x2, y2)

    def updateFromPoint(self, QPointF):
        fx =  self.__x2 - self.__x1
        fy = self.__y2 - self.__y1
        if fx == 0 or fy == 0:
            raise RuntimeError('Could not work out x2 or y2')
        x2 = fx + QPointF.x()
        y2 = fy + QPointF.y()
        return self.update(QPointF.x(), QPointF.y(), x2, y2)

    def updateFromRect(self, QRectF):
        return self.update(QRectF.x(), QRectF.y(), QRectF.right(), QRectF.bottom())

    def getPoint(self):
        return QtCore.QPointF(self.__x1, self.__y1)

    def getRect(self):
        return QtCore.QRectF(QtCore.QPointF(self.__x1, self.__y1), QtCore.QPointF(self.__x2, self.__y2))



