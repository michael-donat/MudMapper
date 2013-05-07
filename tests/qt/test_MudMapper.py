import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

import application

class TestApplication:

    QApplication=None

    def test_bootstrap(self):
        application = application.Application.bootstrap()
        application.QApplication = QApplication()
