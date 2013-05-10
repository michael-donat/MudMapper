__author__ = 'thornag'

from PyQt4 import QtGui, uic, QtCore
from model.helper import ComponentRequest
from view.map import Viewport

config = ComponentRequest('Config').instance

class Toolbar:
    @staticmethod
    def getToolbar(mainWindow):

        QToolBar = QtGui.QToolBar(u"Toolbar")

        mainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, QToolBar)
        QToolBar.setAllowedAreas(QtCore.Qt.NoToolBarArea)
        QToolBar.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
        QToolBar.setOrientation(QtCore.Qt.Vertical)
        QToolBar.move(350, 350)

        return QToolBar

class SplashScreen:
    @staticmethod
    def getSplashScreen():
        """
        :rtype: QtGui.QSplashScreen
        """
        QPixmap = QtGui.QPixmap(config.assets().getSplashScreen())
        QSplashScreen = QtGui.QSplashScreen(QPixmap)
        QSplashScreen.show()
        QSplashScreen.raise_()

        return QSplashScreen

class SystemTray:
    @staticmethod
    def getSystemTrayMenu(parent):
        trayIcon = QtGui.QSystemTrayIcon(parent)
        trayIcon.setIcon(QtGui.QIcon(config.assets().getTrayIcon()))
        trayIcon.show()

        return trayIcon

mainWindowBlueprint, mainWindowBase = uic.loadUiType(config.assets().getMainWindowUI())

class MainWindow(mainWindowBlueprint, mainWindowBase):

    mapViewport=None

    def __init__(self, parent=None):
        super(mainWindowBase, self).__init__(parent)
        self.setupUi(self)
        self.mapViewport = Viewport()
        self.setCentralWidget(self.mapViewport)
        self.mapViewport.show()

    def getMapViewport(self):
        return self.mapViewport