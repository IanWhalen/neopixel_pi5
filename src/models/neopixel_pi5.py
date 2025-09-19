import asyncio
from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, Tuple

try:
    from pi5neo import Pi5Neo  # type: ignore # noqa: F401
except ImportError as e:
    print(f"IMPORT ERROR: Failed to import pi5neo: {e}")
    import sys

    print(f"Python path: {sys.path}")
    print("Installed packages:")
    import subprocess

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"], capture_output=True, text=True
        )
        print(result.stdout)
    except Exception as pip_error:
        print(f"Failed to run pip list: {pip_error}")
    raise
from typing_extensions import Self
from viam.components.generic import Generic
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes


class NeopixelPi5(Generic, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("ianwhalen", "neopixel_pi5"), "neopixel_pi5"
    )

    def __init__(self, name: str):
        super().__init__(name)
        self.pixels = None
        self.num_pixels = 64  # Default number of pixels

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Generic component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both required and optional)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any required dependencies or optional dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Tuple[Sequence[str], Sequence[str]]: A tuple where the
                first element is a list of required dependencies and the
                second element is a list of optional dependencies
        """
        return [], []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both required and optional)
        """
        # Get number of pixels from config
        if hasattr(config, "attributes") and config.attributes:
            self.num_pixels = config.attributes.get("num_pixels", 64)

        if Pi5Neo is not None:
            try:
                self.pixels = Pi5Neo("/dev/spidev0.0", self.num_pixels, 800)
                self.logger.warning(f"Pixels value: {self.pixels}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Pi5Neo: {e}")
                self.pixels = None

        self.logger.warning("got here after Pi5Neo initialization")

        return super().reconfigure(config, dependencies)

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        if "do" in command:
            return await self._cycle_lights()
        else:
            self.logger.error(f"Unknown command: {command}")
            raise NotImplementedError(f"Command {command} is not implemented")

    async def _cycle_lights(self) -> Mapping[str, ValueTypes]:
        """Cycle through all lights with different colors"""
        if self.pixels is None:
            self.logger.warning("Pi5Neo not available, simulating light cycle")
            # Simulate the cycling for testing on non-Pi5 systems
            colors = [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
                (0, 255, 255),
            ]
            for i, color in enumerate(colors):
                self.logger.info(
                    f"Simulating: Setting all {self.num_pixels} pixels to color {color}"
                )
                await asyncio.sleep(0.5)
            return {
                "status": "completed",
                "message": f"Simulated cycling {len(colors)} colors on {self.num_pixels} pixels",
            }

        try:
            # Define a sequence of colors to cycle through
            colors = [
                (255, 0, 0),  # Red
                (0, 255, 0),  # Green
                (0, 0, 255),  # Blue
                (255, 255, 0),  # Yellow
                (255, 0, 255),  # Magenta
                (0, 255, 255),  # Cyan
                (255, 128, 0),  # Orange
                (128, 0, 255),  # Purple
            ]

            # Cycle through each color
            for color in colors:
                # Set all pixels to the current color
                for i in range(self.num_pixels):
                    self.pixels.set_pixel(i, color[0], color[1], color[2])

                # Update the strip
                self.pixels.update_strip()

                # Wait before next color
                await asyncio.sleep(0.5)

            # Turn off all pixels at the end
            for i in range(self.num_pixels):
                self.pixels.set_pixel(i, 0, 0, 0)
            self.pixels.update_strip()

            self.logger.info(f"Successfully cycled through {len(colors)} colors")
            return {
                "status": "completed",
                "message": f"Cycled through {len(colors)} colors on {self.num_pixels} pixels",
            }

        except Exception as e:
            self.logger.error(f"Error cycling lights: {e}")
            return {"status": "error", "message": str(e)}

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> Sequence[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()
