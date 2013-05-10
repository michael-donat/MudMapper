
from PyQt4 import QtCore, QtGui

def main():
    qapp = QtGui.QApplication([])

    w = QtGui.QMainWindow()

    t = QtGui.QToolBar(u"Toolbar")
    t.addAction(QtGui.QAction(u"action", w))

    w.addToolBar(QtCore.Qt.LeftToolBarArea, t)

    w.show()

    t.setAllowedAreas(QtCore.Qt.NoToolBarArea)
    t.setOrientation(QtCore.Qt.Vertical)
    p = t.mapToGlobal(QtCore.QPoint(0, 0))
    t.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
    t.move(p.x() + 30, p.y() + 50)
    t.adjustSize()

    t.show()

    qapp.exec_()

if __name__ == "__main__":
    main()