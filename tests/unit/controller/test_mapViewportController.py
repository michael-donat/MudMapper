
import pytest, sys

from model.helper import Geometry
from PyQt4 import QtCore, QtGui

from mock import MagicMock

import model.map as mapModel

@pytest.fixture(scope="module")
def app():
    return QtGui.QApplication(sys.argv)

from controller.mapViewport import Map as mapController

class TestControllerMap:

    def test_createMap(self, app):

        mockViewport = MagicMock()
        mockMapModel = MagicMock()
        lvl1Mock = MagicMock()
        lvl1Mock.id.return_value='lvl1'
        lvl2Mock = MagicMock()
        lvl2Mock.id.return_value='lvl2'
        mockMapModel.id.return_value = 'some_id'
        mockMapModel.levels.return_value = {'level1':lvl1Mock, 'level2':lvl2Mock}

        controller = mapController()
        controller.setView(mockViewport)
        controller.createMap(mockMapModel)

        assert controller.scenes().has_key('some_id')
        assert len(controller.scenes()['some_id']) == 2

    def test_destroyMap(self, app):

        mockViewport = MagicMock()
        mockMapModel = MagicMock()
        mockMapModel.id.return_value = 'some_id'

        controller = mapController()
        controller.setView(mockViewport)
        controller.createMap(mockMapModel)

        controller.destroyMap(mockMapModel)

        assert len(controller.scenes()) is 0







