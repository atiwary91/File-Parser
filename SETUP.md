# File Parser - Complete Setup Guide

This guide will walk you through setting up the File Parser application with AI-powered test analysis on your machine.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

### Required Software
- **Python 3.8 or higher** (Python 3.13 recommended)
- **pip** package manager
- **git** (if cloning from repository)

### Required API Keys
At least ONE of the following AI API keys:
- **Google Gemini API Key** - Get from: https://makersuite.google.com/app/apikey
- **Anthropic Claude API Key** - Get from: https://console.anthropic.com/

### System Requirements
- **Disk Space**: At least 5GB free space
- **RAM**: Minimum 4GB recommended
- **OS**: Linux, macOS, or Windows

---

## Installation Steps

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd File-Parser

# Or if you downloaded a zip file
unzip File-Parser.zip
cd File-Parser
```

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment keeps dependencies isolated:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal after activation.

### Step 3: Install System Dependencies (Linux Only)

If you're on **Fedora/RHEL/CentOS**:
```bash
sudo dnf install libxml2-devel libxslt-devel
```

If you're on **Ubuntu/Debian**:
```bash
sudo apt-get install libxml2-dev libxslt-dev
```

If you're on **macOS** or **Windows**, you can skip this step.

### Step 4: Install Python Dependencies

Install all required Python packages:

```bash
# Install base dependencies (Flask app)
pip install -r requirements/base.txt

# Install analysis service dependencies (AI features)
pip install -r requirements/analysis.txt

# Install the new Google GenAI SDK (required for Gemini)
pip install google-genai

# Optional: Install MCP support
pip install aiohttp
```

**Note**: If you encounter errors with `lxml`, the system dependencies from Step 3 should resolve them.

### Step 5: Create Required Directories

```bash
mkdir -p data logs uploads extracted
```

These directories are used for:
- `data/` - SQLite database storage
- `logs/` - Application logs
- `uploads/` - Temporary file uploads
- `extracted/` - Extracted archive contents

---

## Configuration

### Step 1: Copy Environment Template

```bash
cp .env.example .env
```

### Step 2: Edit Configuration File

Open the `.env` file in your favorite text editor:

```bash
nano .env
# or
vim .env
# or
code .env  # VS Code
```

### Step 3: Add Your API Keys

**IMPORTANT**: Add at least ONE API key for AI analysis to work.

#### Option A: Using Google Gemini (Recommended - Free Tier Available)

```bash
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### Option B: Using Anthropic Claude

```bash
# Get your API key from: https://console.anthropic.com/
CLAUDE_API_KEY=sk-ant-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### Option C: Using Both (Recommended)

```bash
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
CLAUDE_API_KEY=sk-ant-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 4: Optional Configuration

You can customize these settings in `.env`:

```bash
# Flask Configuration
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-random-secret-key-here

# File Upload Limits
MAX_UPLOAD_SIZE=2147483648  # 2GB in bytes

# Feature Flags
ENABLE_AI_ANALYSIS=true
ENABLE_SEARCH=true
ENABLE_TREE_VIEW=true

# Logging
LOG_LEVEL=INFO
```

---

## Running the Application

The application consists of **two services** that need to run simultaneously:

### Method 1: Using Two Terminal Windows (Recommended for Development)

**Terminal 1 - Main Flask Application:**
```bash
cd /path/to/File-Parser
source venv/bin/activate  # If using virtual environment
python run_main.py
```

You should see:
```
======================================================================
File Extractor - AI-Powered Test Analysis Platform
======================================================================
Environment: development
Starting server on http://localhost:5000
======================================================================
```

**Terminal 2 - Analysis Service:**
```bash
cd /path/to/File-Parser
source venv/bin/activate  # If using virtual environment
python run_analysis.py
```

You should see:
```
======================================================================
File Extractor - Analysis Service
AI-Powered Test Failure Analysis
======================================================================
Gemini API Key: ✓ Configured
Claude API Key: ✓ Configured
Starting analysis service on http://localhost:8001
======================================================================
INFO: Gemini plugin initialized successfully
INFO: Claude plugin initialized successfully
INFO: Initialized plugins: ['gemini', 'claude']
```

### Method 2: Using Background Processes (Linux/macOS)

```bash
# Start both services in the background
python run_main.py > logs/main.log 2>&1 &
python run_analysis.py > logs/analysis.log 2>&1 &

# View logs in real-time
tail -f logs/main.log
tail -f logs/analysis.log
```

### Method 3: Using Screen/Tmux (Linux/macOS)

```bash
# Using screen
screen -dmS file-parser-main python run_main.py
screen -dmS file-parser-analysis python run_analysis.py

# List screens
screen -ls

# Attach to a screen
screen -r file-parser-main
```

---

## Verification

### Step 1: Check Main Application

Open your browser and navigate to:
```
http://localhost:5000
```

You should see the File Parser interface with:
- Upload area for drag & drop
- File type indicators (ZIP, TAR, etc.)
- Clean, modern UI

### Step 2: Check Analysis Service

Open a new browser tab and navigate to:
```
http://localhost:8001
```

You should see a JSON response:
```json
{
  "service": "File Extractor Analysis Service",
  "version": "1.0.0",
  "status": "running"
}
```

### Step 3: Verify AI Backends

Check available AI backends:
```bash
curl http://localhost:8001/api/analysis/backends | python3 -m json.tool
```

