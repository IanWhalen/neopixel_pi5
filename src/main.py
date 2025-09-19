import asyncio

from viam.module.module import Module

try:
    from models.neopixel_pi5 import NeopixelPi5  # noqa: F401
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.neopixel_pi5 import NeopixelPi5  # type: ignore #noqa: F401


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
