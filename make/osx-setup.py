from setuptools import setup

NAME = 'MudMapper'
VERSION = '2.0.0'
ID = 'MudMapper'
COPYRIGHT = 'Copyright Michael Donat'
DATA_FILES = ['gui', 'make/qt.conf', 'config']

"""qt.conf as an empty file is needed cause of some bug, it will crash without it"""

plist = dict(
    CFBundleName                = NAME,
    CFBundleShortVersionString  = ' '.join([NAME, VERSION]),
    CFBundleVersion             = VERSION,
    CFBundleGetInfoString       = NAME,
    CFBundleExecutable          = NAME,
    CFBundleIdentifier          = 'net.michaeldonat.app.%s' % ID,
    NSHumanReadableCopyright    = COPYRIGHT,
    #NSUIElement                 = 1
)


APP = [dict(script='MudMapper.py', plist=plist)]
OPTIONS = {'argv_emulation': True, 'includes': ['sip', 'PyQt4._qt'], 'iconfile':'assets/icons/hychsohn-transparent.icns'}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    data_files = DATA_FILES
)