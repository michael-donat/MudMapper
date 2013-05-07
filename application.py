from model.helper import container as DIContainer
from model.helper import ComponentRequest as DIRequest
from model.config import RuntimeConfig
from controller import mainWindow as mainWindowController, mapViewport as mapViewportController
from PyQt4 import QtGui
import model.map
import view.application as view
import sys


class Application:

    __argv=None
    __QApplication=None
    __uiMainWindow=None
    __config=DIRequest('Config')
    __mapRegistry=None
    __controllers=None #used to keep controller reference alive

    def __init__(self, argv):
        self.__argv = argv
        self.__controllers=[]

    def __wireDependencies(self):
        self.__mapRegistry = model.map.MapRegistry()
        DIContainer.register('MapRegistry', self.__mapRegistry)

    def bootstrap(self):
        self.__wireDependencies()
        self.__QApplication = QtGui.QApplication(self.__argv)

    def QApplication(self):
        return self.__QApplication

    def initialize(self):

        application = self.QApplication()
        QSplashScreen = view.SplashScreen.getSplashScreen()
        QSplashScreen.show()
        QSplashScreen.raise_()
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

        return uiMainWindow

    def __wire(self):
        mainWindowController.Bootstrap(self.__controllers, self.mainWindow())
        mapViewportController.Bootstrap(self.__controllers, self.__mapRegistry, self.mainWindow())

    def mainWindow(self):
        return self.__uiMainWindow

    def load(self):
        map = self.__mapRegistry.createMap()


    def run(self):
        self.mainWindow().show()
        self.mainWindow().raise_()
        sys.exit(self.QApplication().exec_())


