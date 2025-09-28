# NeoPixel Pi5 Module

A Viam module for controlling NeoPixel LED strips on Raspberry Pi 5 using the Pi5Neo library. Provides efficient bulk operations and type-safe pixel control.

## Model ianwhalen:neopixel_pi5:neopixel_pi5

This module wraps the Pi5Neo library to provide clean LED control through Viam's Generic component interface. Features Pydantic models for type safety and validation.

### Configuration

```json
{
  "num_pixels": 64
}
```

#### Attributes

| Name        | Type | Inclusion | Description                           |
|-------------|------|-----------|---------------------------------------|
| `num_pixels`| int  | Optional  | Number of pixels in strip (default: 64) |

#### Example Configuration

```json
{
  "num_pixels": 128
}
```

### DoCommand Actions

The module supports the following actions via DoCommand:

#### set_pixel
Set a specific pixel to an RGB color.

```json
{
  "action": "set_pixel",
  "pixel": 0,
  "red": 255,
  "green": 0,
  "blue": 0
}
```

#### set_all
Set all pixels to the same RGB color.

```json
{
  "action": "set_all",
  "red": 0,
  "green": 255,
  "blue": 0
}
```

#### set_pixels
Set multiple consecutive pixels starting at a specific index.

```json
{
  "action": "set_pixels",
  "pixels": [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
  "start": 0
}
```

#### set_matrix
Set all pixels from a complete matrix of RGB values.

```json
{
  "action": "set_matrix",
  "matrix": [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
}
```
*Note: Matrix must contain exactly `num_pixels` RGB arrays*

#### clear
Turn off all pixels.

```json
{
  "action": "clear"
}
```

#### cycle
Cycle through 8 predefined colors (red, green, blue, yellow, magenta, cyan, orange, purple).

```json
{
  "action": "cycle"
}
```


### Hardware Requirements

- Raspberry Pi 5
- NeoPixel LED strip connected to SPI (default: `/dev/spidev0.0`)
- Pi5Neo library installed

### Implementation Details

- Uses Pi5Neo library for efficient SPI communication
- Pydantic models provide RGB validation (0-255)
- Bulk operations use single `update_strip()` calls for performance
- Type-safe pixel handling with automatic float-to-int conversion
