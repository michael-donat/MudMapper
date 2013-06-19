
from controller import \
    mainWindow as mainWindowController, \
    mapViewport as mapViewportController, \
    map as mapController, \
    propertiesWindow as propertiesController \

import model.map as mapModel
import model.helper as helperModel
import view.map as viewMap


class Container:
    __config = None;
    __objects=None
    def __init__(self, config):
        self.__config = config
        self.__objects={}


    def getMainWindowFileMenuController(self):
        if not self.__objects.has_key('controller.mainwindow.filemenu'):
            self.__objects['controller.mainwindow.filemenu'] = mainWindowController.FileMenu()

        return self.__objects['controller.mainwindow.filemenu']

    def getMainWindowToolbarController(self):
        if not self.__objects.has_key('controller.mainwindow.toolbar'):
            self.__objects['controller.mainwindow.toolbar'] = toolbar = mainWindowController.Toolbar()
            toolbar.setConfig(self.__config)
            toolbar.setViewportController(self.getMapViewportController())

        return self.__objects['controller.mainwindow.toolbar']

    def getMapController(self):
        if not self.__objects.has_key('controller.map'):
            self.__objects['controller.map'] = mapControllerObject = mapController.Map()
            mapControllerObject.setFactory(self.getMapFactory())
            mapControllerObject.setGeometryHelper(self.getHelperGeometry())

        return self.__objects['controller.map']

    def getMapViewportController(self):
        if not self.__objects.has_key('controller.map.viewport'):
            self.__objects['controller.map.viewport'] = mapViewportControllerObject = mapViewportController.Map()
            mapViewportControllerObject.setRoomViewRoutine(self.getViewRoom)

        return self.__objects['controller.map.viewport']

    def getMapFactory(self):
        if not self.__objects.has_key('factory.map'):
            self.__objects['factory.map'] = factoryObject = mapModel.Factory()
            factoryObject.setConfig(self.__config.drawing())

        return self.__objects['factory.map']

    def getViewRoom(self):
        newRoom = viewMap.Room()
        newRoom.setGeometryHelper(self.getHelperGeometry())
        newRoom.setRoomComponents(self.getViewRoomComponents())
        newRoom.setController(self.getRoomController())

        return newRoom

    def getHelperGeometry(self):
        if not self.__objects.has_key('helper.geometry'):
            self.__objects['helper.geometry'] = helperModel.Geometry(self.__config.drawing())

        return self.__objects['helper.geometry']

    def getViewRoomComponents(self):
        if not self.__objects.has_key('view.map.roomComponents'):
            self.__objects['view.map.roomComponents'] = viewMap.RoomComponents(self.__config.drawing())

        return self.__objects['view.map.roomComponents']

    def getPropertiesController(self):
        if not self.__objects.has_key('controller.window.properties'):
            self.__objects['controller.window.properties'] = propertiesController.Properties()

        return self.__objects['controller.window.properties']

    def getRoomController(self):
        if not self.__objects.has_key('controller.map.room'):
            self.__objects['controller.map.room'] = mapViewportController.Room()

        return self.__objects['controller.map.room']