Expected output:
```json
{
  "available": [
    {
      "name": "gemini",
      "display_name": "Google Gemini 2.0 Flash",
      "supports_streaming": true,
      "initialized": true
    },
    {
      "name": "claude",
      "display_name": "Anthropic Claude 3.5 Sonnet",
      "supports_streaming": true,
      "initialized": true
    }
  ],
  "total": 2
}
```

### Step 4: Test File Upload

1. Go to http://localhost:5000
2. Drag and drop a small ZIP file (or use the file picker)
3. Click "Upload & Extract"
4. You should see:
   - Progress bar updating
   - File extraction progress
   - Summary of extracted files

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'dotenv'"

**Solution:**
```bash
pip install python-dotenv
```

### Issue 2: "ModuleNotFoundError: No module named 'uvicorn'"

**Solution:**
```bash
pip install uvicorn
```

### Issue 3: "Error: Please make sure the libxml2 and libxslt development packages are installed"

**Solution (Linux):**
```bash
# Fedora/RHEL/CentOS
sudo dnf install libxml2-devel libxslt-devel

# Ubuntu/Debian
sudo apt-get install libxml2-dev libxslt-dev

# Then reinstall
pip install lxml
```

### Issue 4: "Gemini plugin not available: cannot import name 'genai'"

**Solution:**
```bash
pip install google-genai
```

Then restart the analysis service.

### Issue 5: SQLAlchemy Compatibility Error

**Error:**
```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly...
```

**Solution:**
```bash
pip install --upgrade SQLAlchemy
```

### Issue 6: Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Check what's using port 5000 or 8001
sudo lsof -i :5000
sudo lsof -i :8001

# Kill the process
kill -9 <PID>

# Or use different ports by editing .env:
# FLASK_PORT=5001
# ANALYSIS_PORT=8002
```

### Issue 7: Analysis Service Connection Failed

**Symptoms:**
- Main app works but AI analysis shows "Service unavailable"

**Solution:**
1. Check if analysis service is running:
   ```bash
   curl http://localhost:8001/health
   ```

2. If not running, start it:
   ```bash
   python run_analysis.py
   ```

3. Check firewall settings (should allow localhost connections)

### Issue 8: Database Errors

**Solution:**
```bash
# Remove old database and let it recreate
rm data/app.db

# Restart the main application
python run_main.py
```

### Issue 9: Permission Denied Errors

**Solution:**
```bash
# Ensure directories are writable
chmod -R 755 uploads extracted data logs

# If using virtual environment, ensure it's activated
source venv/bin/activate
```

### Issue 10: AI Analysis Returns Errors

**Check:**
1. Verify API keys are correct in `.env`
2. Check API key has not expired
3. Verify you have API quota/credits remaining
4. Check analysis service logs:
   ```bash
   tail -f logs/analysis.log
   ```

---

## Getting Help

### Check Logs

Logs are your best friend for debugging:

```bash
# Application logs
tail -f logs/app.log

# Analysis service logs (if redirected)
tail -f logs/analysis.log

# Or check terminal output where services are running
```

### Enable Debug Mode

In `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

Then restart both services.

### Common Log Locations

- Main app: Terminal output or `logs/app.log`
- Analysis service: Terminal output or `logs/analysis.log`
- Database: `data/app.db` (SQLite file)

---

## Next Steps

Once everything is running:

1. **Upload a Test File**
   - Try a small ZIP or TAR file first
   - Verify extraction works correctly

2. **Test AI Analysis** (if you have RHOSO test results)
   - Upload an archive containing `rhoso*` folders
   - Navigate to "Test Results" tab
   - Select an AI backend and click "Analyze with AI"

3. **Explore Features**
   - Search functionality
   - Tree view navigation
   - File preview
   - Download individual files

4. **Read the Documentation**
   - See `README.md` for feature details
   - Check `CONTRIBUTING.md` for development guidelines (if available)

---

## Security Recommendations

### For Production Deployment:

1. **Change Secret Key**
   ```bash
   # Generate a random secret key
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Add to `.env`:
   ```bash
   SECRET_KEY=<generated-key-here>
   ```

2. **Disable Debug Mode**
   ```bash
   DEBUG=False
   FLASK_ENV=production
   ```

3. **Use HTTPS**
   - Set up reverse proxy (nginx/Apache)
   - Obtain SSL certificate (Let's Encrypt)

4. **Restrict CORS**
   ```bash
   CORS_ORIGINS=https://yourdomain.com
   ```

5. **Set Up Proper Logging**
   ```bash
   LOG_LEVEL=WARNING
   LOG_FILE=logs/production.log
   ```

6. **Protect API Keys**
   - Never commit `.env` to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

7. **Configure Firewall**
   ```bash
   # Only allow localhost access to analysis service
   sudo firewall-cmd --add-port=5000/tcp
   # DO NOT expose port 8001 externally
   ```

---

## Quick Reference

### Start Services
```bash
python run_main.py          # Terminal 1
python run_analysis.py      # Terminal 2
```

### Stop Services
```
Ctrl+C in each terminal
```

### Access Application
```
Main App: http://localhost:5000
Analysis API: http://localhost:8001
```

### Check Status
```bash
curl http://localhost:5000/         # Main app
curl http://localhost:8001/health   # Analysis service
```

### View Logs
```bash
tail -f logs/app.log
tail -f logs/analysis.log
```

---

## Support

For issues, bugs, or feature requests:
- Check existing issues in the repository
- Create a new issue with:
  - Your OS and Python version
  - Error messages and logs
  - Steps to reproduce

---

**Congratulations!** 🎉 Your File Parser application should now be fully set up and running!

Happy analyzing! 📦✨
