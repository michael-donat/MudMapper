import sys
import unittest
import pytest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
import model

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

        assert MM.container().getMapController().mapModel() is not None, 'Map should be auto created on startup'
        assert len(MM.container().getMapViewportController().scenes()) == 1
        assert MM.mainWindow().getMapViewport().scene() is not None

        MM.exit()






