import asyncio
from viam.module.module import Module
try:
    from models.neopixel_pi5 import NeopixelPi5
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.neopixel_pi5 import NeopixelPi5


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
