__author__ = 'thornag'

from PyQt4 import QtGui, QtCore

class Keyboard(object):

    def processKeyPressEvent(self):
        pass

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

    mapViewportController = None

    __config=None
    __actions=None

    def setConfig(self, config):
        self.__config = config

    def setViewportController(self, controller):
        self.mapViewportController = controller

    def wireToolbarActions(self, mainWindow, toolbar):

        self.__actions={}

        QActionGroup = QtGui.QActionGroup(toolbar)

        self.__actions['pointer'] = actionPointer = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getPointerIcon()), u"Select", toolbar)
        self.__actions['room'] = actionCreateRoom = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getRoomIcon()), u"Create room", toolbar)
        self.__actions['label'] = actionCreateLabel = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getLabelIcon()), u"Create label", toolbar)
        self.__actions['background'] = actionCreateBackground = QtGui.QAction(QtGui.QIcon(self.__config.assets().toolbar().getFillIcon()), u"Create background", toolbar)

        for action in [actionPointer, actionCreateRoom, actionCreateLabel, actionCreateBackground]:
            action.setCheckable(True)
            action.setShortcutContext(QtCore.Qt.ApplicationShortcut)
            QActionGroup.addAction(action)
            toolbar.addAction(action)

        actionPointer.setChecked(True)

        actionPointer.triggered.connect(self.actionPointer)
        actionCreateRoom.triggered.connect(self.actionCreateRoom)
        actionCreateLabel.triggered.connect(self.actionCreateLabel)
        actionCreateBackground.triggered.connect(self.actionCreateBackground)

        actionPointer.setShortcut('CTRL+1')
        actionPointer.setToolTip('Key: CTRL+1')

        actionCreateRoom.setShortcut('CTRL+2')
        actionCreateRoom.setToolTip('Key: CTRL+2')

        actionCreateLabel.setShortcut('CTRL+3')
        actionCreateLabel.setToolTip('Key: CTRL+3')

        actionCreateBackground.setShortcut('CTRL+4')
        actionCreateBackground.setToolTip('Key: CTRL+4')

    @QtCore.pyqtSlot(bool)
    def resetPointer(self):
        #Will reset only if there is no keyboard modifier
        if QtGui.QApplication.queryKeyboardModifiers() & QtCore.Qt.ControlModifier:
            return
        self.actionPointer(True)

    @QtCore.pyqtSlot(bool)
    def actionPointer(self, state):
        self.mapViewportController.resetClickMode()
        self.__actions['pointer'].setChecked(True)

    @QtCore.pyqtSlot(bool)
    def actionCreateRoom(self, state):
        self.mapViewportController.clickMode(self.mapViewportController.CLICK_MODE.ROOM)
        self.__actions['room'].setChecked(True)

    @QtCore.pyqtSlot(bool)
    def actionCreateLabel(self, state):
        self.mapViewportController.clickMode(self.mapViewportController.CLICK_MODE.LABEL)
        self.__actions['label'].setChecked(True)

    @QtCore.pyqtSlot(bool)
    def actionCreateBackground(self, state):
        self.mapViewportController.clickMode(self.mapViewportController.CLICK_MODE.BACKGROUND)
        self.__actions['background'].setChecked(True)



