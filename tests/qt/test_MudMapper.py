import sys
import unittest
import pytest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from application import Application as MudMapper

@pytest.fixture
def AppFixture():
    MM = MudMapper()
    MM.bootstrap()
    MM.initialize()
    MM.show()

    return MM

class TestApplication:

    def test_startUp(self, AppFixture):
        MM = AppFixture

        assert MM.mainWindow().getMapViewport().scene() is None




