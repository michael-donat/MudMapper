__author__ = 'thornag'

from PyQt4 import QtCore, QtGui
from model import map as mapModel
from model.helper import container as di

class Bootstrap(object):
    def __init__(self,  mainWindow):
        mapController = Map(mainWindow.mapViewport)
        di.register('controllerMapViewport', mapController)

class Map(QtCore.QObject):

    __uiMapViewport=None
    __uiScenes=None

    def __init__(self, mapViewport):
        """
        :param mapViewport: QtGui.QGraphicsView
        """
        self.__uiMapViewport=mapViewport
        self.__uiScenes={}

    def createMap(self, mapModel):
        scene = QtGui.QGraphicsScene()
        self.__uiMapViewport.setScene(scene)
        scene.addText(str(mapModel.id()))


