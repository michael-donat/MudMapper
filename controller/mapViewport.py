__author__ = 'thornag'

from PyQt4 import QtCore, QtGui
from model import map as mapModel

class Bootstrap(object):
    def __init__(self, controllerRegistry, mapRegistry, mainWindow):
        mapController = Map(mainWindow.mapViewport)
        mapRegistry.levelCreated.connect(mapController.levelCreated)
        mapRegistry.levelSwitched.connect(mapController.levelSwitched)
        controllerRegistry += [mapController]

class Map(QtCore.QObject):

    __uiMapViewport=None
    __uiScenes=None

    def __init__(self, mapViewport):
        """
        :param mapViewport: QtGui.QGraphicsView
        """
        self.__uiMapViewport=mapViewport
        self.__uiScenes={}

    @QtCore.pyqtSlot(mapModel.Map, name='mapCreated')
    def mapCreated(self, map):
        pass

    @QtCore.pyqtSlot(mapModel.Level, name='levelCreated')
    def levelCreated(self, level):
        scene = QtGui.QGraphicsScene()
        self.__uiScenes[level.id()] = scene

    @QtCore.pyqtSlot(mapModel.Level, name='levelSwitched')
    def levelSwitched(self, level):
        if not level.id() in self.__uiScenes:
            raise ValueError('Unknown level')

        self.__uiMapViewport.setScene(self.__uiScenes[level.id()])


