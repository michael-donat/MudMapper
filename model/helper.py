__author__ = 'donatm'


class Geometry(object):
    configMidPoint = 0
    configBoxSize = 0
    def __init__(self, configuration):
        self.configBoxSize = configuration.getBoxSize()
        self.configMidPoint = configuration.getMidPoint()

    def snapToGrid(self, QFPoint):
        x = int(QFPoint.x() / self.configBoxSize) * self.configBoxSize
        y = int(QFPoint.y() / self.configBoxSize) * self.configBoxSize

        if abs(QFPoint.x()) % self.configBoxSize > self.configMidPoint:
            if(QFPoint.x() < 0):
                x -= self.configBoxSize
            else:
                x += self.configBoxSize

        if abs(QFPoint.y()) % self.configBoxSize > self.configMidPoint:
            if(QFPoint.y() < 0):
                y -= self.configBoxSize
            else:
                y += self.configBoxSize

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