import sys
import unittest
import pytest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
import model

from model.helper import ComponentRequest

from application import Application as MudMapper

@pytest.fixture
def AppFixture():
    MM = MudMapper()
    MM.bootstrap()
    MM.loadMap()
    MM.show()

    return MM

class TestApplication:

    def test_startUp(self, AppFixture):
        MM = AppFixture

        mapControllerInstance = ComponentRequest('controllerMap').instance

        assert mapControllerInstance.mapModel() is not None, 'Map should be auto created on startup'






