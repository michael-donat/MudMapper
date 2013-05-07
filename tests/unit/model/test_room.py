
import pytest

from model.room import *
from model.errors import *

from PyQt4 import QtCore, QtGui

class TestClassRoom:

    def test_addExit(self):

        room = Room()
        exit_ = Exit()
        room.addExit(exit_)

        assert room.exits().getExit(exit_.id()).room().id() is room.id()

class TestClassGeometry:

    def test_initMethod(self):
        assert QtCore.QPointF(0, 0) == Geometry().getPoint()

    def test_updateMethod(self):
        assert QtCore.QPointF(10, 10) == Geometry().update(10,10,0,0).getPoint()
        assert QtCore.QRectF(QtCore.QPointF(10, 10),  QtCore.QPointF(20, 20)) == Geometry().update(10,10,20,20).getRect()

        assert QtCore.QPointF(-13, -13) == Geometry().update(-13,-13,0,0).getPoint()
        assert QtCore.QRectF(QtCore.QPointF(-13, -13),  QtCore.QPointF(3, 3)) == Geometry().update(-13,-13,3,3).getRect()

    def test_updateFromPointMethod(self):
        with pytest.raises(RuntimeError):
            Geometry().updateFromPoint(QtCore.QPointF(10,10)).getPoint()

        geometry = Geometry()
        geometry.update(0,0,10,10) #needed x2/y2 to calculate widh height when updatig from points

        assert QtCore.QPointF(10, 10) == geometry.updateFromPoint(QtCore.QPointF(10,10)).getPoint()
        assert QtCore.QRectF(QtCore.QPointF(10, 10),  QtCore.QPointF(20, 20)) == geometry.updateFromPoint(QtCore.QPointF(10,10)).getRect()

        assert QtCore.QPointF(-10, -10) == geometry.updateFromPoint(QtCore.QPointF(-10,-10)).getPoint()
        assert QtCore.QRectF(QtCore.QPointF(-10, -10),  QtCore.QPointF(0, 0)) == geometry.updateFromPoint(QtCore.QPointF(-10,-10)).getRect()

    def test_updateFromRectMethod(self):

        assert QtCore.QRectF(QtCore.QPointF(15,15),QtCore.QPointF(25,25)) == Geometry().updateFromRect(QtCore.QRectF(15,15, 10, 10)).getRect()
        assert QtCore.QPointF(15,15) == Geometry().update(10, 10, 20, 20).updateFromRect(QtCore.QRectF(15,15, 10, 10)).getPoint()

        assert QtCore.QRectF(QtCore.QPointF(-15,-15),QtCore.QPointF(-5,-5)) == Geometry().updateFromRect(QtCore.QRectF(-15,-15, 10, 10)).getRect()
        assert QtCore.QPointF(-15,-15) == Geometry().updateFromRect(QtCore.QRectF(-15,-15, 10, 10)).getPoint()

    def test_updateFromViewMethod(self):

        QGraphicsItem = QtGui.QGraphicsRectItem(0,0,10,10)
        QGraphicsItem.moveBy(15, 15)


        assert QtCore.QRectF(QtCore.QPointF(15,15),QtCore.QPointF(25,25)) == Geometry().updateFromView(QGraphicsItem).getRect()
        assert QtCore.QPointF(15,15) == Geometry().updateFromView(QGraphicsItem).getPoint()

        QGraphicsItem.moveBy(-50, 0)

        assert QtCore.QRectF(QtCore.QPointF(-35,15),QtCore.QPointF(-25,25)) == Geometry().updateFromView(QGraphicsItem).getRect()
        assert QtCore.QPointF(-35,15) == Geometry().updateFromView(QGraphicsItem).getPoint()

@pytest.fixture
def exits():
    return Exits()

class TestClassExits:
    def test_hasExitInDirectionMethod(self, exits):
        exits.addExit(Exit(direction=Directions.N))

        assert True == exits.hasExitInDirection(Directions.N)
        assert False == exits.hasExitInDirection(Directions.S)

    def test_getExitByDirectionMethod(self, exits):

        exit_ = Exit(direction=Directions.N)

        exits.addExit(exit_)

        assert exit_ is exits.getExitByDirection(Directions.N)

        with pytest.raises(NoExitError):
            exits.getExitByDirection(Directions.S)

    def test_getExitByLabelMethod(self, exits):

        exit_ = Exit(label='wyjscie')

        exits.addExit(exit_)

        assert exit_ is exits.getExitByLabel('wyjscie')

        with pytest.raises(NoExitError):
            exits.getExitByLabel('drzwi')

class TestClassExit:
    def test_kwargsInit(self):

        #constants for tests
        eLABEL = 'label'
        eDIRECTION = Directions.N
        eMASKS = ['mask1', 'mask2']
        eONEWAY = True
        eBLOCKED = True
        eROOM = Room()

        exit_ = Exit(direction=eDIRECTION, label=eLABEL, masks=eMASKS, oneWay=eONEWAY, blocked=eBLOCKED, room=eROOM)

        assert exit_.direction() is eDIRECTION
        assert exit_.label() is eLABEL
        assert exit_.masks() is eMASKS
        assert exit_.oneWay() is eONEWAY
        assert exit_.blocked() is eBLOCKED
        assert exit_.room() is eROOM

        with pytest.raises(ValueError):
            exit_ = Exit(masks=False)

        with pytest.raises(ValueError):
            exit_ = Exit(room=False)


