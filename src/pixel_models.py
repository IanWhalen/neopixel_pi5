from pydantic import BaseModel, Field


class Pixel(BaseModel):
    """RGB pixel with validation"""

    red: int = Field(ge=0, le=255, description="Red component (0-255)")
    green: int = Field(ge=0, le=255, description="Green component (0-255)")
    blue: int = Field(ge=0, le=255, description="Blue component (0-255)")

    def to_tuple(self) -> tuple[int, int, int]:
        """Convert to RGB tuple for Pi5Neo library"""
        return (self.red, self.green, self.blue)

    @classmethod
    def from_list(cls, rgb_list: list[int]) -> "Pixel":
        """Create Pixel from [r, g, b] list"""
        if len(rgb_list) != 3:
            raise ValueError("RGB list must contain exactly 3 values")
        return cls(red=rgb_list[0], green=rgb_list[1], blue=rgb_list[2])

    @classmethod
    def from_tuple(cls, rgb_tuple: tuple[int, int, int]) -> "Pixel":
        """Create Pixel from (r, g, b) tuple"""
        return cls(red=rgb_tuple[0], green=rgb_tuple[1], blue=rgb_tuple[2])


class PixelStrip(BaseModel):
    """Collection of pixels for bulk operations"""

    pixels: list[Pixel]
    start_index: int = Field(ge=0, default=0, description="Starting pixel index")

    def to_tuples(self) -> list[tuple[int, int, int]]:
        """Convert all pixels to RGB tuples"""
        return [pixel.to_tuple() for pixel in self.pixels]

    @classmethod
    def from_lists(
        cls,
        pixel_lists: list[list[int]],
        start_index: int = 0,
    ) -> "PixelStrip":
        """Create PixelStrip from list of [r, g, b] lists"""
        pixels = [Pixel.from_list(rgb_list) for rgb_list in pixel_lists]
        return cls(pixels=pixels, start_index=start_index)
