__author__ = 'donatm'

import math

from uuid import uuid1

def generateId():
    return str(uuid1())

class Geometry(object):
    configMidPoint = 0
    configBoxSize = 0
    configPadding = 0
    def __init__(self, configuration):
        self.configBoxSize = configuration.getBoxSize()
        self.configPadding = configuration.getPadding()

    def snapToGrid(self, QFPoint):

        print 'Event at %sx%s' % (QFPoint.x(), QFPoint.y())

        areaSize = self.configBoxSize + self.configPadding

        x = math.floor(abs(QFPoint.x()) / areaSize) * areaSize
        y = math.floor(abs(QFPoint.y()) / areaSize) * areaSize



        if QFPoint.x() < 0:
            x *= -1
            x -= areaSize

        if QFPoint.y() < 0:
            y *= -1
            y -= areaSize


        x += self.configPadding
        y += self.configPadding

        QFPoint.setX(x)
        QFPoint.setY(y)

        print 'Adapted to %sx%s' % (QFPoint.x(), QFPoint.y())

        print 'Area size %s' % areaSize

        return QFPoint

    def dummy(self):

        if not fromMidpoint and QFPoint.x() < 0: x -= (self.configBoxSize + self.configPadding)
        if not fromMidpoint and QFPoint.y() < 0: y -= (self.configBoxSize + self.configPadding)

        if fromMidpoint and abs(QFPoint.x()) % self.configBoxSize > self.configMidPoint:
            if(QFPoint.x() < 0):
                x -= self.configBoxSize - self.configPadding
            else:
                x += self.configBoxSize + self.configPadding

        if fromMidpoint and +abs(QFPoint.y()) % self.configBoxSize > self.configMidPoint:
            if(QFPoint.y() < 0):
                y -= (self.configBoxSize + self.configPadding)
            else:
                y += (self.configBoxSize + self.configPadding)

        print x, y, self.configPadding

        QFPoint.setX(x)
        QFPoint.setY(y)

        return QFPoint

class ComponentContainer(object):
    def __init__(self):
        self.components = {}
    def __getitem__(self, component):
        try:
            componentClass = self.components[component]
        except KeyError:
            raise KeyError, "Unknown component named %r" % component
        return componentClass()
    def register(self, component, componentClass, *args, **kwargs):
        if callable(componentClass):
            def componentInstance(): return componentClass(*args, **kwargs)
        else:
            def componentInstance(): return componentClass

        self.components[component] = componentInstance

container = ComponentContainer()

class ComponentRequest(object):
    def __init__(self, component):
        self.component = component
    def __get__(self, obj, T):
        return self.result # <-- will request the feature upon first call
    def __getattr__(self, name):
        self.result = container[self.component]
        return self.result