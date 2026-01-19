# Troubleshooting Guide

Quick solutions to common File Parser issues.

## Installation Issues

### Error: "ModuleNotFoundError"

**Missing module during startup**

```bash
ModuleNotFoundError: No module named 'xyz'
```

**Solution:**
```bash
pip install <module-name>

# Or reinstall all dependencies
pip install -r requirements/base.txt
pip install -r requirements/analysis.txt
```

### Error: "cannot import name 'genai' from 'google'"

**Gemini plugin fails to load**

**Solution:**
```bash
pip install google-genai
# Then restart analysis service
```

### Error: "libxml2 development packages"

**lxml installation fails**

**Solution (Linux):**
```bash
# Fedora/RHEL
sudo dnf install libxml2-devel libxslt-devel

# Ubuntu/Debian  
sudo apt-get install libxml2-dev libxslt-dev

# Then reinstall
pip install lxml
```

### Error: SQLAlchemy compatibility

```
AssertionError: Class directly inherits TypingOnly...
```

**Solution:**
```bash
pip install --upgrade SQLAlchemy
```

---

## Runtime Issues

### Port Already in Use

```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find process using port
sudo lsof -i :5000
sudo lsof -i :8001

# Kill the process
kill -9 <PID>

# Or change ports in .env
```

### Database Errors

**Database locked or corrupted**

**Solution:**
```bash
# Backup if needed
cp data/app.db data/app.db.backup

# Remove and recreate
rm data/app.db
python run_main.py  # Will auto-create
```

### Permission Denied

**Cannot write to directories**

**Solution:**
```bash
chmod -R 755 uploads extracted data logs
```

---

## AI Backend Issues

### "Error discovering RHOSO test folders"

**Discovery endpoint returns 404 or path errors**

**Cause:**
The frontend had hardcoded paths that don't match your system.

**Solution:**
This has been fixed in the latest version. If you still see this error:

```bash
# Verify the fix is applied
grep "extracted/\${currentJobId}" frontend/static/js/main.js

# Should see 4 lines like:
#   const extractPath = `extracted/${currentJobId}`;

# If you see /home/atiwary paths, update the file manually
# or pull the latest code
```

### "Backend not initialized"

**AI analysis fails**

**Checklist:**
1. Check API key is in `.env`
2. Verify key is valid (not expired)
3. Check analysis service is running
4. Restart analysis service

**Solution:**
```bash
# Verify configuration
cat .env | grep API_KEY

# Restart analysis service
# Ctrl+C in terminal running it
python run_analysis.py
```

### "Analysis service not reachable"

**Main app can't connect to analysis service**

**Solution:**
```bash
# Check if running
curl http://localhost:8001/health

# If not, start it
python run_analysis.py

# Check firewall (should allow localhost)
```

### Gemini Plugin Not Available

**Error in logs:** `Gemini plugin not available`

**Solution:**
```bash
# Install new SDK
pip install google-genai

# Restart analysis service
```

### Claude API Errors

**Rate limits or authentication errors**

**Checklist:**
1. Verify API key format starts with `sk-ant-`
2. Check you have credits remaining
3. Verify no rate limiting

---

## Application Behavior

### Upload Fails

**File won't upload**

**Checklist:**
- File size under 2GB
- File format supported (ZIP, TAR, etc.)
- Sufficient disk space
- `uploads/` directory writable

### Extraction Hangs

**Progress bar stuck**

**Solution:**
```bash
# Check main app logs for errors
# Look in terminal where run_main.py is running

# Or check log file if configured
tail -f logs/app.log
```

### No Test Results Showing

**AI analysis tab missing**

**Requirements:**
- Archive must contain `rhoso*` folders
- Folders must have `tempest_results.html` or `.xml`
- Analysis service must be running

### File Preview Empty

**Can't view file contents**

**Possible causes:**
- File is binary (not text)
- File larger than 5MB
- File path contains special characters

---

## Network & Connectivity

### Cannot Access http://localhost:5000

**Browser can't connect**

**Checklist:**
1. Main app is running (check terminal)
2. No firewall blocking port 5000
3. Try http://127.0.0.1:5000
4. Check for port conflicts

### CORS Errors in Browser Console

**Cross-origin request blocked**

**Solution:**
Edit `.env`:
```bash
CORS_ORIGINS=*  # For development only
# For production, use specific domain
```

Restart main app.

---

## Performance Issues

### Slow Extraction

**Large files take too long**

**Expected times:**
- 100MB: ~30 seconds
- 500MB: ~2 minutes  
- 2GB: ~5-10 minutes

**Tips:**
- Extract to SSD instead of HDD
- Close other applications
- Check CPU/memory usage

### High Memory Usage

**Application uses lots of RAM**

**Solutions:**
- Reduce file size
- Extract smaller archives
- Restart services periodically
- Check for memory leaks in logs

---

## Debug Mode

### Enable Detailed Logging

Edit `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

Restart both services.

### Check Logs

```bash
# Main app terminal output
# Analysis service terminal output

# Or log files if configured
tail -f logs/app.log
tail -f logs/analysis.log
```

---

## Clean Reinstall

If all else fails:

```bash
# 1. Stop all services (Ctrl+C)

# 2. Clean up
rm -rf venv data/app.db uploads/* extracted/*

# 3. Reinstall
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt
pip install -r requirements/analysis.txt
pip install google-genai

# 4. Reconfigure .env
nano .env

# 5. Restart
python run_main.py     # Terminal 1
python run_analysis.py # Terminal 2
```

---

## Still Having Issues?

1. **Check existing issues** in repository
2. **Search logs** for error messages
3. **Create new issue** with:
   - OS and Python version
   - Full error message
   - Steps to reproduce
   - Relevant logs

---

## Quick Diagnostic Commands

```bash
# Check Python version
python3 --version

# Check installed packages
pip list | grep -E "(flask|fastapi|google-genai|anthropic)"

# Test API connectivity
curl http://localhost:5000/
curl http://localhost:8001/health
curl http://localhost:8001/api/analysis/backends

# Check ports in use
sudo netstat -tulpn | grep -E "(5000|8001)"

# Check disk space
df -h

# Check memory
free -h

# Check running processes
ps aux | grep python
```

---

## Environment Variables Reference

Key settings in `.env`:

```bash
# Required for AI analysis
GEMINI_API_KEY=your-key-here
CLAUDE_API_KEY=your-key-here

# Service URLs
ANALYSIS_SERVICE_URL=http://localhost:8001

# Features
ENABLE_AI_ANALYSIS=true
ENABLE_SEARCH=true

# Debug
DEBUG=True
LOG_LEVEL=DEBUG
```

---

For more help, see:
- [SETUP.md](SETUP.md) - Complete setup guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start
- [README.md](README.md) - Feature documentation
