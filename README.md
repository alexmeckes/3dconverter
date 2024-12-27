# STL to 3MF Converter

A web-based tool to convert STL (stereolithography) files to 3MF (3D Manufacturing Format) format, making 3D models more compatible with modern 3D printing workflows.

## Features

- Drag-and-drop interface for easy file upload
- Support for binary STL files
- File size limit: 50MB
- Browser-based implementation (no installation required)
- Follows 3MF Core Specification v1.3.0
- Automatic download of converted files
- Clean, modern UI

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd stl-to-3mf-converter
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask development server:
```bash
cd src
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Either drag and drop your STL file onto the upload area or click "Choose File" to select it

4. Click "Convert to 3MF" to process the file

5. The converted 3MF file will automatically download when ready

## Technical Details

- The converter preserves the original model geometry while converting to the 3MF format
- Implements the 3MF Core Specification, including:
  - Proper XML namespace handling
  - Required OPC package structure
  - Correct content types and relationships
  - Valid 3MF model structure
- Uses efficient memory handling for large files
- Implements proper cleanup of temporary files

## Requirements

- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection not required for conversion

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 