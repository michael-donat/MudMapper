__author__ = 'thornag'

from PyQt4 import QtGui

class Bootstrap(object):
    def __init__(self, controllerRegistry, mainWindow):
        controllerRegistry += [FileMenu(mainWindow)]


class FileMenu(object):
    def __init__(self, menu):
        menu.actionNew.triggered.connect(self.new)
        menu.actionOpen.triggered.connect(self.open)
        menu.actionSave.triggered.connect(self.save)
        menu.actionSaveAs.triggered.connect(self.saveAs)
        menu.actionQuit.triggered.connect(QtGui.qApp.quit)
        menu.actionPreferences.triggered.connect(self.preferences)


    def new(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def saveAs(self):
        pass


    def preferences(self):
        pass