# MP4 to ASCII Video Player

A terminal-based video player that converts MP4 videos to ASCII art and plays them in real-time with synchronized audio.

![ASCII Video Player Demo](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- 🎥 Real-time MP4 to ASCII conversion
- 🔊 Synchronized audio playback
- ⚡ Adjustable FPS control
- 🎨 Two character sets: Standard ASCII and Unicode blocks
- 📱 Dynamic terminal size adaptation
- 📊 Real-time FPS counter
- 🌐 Built-in video download capability
- 🎵 Multiple audio backends (ffplay, pygame)

## Demo

The player converts video frames to ASCII art using different character sets:

**Standard ASCII Mode:**
```
....'''',,,::::;;;;!!!!>>>>~~~~++++____----????]]]]}}}}
1111))))||||\\\\////ttttffffrrrrxxxxnnnnuuuuvvvvcccczzzz
XXXXYYYUUUJJJCCCLLLLQQQQ0000OOOZZZmmmwwwqqpppddddbbbkkkhh
aaaooo***###MMMWWW&&&888%%%%BBB@@@$$$
```

**Block Character Mode:**
```
░░░░▒▒▒▒▓▓▓▓████░░░░▒▒▒▒▓▓▓▓████░░░░▒▒▒▒▓▓▓▓████
▒▒▒▒▓▓▓▓████░░░░▒▒▒▒▓▓▓▓████░░░░▒▒▒▒▓▓▓▓████░░░░
▓▓▓▓████░░░░▒▒▒▒▓▓▓▓████░░░░▒▒▒▒▓▓▓▓████░░░░▒▒▒▒
```

## Requirements

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg python3 python3-pip

# macOS (with Homebrew)
brew install ffmpeg python3

# Windows (with Chocolatey)
choco install ffmpeg python3
```

### Python Dependencies
```bash
pip install opencv-python pygame numpy requests
```

**Optional dependencies:**
```bash
pip install moviepy  # Alternative audio extraction
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Bali0531-RC/mp4-to-ascii-player.git
cd mp4-to-ascii-player
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the player:**
```bash
python ascii.py apple  # Play built-in demo video
```

## Usage

### Basic Usage
```bash
python ascii.py <video> [fps] [blocks]
```

### Parameters
- `<video>`: Video file path or 'apple' for demo video
- `[fps]`: Optional FPS override (e.g., 30, 60)
- `[blocks]`: Character set selection (true/false)

### Examples

**Play demo video:**
```bash
python ascii.py apple
```

**Play with custom FPS:**
```bash
python ascii.py apple 60
```

**Play with block characters:**
```bash
python ascii.py apple 30 true
```

**Play custom video:**
```bash
python ascii.py myvideo.mp4 24 false
```

**Play with automatic .mp4 extension:**
```bash
python ascii.py myvideo  # Looks for myvideo.mp4
```

### Character Set Options

| Parameter | Description | Characters |
|-----------|-------------|------------|
| `false` or `0` | Standard ASCII | ` .'^\",;Il!><~+-?}{)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$` |
| `true` or `1` | Unicode blocks | ` .'^\",;Il!~+-?|\\tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$░▒▓█` |

## Controls

- **CTRL+C**: Exit the player
- **Terminal resize**: Automatically adapts to new terminal size

## How It Works

1. **Video Processing**: OpenCV reads the video frame by frame
2. **Conversion**: Each frame is resized to terminal dimensions and converted to grayscale
3. **ASCII Mapping**: Pixel brightness values are mapped to ASCII characters
4. **Audio Sync**: Audio is played in parallel using ffplay or pygame
5. **Display**: Frames are displayed in the terminal with ANSI escape codes

## Technical Details

### ASCII Conversion Algorithm
```python
# Grayscale conversion
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Character mapping
ascii_index = int(pixel_value / 255 * (len(ascii_chars) - 1))
ascii_char = ascii_chars[ascii_index]
```

### Performance Optimization
- **Frame differencing**: Only updates changed parts
- **Adaptive timing**: Maintains proper FPS with frame skipping/delaying
- **Terminal optimization**: Uses ANSI escape codes for efficient rendering

### Audio Backends
1. **ffplay (primary)**: Best quality, tempo adjustment support
2. **pygame (fallback)**: Cross-platform compatibility

## Troubleshooting

### Common Issues

**"ffplay not found"**
```bash
sudo apt install ffmpeg  # Linux
brew install ffmpeg       # macOS
```

**"OpenCV error"**
```bash
pip install opencv-python
```

**Audio playback issues:**
- Ensure ffmpeg is installed for best audio support
- For MP4 files, audio extraction to WAV is automatic
- pygame fallback is available but with limited format support

**Terminal display issues:**
- Use a terminal with Unicode support for block characters
- Ensure terminal is large enough (minimum 40x20)
- Some terminals may not support all ANSI escape codes

### Performance Tips
- Use smaller FPS for better performance on slower systems
- Standard ASCII mode is faster than block character mode
- Larger terminal sizes require more processing power

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- ASCII art conversion inspired by classic terminal video players
- Thanks to the OpenCV and pygame communities
- Special thanks to ffmpeg for excellent multimedia support

## Changelog

### v1.0.0
- Initial release
- Basic ASCII video playback
- Audio synchronization
- Multiple character sets
- Terminal size adaptation
- Built-in demo video

---

**Made with ❤️ by [Bali0531-RC](https://github.com/Bali0531-RC)**