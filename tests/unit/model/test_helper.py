
import pytest

from model.helper import Geometry
from PyQt4 import QtCore

@pytest.fixture
def ConfigFixture():
    class Config:
        def getBoxSize(self): return 100
        def getPadding(self): return 20
    return Config()


@pytest.fixture
def GeometryFixture(ConfigFixture):
    return Geometry(ConfigFixture)

class TestClassGeometry:

    def test_snapToGrid(self, GeometryFixture):

        #with area of size 30 (as above)Event at -1540x-700
        assert QtCore.QPoint(-100, -100) == GeometryFixture.snapToGrid(QtCore.QPoint(-100, -100))
        assert QtCore.QPointF(-100, -100) == GeometryFixture.snapToGrid(QtCore.QPointF(-100, -100))
        assert QtCore.QPointF(-220.0, -100.0) == GeometryFixture.snapToGrid(QtCore.QPointF(-173.333333333, -36.6666666667))




