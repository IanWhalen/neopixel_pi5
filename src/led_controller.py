from pixel_models import Pixel, PixelStrip

try:
    from pi5neo import Pi5Neo  # type: ignore
except ImportError as e:
    print(f"IMPORT ERROR: Failed to import pi5neo: {e}")
    raise


class LEDController:
    """Simple wrapper for Pi5Neo library with efficient bulk operations"""

    def __init__(
        self,
        spi_device: str = "/dev/spidev0.0",
        num_pixels: int = 64,
        frequency: int = 800,
    ):
        self.num_pixels = num_pixels
        self.pixels = Pi5Neo(spi_device, num_pixels, frequency)

    async def set_pixel(self, pixel_index: int, pixel: Pixel) -> None:
        """Set a specific pixel to RGB color"""
        rgb = pixel.to_tuple()
        self.pixels.set_led_color(pixel_index, rgb[0], rgb[1], rgb[2])
        self.pixels.update_strip(sleep_duration=None)

    async def set_all(self, pixel: Pixel) -> None:
        """Set all pixels to the same RGB color using efficient fill_strip"""
        rgb = pixel.to_tuple()
        self.pixels.fill_strip(rgb[0], rgb[1], rgb[2])
        self.pixels.update_strip(sleep_duration=None)

    async def set_pixels(self, pixel_strip: PixelStrip) -> None:
        """Set multiple pixels from a PixelStrip"""
        rgb_tuples = pixel_strip.to_tuples()
        for i, (red, green, blue) in enumerate(rgb_tuples):
            self.pixels.set_led_color(pixel_strip.start_index + i, red, green, blue)
        self.pixels.update_strip(sleep_duration=None)

    async def set_all_pixels(self, pixels: list[Pixel]) -> None:
        """Set all pixels from a list of Pixel models"""
        for i, pixel in enumerate(pixels):
            red, green, blue = pixel.to_tuple()
            self.pixels.set_led_color(i, red, green, blue)
        self.pixels.update_strip(sleep_duration=None)

    async def clear(self) -> None:
        """Turn off all pixels using efficient clear_strip"""
        self.pixels.clear_strip()
        self.pixels.update_strip(sleep_duration=None)

    async def cycle_colors(self) -> dict[str, str]:
        """Cycle through all lights with different colors"""
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
                    self.pixels.set_led_color(i, color[0], color[1], color[2])

                # Update the strip
                self.pixels.update_strip(sleep_duration=None)

                # Wait before next color
                import asyncio

                await asyncio.sleep(0.5)

            # Turn off all pixels at the end
            for i in range(self.num_pixels):
                self.pixels.set_led_color(i, 0, 0, 0)
            self.pixels.update_strip(sleep_duration=None)

            return {
                "status": "completed",
                "message": f"Cycled through {len(colors)} colors on {self.num_pixels} pixels",
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}
