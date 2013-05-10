import sys

from model.helper import container as DIContainer
from model.config import RuntimeConfig

#need to register RuntimeConfig dependency first to avoid race conditions
DIContainer.register('Config', RuntimeConfig(sys.argv))

from model.helper import ComponentRequest as DIRequest

from controller import mainWindow as mainWindowController, mapViewport as mapViewportController, map as mapController
from PyQt4 import QtGui
import model.map
import view.application as view
import sys


class Application:

    __QApplication=None
    __uiMainWindow=None
    __config=DIRequest('Config')
    __mapRegistry=None
    __controllers=None #used to keep controller reference alive

    def __init__(self):
        self.__controllers=[]

    def bootstrap(self):
        self.__QApplication = QtGui.QApplication([])

    def QApplication(self):
        return self.__QApplication

    def initialize(self):

        application = self.QApplication()
        QSplashScreen = view.SplashScreen.getSplashScreen()
        application.processEvents()

        QSplashScreen.showMessage("Initializing application")
        uiMainWindow = self.__buildUI()
        QSplashScreen.showMessage("Wiring")
        self.__wire()
        QSplashScreen.finish(uiMainWindow)

    def __buildUI(self):

        #let's get main window
        self.__uiMainWindow = uiMainWindow = view.MainWindow()
        self.__uiMainWindow.resize(self.__config.getint('view', 'width'), self.__config.getint('view', 'height'))
        self.__uiMainWindow.setWindowTitle(self.__config.get('meta', 'windowTitle'))

        view.SystemTray.getSystemTrayMenu(uiMainWindow)

        return uiMainWindow

    def __wire(self):
        mainWindowController.Bootstrap(self.mainWindow())
        mapViewportController.Bootstrap(self.mainWindow())
        mapController.Bootstrap()

        self.__wireSignals()

    def __wireSignals(self):

        mapControllerInstance = DIRequest('controllerMap').instance
        mapViewportControllerInstance = DIRequest('controllerMapViewport').instance

        mapControllerInstance.newMapModelCreated.connect(mapViewportControllerInstance.createMap)

    def mainWindow(self):
        return self.__uiMainWindow

    def show(self):
        self.mainWindow().show()
        self.mainWindow().raise_()

    def run(self):
        sys.exit(self.QApplication().exec_())

    def exit(self, code=0):
        self.QApplication().exit(code)


