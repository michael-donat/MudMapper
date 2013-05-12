
import pytest

from model.helper import Geometry
from PyQt4 import QtCore

@pytest.fixture
def ConfigFixture():
    class Config:
        def getBoxSize(self): return 20
        def getMidPoint(self): return 10
        def getPadding(self): return 10
    return Config()


@pytest.fixture
def GeometryFixture(ConfigFixture):
    return Geometry(ConfigFixture)

class TestClassGeometry:

    def test_snapToGrid(self, GeometryFixture):

        assert QtCore.QPointF(0, 0) == GeometryFixture.snapToGrid(QtCore.QPointF(5, 5))
        assert QtCore.QPointF(0, 0) == GeometryFixture.snapToGrid(QtCore.QPointF(13, 5))
        assert QtCore.QPointF(0, 0) == GeometryFixture.snapToGrid(QtCore.QPointF(13, 17))
        assert QtCore.QPointF(0, 0) == GeometryFixture.snapToGrid(QtCore.QPointF(21, 21))
        assert QtCore.QPointF(30, 30) == GeometryFixture.snapToGrid(QtCore.QPointF(31, 31))
        assert QtCore.QPointF(-30, -30) == GeometryFixture.snapToGrid(QtCore.QPointF(-5, -5))
        assert QtCore.QPointF(-30, -30) == GeometryFixture.snapToGrid(QtCore.QPointF(-5, -13))
        assert QtCore.QPointF(-30, -30) == GeometryFixture.snapToGrid(QtCore.QPointF(-13, -17))

    def test_snapToHalfGrid(self, GeometryFixture):

        assert QtCore.QPointF(0, 0) == GeometryFixture.snapToHalfGrid(QtCore.QPointF(5, 5))
        assert QtCore.QPointF(20, 0) == GeometryFixture.snapToHalfGrid(QtCore.QPointF(13, 5))
        assert QtCore.QPointF(20, 20) == GeometryFixture.snapToHalfGrid(QtCore.QPointF(13, 17))
        assert QtCore.QPointF(-20, -20) == GeometryFixture.snapToHalfGrid(QtCore.QPointF(-5, -5))
        assert QtCore.QPointF(-20, -30) == GeometryFixture.snapToHalfGrid(QtCore.QPointF(-5, -13))
        assert QtCore.QPointF(-30, -30) == GeometryFixture.snapToHalfGrid(QtCore.QPointF(-13, -17))
