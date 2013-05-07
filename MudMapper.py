from model.helper import container as DIContainer
from model.config import RuntimeConfig
import sys

#need to register RuntimeConfig dependency first to avoid race conditions
DIContainer.register('Config', RuntimeConfig(sys.argv))

from application import Application as MudMapper

mapper = MudMapper(sys.argv)
mapper.bootstrap()
mapper.initialize()
mapper.load()
mapper.run()