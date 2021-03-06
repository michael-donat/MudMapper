import os
import ConfigParser

class RuntimeConfig(ConfigParser.SafeConfigParser):

    __baseDir=None
    __assetsConfig=None

    __width=None
    __height=None

    def __init__(self, argv):
        ConfigParser.SafeConfigParser.__init__(self)
        self.__baseDir = '.'
        self.__assetsConfig = AssetsConfig(self.__baseDir)
        self.__readDefaults()

    def assets(self):
        return self.__assetsConfig

    def __readDefaults(self):
        self.read(self.__baseDir+'/config/defaults.ini')


class AssetsConfig(object):

    __baseDir=None

    IMAGE_SPLASH_SCREEN = '/assets/images/splash.png'

    UI_MAIN_WINDOW = '/gui/map.ui'

    ICON_SYSTEM_TRAY = '/assets/icons/hychsohn-transparent-bw_128x128x32.png'

    def __init__(self, baseDir):
        self.__baseDir = baseDir

    def getSplashScreen(self):
        return self.__baseDir+self.IMAGE_SPLASH_SCREEN

    def getMainWindowUI(self):
        return self.__baseDir+self.UI_MAIN_WINDOW

    def getTrayIcon(self):
        return self.__baseDir+self.ICON_SYSTEM_TRAY