__author__ = 'donatm'


class Geometry(object):
    configMidPoint = 0
    configBoxSize = 0
    configPadding = 0
    def __init__(self, configuration):
        self.configBoxSize = configuration.getBoxSize()
        self.configMidPoint = configuration.getMidPoint()
        self.configPadding = configuration.getPadding()

    def snapToHalfGrid(self, QFPoint, fromMidpoint=False):
        x = int(QFPoint.x() / (self.configBoxSize / 2)) * (self.configBoxSize / 2)
        y = int(QFPoint.y() / (self.configBoxSize / 2)) * (self.configBoxSize / 2)

        if not fromMidpoint and QFPoint.x() < 0: x -= self.configBoxSize / 2
        if not fromMidpoint and QFPoint.y() < 0: y -= self.configBoxSize / 2

        if fromMidpoint and abs(QFPoint.x()) % (self.configBoxSize / 2) > (self.configMidPoint / 2):
            if(QFPoint.x() < 0):
                x -= self.configBoxSize / 2
            else:
                x += self.configBoxSize / 2

        if fromMidpoint and abs(QFPoint.y()) % (self.configBoxSize / 2) > (self.configMidPoint / 2):
            if(QFPoint.y() < 0):
                y -= self.configBoxSize / 2
            else:
                y += self.configBoxSize / 2

        QFPoint.setX(x)
        QFPoint.setY(y)

        return QFPoint

    def snapToGrid(self, QFPoint, fromMidpoint=False):
        x = int(QFPoint.x() / (self.configBoxSize + self.configPadding)) * self.configBoxSize
        y = int(QFPoint.y() / (self.configBoxSize + self.configPadding)) * self.configBoxSize

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