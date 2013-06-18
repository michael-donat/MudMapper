
import pytest

from model.helper import Geometry
from PyQt4 import QtCore

import model.map as mapModel

from controller.map import Map as mapController

from tests.signals import ConnectionBox

from mock import MagicMock

@pytest.fixture
def signalSniffer():
    """
    :return: ConnectionBox
    """
    return ConnectionBox()

@pytest.fixture
def mapControllerObject():
    controller = mapController()

    factory = mapModel.Factory()

    config = MagicMock()
    config.getBoxSize.return_value=10

    factory.setConfig(config)

    controller.setFactory(factory)

    geometryHelper = MagicMock()
    geometryHelper.snapToGrid.return_value=QtCore.QPoint(0, 0)

    controller.setGeometryHelper(geometryHelper)

    return controller

class TestControllerMap:

    def test_createNewMapIsEmitting(self, signalSniffer, mapControllerObject):

        controller = mapControllerObject

        controller.mapModelCreated.connect(signalSniffer.slotSlot)

        controller.createMap()

        signalSniffer.assertSignalArrived()
        signalSniffer.assertArgumentTypes(mapModel.Map)

    def test_createNewMapIsDestroyingCurrentMap(self, signalSniffer, mapControllerObject):

        controller = mapControllerObject

        controller.createMap()

        controller.mapModelDestroyed.connect(signalSniffer.slotSlot)

        controller.createMap()

        signalSniffer.assertSignalArrived()
        signalSniffer.assertArgumentTypes(mapModel.Map)

    def test_createRoomRegistersRooms(self, mapControllerObject):

        controller = mapControllerObject
        controller.createMap()

        newRoom = controller.createRoomAt(QtCore.QPoint(0,0))

        assert controller.mapModel().roomById(newRoom.id()) is not None, 'Model has room registered'


