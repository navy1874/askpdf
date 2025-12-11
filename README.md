# AskPDF

A cross-platform desktop application for handling PDF, text, image files, and more. Built with Electron for Windows, Linux, and macOS.

## Features

- 📄 **PDF Viewer**: View PDF documents with multi-page support
- 📝 **Text File Reader**: Open and read text files
- 🖼️ **Image Viewer**: Display images (JPG, PNG, GIF, BMP)
- 🖥️ **Cross-Platform**: Works on Windows, Linux, and macOS
- 🎨 **Modern UI**: Clean and intuitive user interface

## Supported File Formats

- **PDF**: `.pdf`
- **Text**: `.txt`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

## Installation

### Prerequisites

- Node.js 16 or higher
- npm (comes with Node.js)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/navy1874/askpdf.git
cd askpdf
```

2. Install dependencies:
```bash
npm install
```

## Usage

### Development Mode

Run the application in development mode:

```bash
npm start
```

### Building for Production

Build for all platforms:
```bash
npm run build
```

Build for specific platforms:

**Windows:**
```bash
npm run build:win
```

**macOS:**
```bash
npm run build:mac
```

**Linux:**
```bash
npm run build:linux
```

The built applications will be available in the `dist` directory.

## Platform-Specific Notes

### Windows
- Builds as an NSIS installer (`.exe`)
- Requires Windows 7 or later

### macOS
- Builds as a DMG file (`.dmg`)
- Requires macOS 10.13 (High Sierra) or later
- Note: Building for macOS requires a macOS machine

### Linux
- Builds as AppImage and DEB packages
- AppImage is portable and works on most distributions
- DEB package for Debian-based systems (Ubuntu, Mint, etc.)

## Project Structure

```
askpdf/
├── main.js           # Electron main process
├── preload.js        # Preload script for secure IPC
├── renderer.js       # Renderer process logic
├── index.html        # Application UI
├── styles.css        # Styling
├── package.json      # Project configuration
└── README.md         # Documentation
```

## How It Works

1. **Main Process** (`main.js`): Manages the application lifecycle, creates windows, and handles file system operations
2. **Preload Script** (`preload.js`): Provides secure communication between main and renderer processes
3. **Renderer Process** (`renderer.js`): Handles UI interactions and file content display
4. **UI** (`index.html` + `styles.css`): Modern, responsive interface for file viewing

## Development

### Technologies Used

- **Electron**: Cross-platform desktop framework
- **Browser PDF Viewer**: Built-in PDF rendering via iframe
- **Node.js**: File system and backend operations

### Security

The application uses Electron's security best practices:
- Context isolation enabled
- Node integration disabled in renderer
- Secure IPC communication via preload scripts

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
