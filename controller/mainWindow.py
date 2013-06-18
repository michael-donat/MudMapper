__author__ = 'thornag'

from PyQt4 import QtGui, QtCore

class FileMenu(object):

    mapController = None#ComponentRequest('controllerMap')

    def __init__(self):
        pass

    def wireMenu(self, menu):
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

class Toolbar():

    mapViewportController = None#ComponentRequest('controllerMapViewport')

    __config=None

    def setConfig(self, config):
        self.__config = config

    def setViewportController(self, controller):
        self.mapViewportController = controller

    def wireToolbarActions(self, mainWindow, toolbar):

        QActionGroup = QtGui.QActionGroup(toolbar)

        actionPointer = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getPointerIcon()), u"Select", toolbar)
        actionCreateRoom = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getRoomIcon()), u"Create room", toolbar)
        actionCreateLabel = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getLabelIcon()), u"Create label", toolbar)
        actionCreateBackground = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getFillIcon()), u"Create background", toolbar)

        for action in [actionPointer, actionCreateRoom, actionCreateLabel, actionCreateBackground]:
            action.setCheckable(True)
            QActionGroup.addAction(action)
            toolbar.addAction(action)

        actionPointer.setChecked(True)

        actionPointer.triggered.connect(self.actionPointer)
        actionCreateRoom.triggered.connect(self.actionCreateRoom)
        actionCreateLabel.triggered.connect(self.actionCreateLabel)
        actionCreateBackground.triggered.connect(self.actionCreateBackground)

    @QtCore.pyqtSlot(bool)
    def actionPointer(self, state):
        self.mapViewportController.resetClickMode()

    @QtCore.pyqtSlot(bool)
    def actionCreateRoom(self, state):
        self.mapViewportController.clickMode(self.mapViewportController.CLICK_MODE.ROOM)

    @QtCore.pyqtSlot(bool)
    def actionCreateLabel(self, state):
        self.mapViewportController.clickMode(self.mapViewportController.CLICK_MODE.LABEL)

    @QtCore.pyqtSlot(bool)
    def actionCreateBackground(self, state):
        self.mapViewportController.clickMode(self.mapViewportController.CLICK_MODE.BACKGROUND)



