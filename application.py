import sys

from model.config import RuntimeConfig
from model.helper import Geometry as GeometryHelper
from PyQt4 import QtGui
import model.map
import view.application as view
import view.map as viewMap
import sys
from model.dic import Container

class Application:

    __QApplication=None
    __uiMainWindow=None
    __uiPropertiesWindow=None
    __mapRegistry=None
    __uiToolbar=None
    __dic=None

    def bootstrap(self):

        config = RuntimeConfig(sys.argv)

        self.__dic = container = Container(config)

        #will initialize all controllers here

        fileMenuController = container.getMainWindowFileMenuController()
        toolbarController = container.getMainWindowToolbarController()

        mapViewportControllerInstance = container.getMapViewportController()
        mapControllerInstance = container.getMapController()

        propertiesController = container.getPropertiesController()

        #will setup UI bits
        view.config = config
        self.__QApplication = application = QtGui.QApplication([])
        QSplashScreen = view.SplashScreen.getSplashScreen()
        application.processEvents()

        QSplashScreen.showMessage("Initializing application")
        self.__uiMainWindow = uiMainWindow = view.createMainWindow()
        self.__uiMainWindow.resize(config.getint('view', 'width'), config.getint('view', 'height'))
        self.__uiMainWindow.setWindowTitle(config.get('meta', 'windowTitle'))

        self.__uiPropertiesWindow = uiPropertiesWindow = view.createPropertiesWindow()

        view.SystemTray.getSystemTrayMenu(uiMainWindow)

        self.__uiToolbar = uiToolbar = view.Toolbar.getToolbar(uiMainWindow)
        QSplashScreen.showMessage("Wiring")
        QSplashScreen.finish(uiMainWindow)

        #wire it all together

        mapViewportControllerInstance.setView(uiMainWindow.getMapViewport())
        propertiesController.setWindow(uiPropertiesWindow)


        mapControllerInstance.mapModelCreated.connect(mapViewportControllerInstance.createMap)
        mapControllerInstance.mapModelDestroyed.connect(mapViewportControllerInstance.destroyMap)
        mapControllerInstance.mapLevelSelected.connect(mapViewportControllerInstance.selectLevel)
        mapControllerInstance.mapRoomCreated.connect(mapViewportControllerInstance.createRoom)
        mapControllerInstance.mapRoomCreated.connect(toolbarController.actionPointer)
        mapViewportControllerInstance.roomCreateRequest.connect(mapControllerInstance.createRoomAt)

        fileMenuController.wireMenu(uiMainWindow)
        toolbarController.wireToolbarActions(uiMainWindow, uiToolbar)



    def QApplication(self):
        return self.__QApplication


    def mainWindow(self):
        return self.__uiMainWindow

    def toolbar(self):
        return self.__uiToolbar

    def propertiesWindow(self):
        return self.__uiPropertiesWindow

    def show(self):
        self.mainWindow().show()
        self.mainWindow().raise_()
        self.toolbar().show()
        self.toolbar().raise_()
        self.propertiesWindow().raise_()

    def run(self):
        sys.exit(self.QApplication().exec_())

    def loadMap(self):
        mapControllerInstance = self.__dic.getMapController().createMap()

    def exit(self, code=0):
        self.QApplication().exit(code)

    def container(self):
        return self.__dic

