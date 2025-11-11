# Quick Start Guide

## Installation & Running

### Option 1: Using the startup script
```bash
cd /home/shrepati/AI/file-extractor-app
./start.sh
```

### Option 2: Manual start
```bash
cd /home/shrepati/AI/file-extractor-app
python3 server.py
```

## Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

## How to Use

### 1. Upload an Archive File
- **Drag & Drop**: Drag your ZIP, TAR, or compressed file onto the upload area
- **Or Browse**: Click "Select File" to choose from your computer
- Click "Upload & Extract" button

### 2. Watch the Progress
The app shows real-time updates:
- ✅ File uploaded: 10%
- ✅ File is processing: 10-90% (with detailed file-by-file progress)
- ✅ Extracting: Shows percentage and current file being extracted
- ✅ Analyzing: 95%
- ✅ Working: Shows what it's currently doing
- ✅ Completed: 100%

### 3. View Summary
After extraction completes, you'll see three cards:
- **Files Card**: Shows total number of files extracted
- **Directories Card**: Shows total number of directories
- **Size Card**: Shows total size of all extracted content

### 4. Browse Files
Click on the **Files** card to see:
- Complete list of all extracted files
- File names, paths, and sizes
- "View" button - Preview text files in browser
- "Download" button - Download individual files

### 5. Browse Directories
Click on the **Directories** card to see:
- Complete list of all directories
- Directory names, paths, and sizes

### 6. Read Files
In the Files view:
1. Click "View" button on any file
2. Text files will open in a code viewer
3. Binary files will show a warning
4. Large files (>5MB) will show size warning
5. Click "Close" to go back to the file list

## Progress Indicators

The application shows different status messages:

| Progress | Status | Description |
|----------|--------|-------------|
| 0-5% | "Uploading file..." | File is being uploaded to server |
| 5-10% | "File uploaded, starting extraction..." | Upload complete, preparing extraction |
| 10-90% | "Extracting: filename.txt (X/Y)" | Currently extracting files with count |
| 90-95% | "Analyzing extracted files..." | Scanning directory structure |
| 95-100% | "Extraction completed successfully!" | All done! |

## Supported Formats

- ✅ ZIP (.zip)
- ✅ TAR (.tar)
- ✅ GZIP (.tar.gz, .tgz, .gz)
- ✅ BZIP2 (.tar.bz2, .bz2)
- ✅ XZ (.tar.xz, .xz)

## Tips

1. **Maximum file size**: 500MB
2. **File preview limit**: 5MB (larger files can be downloaded)
3. **Text files only**: Preview works for text-based files
4. **Progress updates**: Real-time updates every 300ms
5. **Multiple uploads**: Each upload gets a unique job ID

## Example Workflow

```
1. Visit http://localhost:5000
2. Drag your archive.zip file onto the page
3. Click "Upload & Extract"
4. Watch progress: "Extracting: file1.txt (1/100) - 15%"
5. See summary: "100 Files, 5 Directories, 2.5 MB"
6. Click "Files" card
7. Click "View" on README.md
8. Read the file content
9. Click "Download" to save locally
10. Click "Close" to return
```

## Troubleshooting

**Server won't start?**
- Make sure Flask is installed: `pip install -r requirements.txt`
- Check if port 5000 is available

**Upload fails?**
- Check file size (must be < 500MB)
- Verify file format is supported

**Can't preview file?**
- Only text files can be previewed
- Binary files must be downloaded
- Files > 5MB must be downloaded

**Progress stuck?**
- Wait a moment, extraction takes time
- Check browser console for errors
- Refresh the page and try again

## Project Structure

```
file-extractor-app/
├── server.py           # Backend Flask server
├── templates/
│   └── index.html      # Frontend web interface
├── uploads/            # Temporary upload storage (auto-created)
├── extracted/          # Extracted files (auto-created)
├── requirements.txt    # Python dependencies
├── start.sh           # Quick start script
├── README.md          # Full documentation
└── QUICKSTART.md      # This guide
```

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

---

**Ready to extract files!** 📦🚀
