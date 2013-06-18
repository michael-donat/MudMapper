import os
import ConfigParser
from PyQt4 import QtCore

class RuntimeConfig(ConfigParser.SafeConfigParser):

    __baseDir=None
    __assetsConfig=None

    __width=None
    __height=None

    __drawingConfig=None

    def __init__(self, argv):
        ConfigParser.SafeConfigParser.__init__(self)
        self.__baseDir = '.'
        self.__assetsConfig = AssetsConfig(self.__baseDir)
        self.__readDefaults()

    def assets(self):
        return self.__assetsConfig

    def drawing(self):
        if self.__drawingConfig is None:
            self.__drawingConfig = DrawingConfig(self)

        return self.__drawingConfig

    def __readDefaults(self):
        self.read(self.__baseDir+'/config/defaults.ini')

class DrawingConfig(object):

    __boxSize=None
    __midPoint=None
    __edgeSize=None
    __exitSize=None
    __padding=None

    def __init__(self, config):
        self.__boxSize = config.getint('room', 'box')
        self.__midPoint = config.getint('room', 'box') / 2
        self.__edgeSize = config.getint('room', 'inside')
        self.__exitSize = config.getint('room', 'exit')
        self.__padding = config.getint('room', 'padding')

    def getPadding(self):
        return self.__padding

    def getExitSize(self):
        return self.__exitSize

    def getBoxSize(self):
        return self.__boxSize

    def getRoomSize(self):
        return self.__edgeSize

    def getMidPoint(self):
        return self.__midPoint

    def getBoundingRect(self):
        return QtCore.QRectF(0,0,self.__boxSize, self.__boxSize)

class AssetsConfig(object):

    __baseDir=None
    __toolbar=None

    IMAGE_SPLASH_SCREEN = '/assets/images/splash.png'

    UI_MAIN_WINDOW = '/gui/map.ui'
    UI_PROPERTIES_WINDOW = '/gui/properties.ui'

    ICON_SYSTEM_TRAY = '/assets/icons/hychsohn-transparent-bw_128x128x32.png'

    def __init__(self, baseDir):
        self.__baseDir = baseDir
        self.__toolbar = ToolbarConfig(baseDir)

    def getSplashScreen(self):
        return self.__baseDir+self.IMAGE_SPLASH_SCREEN

    def getMainWindowUI(self):
        return self.__baseDir+self.UI_MAIN_WINDOW

    def getPropertiesWindowUI(self):
        return self.__baseDir+self.UI_PROPERTIES_WINDOW

    def getTrayIcon(self):
        return self.__baseDir+self.ICON_SYSTEM_TRAY

    def toolbar(self):
        return self.__toolbar

class ToolbarConfig(object):

    ROOM_ICON = '/assets/images/toolbar/room.png'
    LABEL_ICON = '/assets/images/toolbar/label.png'
    FILL_ICON = '/assets/images/toolbar/background.png'
    POINTER_ICON = '/assets/images/toolbar/pointer.png'

    __baseDir=None

    def __init__(self, baseDir):
        self.__baseDir = baseDir

    def getRoomIcon(self):
        return self.__baseDir+self.ROOM_ICON

    def getFillIcon(self):
        return self.__baseDir+self.FILL_ICON

    def getLabelIcon(self):
        return self.__baseDir+self.LABEL_ICON

    def getPointerIcon(self):
        return self.__baseDir+self.POINTER_ICON
