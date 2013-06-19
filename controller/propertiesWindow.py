__author__ = 'thornag'

from PyQt4 import QtCore, QtGui
from model import map as mapModel
from model.tools import enum
from view.map import Room as roomView
from view.map import Level as levelView

class Properties(QtCore.QObject):

    __uiPropertiesWindow=None

    def __init__(self):
        super(Properties, self).__init__()

    def setWindow(self, uiPropertiesWindow):
        self.__uiPropertiesWindow=uiPropertiesWindow
        uiPropertiesWindow.setController(self)