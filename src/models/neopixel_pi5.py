from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, Tuple

from typing_extensions import Self
from viam.components.generic import Generic
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes

from led_controller import LEDController
from pixel_models import Pixel, PixelStrip


class NeopixelPi5(Generic, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("ianwhalen", "neopixel_pi5"), "neopixel_pi5"
    )

    def __init__(self, name: str):
        super().__init__(name)
        self.led_controller = None
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

        try:
            self.led_controller = LEDController(
                spi_device="/dev/spidev0.0", num_pixels=self.num_pixels, frequency=800
            )
            self.logger.info(
                f"LED controller initialized with {self.num_pixels} pixels"
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize LED controller: {e}")
            raise

        return super().reconfigure(config, dependencies)

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        self.logger.info(f"Received command: {command}")

        if self.led_controller is None:
            raise RuntimeError("LED controller not initialized")

        # Handle commands
        if "action" not in command:
            raise ValueError("Command must include 'action' field")

        action = command["action"]

        try:
            if action == "set_pixel":
                pixel_index = command.get("pixel", 0)
                red = command.get("red", 0)
                green = command.get("green", 0)
                blue = command.get("blue", 0)
                pixel = Pixel(red=red, green=green, blue=blue)
                await self.led_controller.set_pixel(pixel_index, pixel)
                return {
                    "status": "completed",
                    "message": f"Set pixel {pixel_index} to RGB({red}, {green}, {blue})",
                }

            elif action == "set_all":
                red = command.get("red", 0)
                green = command.get("green", 0)
                blue = command.get("blue", 0)
                pixel = Pixel(red=red, green=green, blue=blue)
                await self.led_controller.set_all(pixel)
                return {
                    "status": "completed",
                    "message": f"Set all pixels to RGB({red}, {green}, {blue})",
                }

            elif action == "set_pixels":
                pixel_data = command.get("pixels", [])
                start_index = command.get("start", 0)
                if not pixel_data:
                    raise ValueError(
                        "pixels parameter is required for set_pixels action"
                    )
                pixel_strip = PixelStrip.from_lists(pixel_data, start_index)
                await self.led_controller.set_pixels(pixel_strip)
                return {
                    "status": "completed",
                    "message": f"Set {len(pixel_data)} pixels starting at index {start_index}",
                }

            elif action == "set_matrix":
                pixel_matrix = command.get("matrix", [])
                if not pixel_matrix:
                    raise ValueError(
                        "matrix parameter is required for set_matrix action"
                    )
                pixels = [Pixel.from_list(rgb) for rgb in pixel_matrix]
                await self.led_controller.set_all_pixels(pixels)
                return {
                    "status": "completed",
                    "message": f"Set all {len(pixel_matrix)} pixels from matrix",
                }

            elif action == "clear":
                await self.led_controller.clear()
                return {"status": "completed", "message": "Cleared all pixels"}

            elif action == "cycle":
                return await self.led_controller.cycle_colors()

            else:
                raise NotImplementedError(f"Action '{action}' is not implemented")

        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return {"status": "error", "message": str(e)}

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: float | None = None
    ) -> Sequence[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()
