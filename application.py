import sys

from model.helper import container as DIContainer
from model.config import RuntimeConfig
from model.helper import Geometry as GeometryHelper

#need to register RuntimeConfig dependency first to avoid race conditions
DIContainer.register('Config', RuntimeConfig(sys.argv))

from model.helper import ComponentRequest as DIRequest

from controller import mainWindow as mainWindowController, mapViewport as mapViewportController, map as mapController
from PyQt4 import QtGui
import model.map
import view.application as view
from view.map  import changeEmitter as roomViewChangeEmitter
import sys


class Application:

    __QApplication=None
    __uiMainWindow=None
    __config=DIRequest('Config')
    __mapRegistry=None
    __uiToolbar=None
    __controllers=None

    def __init__(self):
        self.__controllers=[]

    def bootstrap(self):

        #will initialize all controllers here

        fileMenuController = mainWindowController.FileMenu()
        toolbarController = mainWindowController.Toolbar()

        mapViewportControllerInstance = mapViewportController.Map()
        mapControllerInstance = mapController.Map()

        self.__controllers.append(fileMenuController)
        self.__controllers.append(mapViewportControllerInstance)
        self.__controllers.append(mapControllerInstance)
        self.__controllers.append(toolbarController)

        #will setup UI bits
        self.__QApplication = application = QtGui.QApplication([])
        QSplashScreen = view.SplashScreen.getSplashScreen()
        application.processEvents()

        QSplashScreen.showMessage("Initializing application")
        self.__uiMainWindow = uiMainWindow = view.MainWindow()
        self.__uiMainWindow.resize(self.__config.getint('view', 'width'), self.__config.getint('view', 'height'))
        self.__uiMainWindow.setWindowTitle(self.__config.get('meta', 'windowTitle'))

        view.SystemTray.getSystemTrayMenu(uiMainWindow)

        self.__uiToolbar = uiToolbar = view.Toolbar.getToolbar(uiMainWindow)
        QSplashScreen.showMessage("Wiring")
        QSplashScreen.finish(uiMainWindow)

        #wire it all together

        mapViewportControllerInstance.setView(uiMainWindow.getMapViewport())

        mapControllerInstance.mapModelCreated.connect(mapViewportControllerInstance.createMap)
        mapControllerInstance.mapModelDestroyed.connect(mapViewportControllerInstance.destroyMap)
        mapControllerInstance.mapLevelSelected.connect(mapViewportControllerInstance.selectLevel)
        mapControllerInstance.mapRoomCreated.connect(mapViewportControllerInstance.createRoom)

        mapViewportControllerInstance.roomCreateRequest.connect(mapControllerInstance.createRoomAt)

        roomViewChangeEmitter.roomPositionChanged.connect(mapControllerInstance.roomPositionChanged)
        roomViewChangeEmitter.roomDoubleClicked.connect(mapControllerInstance.markCurrentlyVisitedRoom)
        roomViewChangeEmitter.roomDoubleClicked.connect(mapViewportControllerInstance.markCurrentlyVisitedRoom)

        fileMenuController.wireMenu(uiMainWindow)
        toolbarController.wireToolbarActions(uiMainWindow, uiToolbar)

        geometryHelper = GeometryHelper(self.__config.drawing())

        DIContainer.register('controllerMap', mapControllerInstance)
        DIContainer.register('controllerMapViewport', mapViewportControllerInstance)
        DIContainer.register('geometryHelper', geometryHelper)


    def QApplication(self):
        return self.__QApplication


    def mainWindow(self):
        return self.__uiMainWindow

    def toolbar(self):
        return self.__uiToolbar

    def show(self):
        self.mainWindow().show()
        self.mainWindow().raise_()
        self.toolbar().show()
        self.toolbar().raise_()

    def run(self):
        sys.exit(self.QApplication().exec_())

    def loadMap(self):
        mapControllerInstance = DIRequest('controllerMap').instance.createMap()

    def exit(self, code=0):
        self.QApplication().exit(code)


