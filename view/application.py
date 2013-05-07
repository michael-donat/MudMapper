__author__ = 'thornag'

from PyQt4 import QtGui, uic
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
        return QSplashScreen


mainWindowBlueprint, mainWindowBase = uic.loadUiType(config.assets().getMainWindowUI())

class MainWindow(mainWindowBlueprint, mainWindowBase):
    def __init__(self, parent=None):
        super(mainWindowBase, self).__init__(parent)
        self.setupUi(self)

    def mapViewport(self):
        return self.mapViewport