# File Extractor Web Application

A modern web application for uploading, extracting, and browsing archive files with real-time progress tracking.

## Features

### Core Functionality
- **File Upload**: Drag & drop or browse to upload archive files
- **Multiple Format Support**: ZIP, TAR, TAR.GZ, TGZ, BZ2, XZ, and more
- **Real-time Progress Tracking**:
  - Upload progress
  - Extraction progress with percentage
  - Processing status updates
  - File-by-file extraction tracking

### File Management
- **Summary Dashboard**: View counts and sizes at a glance
  - Total files count
  - Total directories count
  - Total size in human-readable format

- **Separate File & Directory Views**:
  - Click on "Files" card to see all extracted files
  - Click on "Directories" card to see all directories
  - Each view shows name, path, and size information

- **File Preview**:
  - Click "View" to read text files directly in browser
  - Supports files up to 5MB for preview
  - Syntax highlighting with monospace font
  - Download option for all files

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Application**:
```bash
python server.py
```

3. **Access the Web Interface**:
Open your browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Uploading Files

1. **Drag & Drop**: Drag an archive file onto the upload area
2. **Browse**: Click "Select File" to choose a file from your computer
3. **Upload**: Click "Upload & Extract" to begin processing

### Viewing Progress

The application shows real-time progress updates:
- **0-10%**: Uploading file
- **10-90%**: Extracting files (shows individual file progress)
- **90-95%**: Analyzing extracted files
- **95-100%**: Finalizing and completing

### Browsing Extracted Files

1. **View Summary**: After extraction, see total files, directories, and size
2. **Browse Files**: Click the "Files" card to see all extracted files
3. **Browse Directories**: Click the "Directories" card to see all folders
4. **View File Content**: Click "View" on any text file to preview it
5. **Download Files**: Click "Download" to save individual files

### File Viewer

- Supports text files up to 5MB
- Shows binary file warning for non-text files
- Displays file size information
- Scroll through large files
- Close viewer to return to file list

## Project Structure

```
file-extractor-app/
├── server.py              # Flask backend server
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend interface
├── uploads/              # Temporary upload storage (auto-created)
└── extracted/            # Extracted files storage (auto-created)
```

## API Endpoints

### POST /upload
Upload an archive file for extraction
- **Body**: multipart/form-data with 'file' field
- **Response**: `{"success": true, "job_id": "...", "filename": "..."}`

### GET /progress/<job_id>
Get extraction progress for a job
- **Response**: `{"status": "extracting", "progress": 45, "message": "..."}`

### GET /browse/<job_id>
Get list of extracted files and directories
- **Response**: JSON with files, directories, and size information

### GET /read/<job_id>/<file_path>
Read content of an extracted file
- **Response**: `{"success": true, "content": "...", "size": 1234}`

### GET /download/<job_id>/<file_path>
Download an extracted file
- **Response**: File download

## Configuration

You can modify these settings in `server.py`:

```python
UPLOAD_FOLDER = 'uploads'           # Upload directory
EXTRACT_FOLDER = 'extracted'        # Extraction directory
MAX_FILE_SIZE = 500 * 1024 * 1024  # Max upload: 500MB
ALLOWED_EXTENSIONS = {...}          # Supported formats
```

## Security Features

- File path validation to prevent directory traversal
- Secure filename handling
- File size limits
- Binary file detection
- CORS protection

## Supported Archive Formats

- ZIP (.zip)
- TAR (.tar)
- GZIP (.gz, .tar.gz, .tgz)
- BZIP2 (.bz2, .tar.bz2)
- XZ (.xz, .tar.xz)

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

## Troubleshooting

### Upload Fails
- Check file size (must be under 500MB)
- Verify file format is supported
- Ensure sufficient disk space

### Extraction Error
- Archive file may be corrupted
- Check server logs for details
- Try re-uploading the file

### File Preview Not Working
- File must be text-based
- File must be under 5MB
- Binary files cannot be previewed

## Future Enhancements

- Support for RAR and 7Z archives
- Batch file operations
- Search within extracted files
- Archive creation functionality
- User authentication
- Cloud storage integration

## License

MIT License - feel free to use and modify as needed.

## Author

Created with Flask and vanilla JavaScript for simplicity and performance.
