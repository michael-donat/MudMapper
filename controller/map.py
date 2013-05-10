__author__ = 'thornag'

from PyQt4 import QtCore
from model import map as mapModel
from model.helper import container as di

from model.map import Factory

class Bootstrap(object):
    def __init__(self):
        mapController = Map()
        di.register('controllerMap', mapController)


class Map(QtCore.QObject):

    newMapModelCreated = QtCore.pyqtSignal(mapModel.Map)

    def createMap(self):

        newMap = Factory.createNewMap()

        self.newMapModelCreated.emit(newMap)



