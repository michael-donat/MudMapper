__author__ = 'thornag'

from PyQt4 import QtGui, uic, QtCore
from model.helper import ComponentRequest

config = ComponentRequest('Config').instance

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
    def __init__(self, parent=None):
        super(mainWindowBase, self).__init__(parent)
        self.setupUi(self)

    def getMapViewport(self):
        return self.mapViewport