
import pytest

from model.helper import Geometry
from PyQt4 import QtCore

import model.map as mapModel

from controller.map import Map as mapController

from tests.signals import ConnectionBox

@pytest.fixture
def signalSniffer():
    """
    :return: ConnectionBox
    """
    return ConnectionBox()

class TestControllerMap:

    def test_createNewMapIsEmitting(self, signalSniffer):

        controller = mapController()

        controller.newMapModelCreated.connect(signalSniffer.slotSlot)

        controller.createMap()

        signalSniffer.assertSignalArrived()
        signalSniffer.assertArgumentTypes(mapModel.Map)




