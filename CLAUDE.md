# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Viam robotics module for controlling NeoPixel LED strips on Raspberry Pi 5 using the Pi5Neo library. The module implements a Generic component that can cycle through colors on a configurable number of pixels.

## Key Commands

### Development and Testing
- `./setup.sh` - Creates virtual environment and installs dependencies from requirements.txt
- `./run.sh` - Runs the module locally (calls setup.sh then executes the module)
- `python -m src.main` - Alternative way to run the module directly

### Building and Deployment
- `./build.sh` - Builds the module using PyInstaller and creates deployment archive
- Deploy via Git tags matching pattern `[0-9]+.[0-9]+.[0-9]+` (triggers GitHub Actions)

### Testing Hardware Wiring
- `python test_wiring.py` - Test script for verifying LED strip wiring and functionality

## Architecture

### Core Structure
- `src/main.py` - Entry point that runs the Viam module registry
- `src/models/neopixel_pi5.py` - Viam module wrapper implementing the Generic component interface
- `src/led_controller.py` - Pure LED control logic independent of Viam framework
- `meta.json` - Viam module metadata defining the model and build configuration

### Component Model
- **API**: `rdk:component:generic`
- **Model**: `ianwhalen:neopixel_pi5:neopixel_pi5`
- **Configuration**: Accepts `num_pixels` attribute (defaults to 64)

### Hardware Dependencies
- Uses Pi5Neo library for SPI communication with NeoPixel strips
- Defaults to `/dev/spidev0.0` SPI interface with 800kHz timing
- LED controller will fail fast if Pi5Neo is not available

### DoCommand Interface
The component supports a simple command interface:

#### Available Actions:
- **`set_pixel`** - Set a specific pixel to a color
  - Parameters: `pixel` (index), `red`, `green`, `blue` (0-255)
- **`set_all`** - Set all pixels to the same color  
  - Parameters: `red`, `green`, `blue` (0-255)
- **`clear`** - Turn off all pixels
- **`cycle`** - Cycle through 8 predefined colors with 0.5s intervals

#### Command Format:
```json
{
  "action": "set_pixel",
  "pixel": 5,
  "red": 255,
  "green": 0, 
  "blue": 0
}
```

#### Legacy Support:
Commands with the key "do" still trigger the original cycle behavior for backward compatibility.

## Development Notes

- LED logic is separated in `led_controller.py` for independent testing and reuse
- Uses Viam SDK's EasyResource base class for simplified component development
- Module fails fast on hardware initialization errors
- Virtual environment is automatically managed by setup scripts