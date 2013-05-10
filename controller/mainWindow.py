__author__ = 'thornag'

from PyQt4 import QtGui
from model.helper import container as di, ComponentRequest

class Bootstrap(object):
    def __init__(self,  mainWindow):
        di.register('controllerFileMenu', FileMenu(mainWindow))


class FileMenu(object):

    mapController = ComponentRequest('controllerMap')

    def __init__(self, menu):
        menu.actionNew.triggered.connect(self.new)
        menu.actionOpen.triggered.connect(self.open)
        menu.actionSave.triggered.connect(self.save)
        menu.actionSaveAs.triggered.connect(self.saveAs)
        menu.actionQuit.triggered.connect(QtGui.qApp.quit)
        menu.actionPreferences.triggered.connect(self.preferences)


    def new(self):
        self.mapController.createMap()

    def open(self):
        pass

    def save(self):
        pass

    def saveAs(self):
        pass


    def preferences(self):
        pass