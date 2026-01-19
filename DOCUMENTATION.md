# File Parser - Documentation Index

Complete guide to all documentation and resources.

## 📚 Documentation Overview

### For New Users

1. **[QUICKSTART.md](QUICKSTART.md)** ⚡ (2 min read)
   - 5-minute setup guide
   - Fastest way to get started
   - Essential steps only
   - **Start here if you want to get running quickly**

2. **[install.sh](install.sh)** 🤖 (Automated)
   - Interactive installation script
   - Guides you through setup
   - Configures environment automatically
   - **Run this for hassle-free installation**
   ```bash
   ./install.sh
   ```

### For Detailed Setup

3. **[SETUP.md](SETUP.md)** 📖 (15 min read)
   - Comprehensive installation guide
   - Step-by-step instructions
   - Configuration options explained
   - Security recommendations
   - **Read this for complete understanding**

### For Feature Information

4. **[README.md](README.md)** 📦 (10 min read)
   - Application overview
   - Feature descriptions
   - Architecture details
   - Usage examples
   - **Read this to understand what the app does**

### For Problem Solving

5. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** 🔧 (Reference)
   - Common errors and solutions
   - Debug commands
   - Performance tips
   - Quick diagnostic tools
   - **Consult this when you encounter issues**

---

## 🚀 Quick Navigation

### I want to...

**...install the application**
→ Run `./install.sh` or follow [QUICKSTART.md](QUICKSTART.md)

**...understand how it works**
→ Read [README.md](README.md)

**...fix an error**
→ Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**...configure advanced settings**
→ Read [SETUP.md](SETUP.md)

**...get API keys**
- Gemini: https://makersuite.google.com/app/apikey
- Claude: https://console.anthropic.com/

---

## 📋 File Structure

```
File-Parser/
├── README.md              # Main project overview
├── QUICKSTART.md         # 5-minute setup guide
├── SETUP.md              # Comprehensive setup guide
├── TROUBLESHOOTING.md    # Error solutions
├── DOCUMENTATION.md      # This file (index)
├── install.sh            # Automated installer
├── .env.example          # Environment template
├── requirements/         # Python dependencies
│   ├── base.txt         # Main app dependencies
│   └── analysis.txt     # AI service dependencies
├── app/                  # Flask main application
├── analysis_service/     # FastAPI AI service
├── config/               # Configuration files
├── frontend/             # HTML/CSS/JS
├── data/                 # Database storage
├── logs/                 # Application logs
├── uploads/              # Temp uploads
└── extracted/            # Extracted files
```

---

## 🎯 Installation Methods

### Method 1: Automated Script (Easiest)
```bash
./install.sh
```
- Interactive prompts
- Automatic dependency installation
- API key configuration
- **Recommended for beginners**

### Method 2: Quick Manual (5 minutes)
```bash
# Follow QUICKSTART.md
pip install -r requirements/base.txt
pip install -r requirements/analysis.txt
pip install google-genai
cp .env.example .env
# Edit .env with your API keys
mkdir -p data logs uploads extracted
python run_main.py &
python run_analysis.py &
```
- Fast setup
- Good for experienced users
- **Recommended for developers**

### Method 3: Comprehensive Manual (15 minutes)
- Follow [SETUP.md](SETUP.md)
- Includes virtual environment
- Security hardening
- Production configuration
- **Recommended for production deployments**

---

## 🔑 Configuration Files

### .env (Required)
Main configuration file containing:
- AI API keys (Gemini, Claude)
- Service URLs
- Feature flags
- Debug settings

**Setup:**
```bash
cp .env.example .env
nano .env  # Add your API keys
```

### config/settings.py
Advanced configuration:
- Database settings
- Upload limits
- Path configurations
- Security settings

---

## 🏃 Running the Application

### Start Services

**Terminal 1:**
```bash
python run_main.py
# Main app runs on http://localhost:5000
```

**Terminal 2:**
```bash
python run_analysis.py  
# Analysis service runs on http://localhost:8001
```

### Access Application
```
Main Interface: http://localhost:5000
API Health:     http://localhost:8001/health
AI Backends:    http://localhost:8001/api/analysis/backends
```

### Stop Services
Press `Ctrl+C` in each terminal

---

## 🧪 Testing Installation

### Quick Health Check
```bash
# Test main app
curl http://localhost:5000/ | head -5

# Test analysis service
curl http://localhost:8001/health

# Check AI backends
curl http://localhost:8001/api/analysis/backends
```

### Expected Output
```json
{
  "available": [
    {
      "name": "gemini",
      "display_name": "Google Gemini 2.0 Flash",
      "initialized": true
    },
    {
      "name": "claude", 
      "display_name": "Anthropic Claude 3.5 Sonnet",
      "initialized": true
    }
  ]
}
```

---

## ❓ Common Questions

### Do I need both API keys?
No, you need at least **one**. Both provide similar functionality.

### Which AI backend is better?
- **Gemini**: Faster, free tier available, good for most use cases
- **Claude**: Better reasoning, more detailed analysis, paid service

### Can I run without AI features?
Yes, set `ENABLE_AI_ANALYSIS=false` in `.env`. File extraction/browsing will still work.

### What Python version is required?
Python 3.8 or higher. Python 3.13 is tested and recommended.

### How much disk space do I need?
At least 5GB free space for operation. More if processing large archives.

### Is this production-ready?
The code is functional, but review [SETUP.md](SETUP.md) security section before deploying to production.

---

## 🔒 Security Notes

### Development vs Production

**Development (default):**
- Debug mode enabled
- Detailed error messages
- Auto-reload on code changes

**Production (recommended):**
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Configure HTTPS
- Restrict CORS origins
- Set up firewall rules

See [SETUP.md](SETUP.md#security-recommendations) for complete security guide.

---

## 📞 Getting Help

### Self-Service
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for your error
2. Search existing issues on GitHub
3. Review relevant documentation section
4. Check application logs

### Creating an Issue
Include:
- OS and Python version (`python3 --version`)
- Error message and full traceback
- Steps to reproduce
- Relevant log excerpts
- What you've tried already

### Useful Debug Info
```bash
# System info
python3 --version
pip list | grep -E "(flask|fastapi|google|anthropic)"
df -h
free -h

# Check services
curl http://localhost:5000/
curl http://localhost:8001/health

# View logs
tail -50 logs/app.log
```

---

## 📖 Learning Path

### Beginner Path
1. Run `./install.sh`
2. Skim [QUICKSTART.md](QUICKSTART.md)
3. Test with sample file
4. Read [README.md](README.md) features section
5. Keep [TROUBLESHOOTING.md](TROUBLESHOOTING.md) handy

### Advanced Path
1. Read [SETUP.md](SETUP.md) completely
2. Set up virtual environment
3. Review [README.md](README.md) architecture
4. Study `config/settings.py`
5. Explore API documentation
6. Configure for production

### Developer Path
1. Clone repository
2. Read all documentation
3. Review code structure
4. Study plugin system (`analysis_service/plugins/`)
5. Set up development environment
6. Run tests (if available)
7. Create custom plugins

---

## 🎓 Additional Resources

### External Links
- **Gemini API Docs**: https://ai.google.dev/docs
- **Claude API Docs**: https://docs.anthropic.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

### Related Files
- `.env.example` - Configuration template
- `requirements/` - Dependency specifications
- `config/` - Advanced settings

---

## 📝 Document Maintenance

**Last Updated**: January 16, 2026

**Version**: 1.0.0

**Maintained By**: Project maintainers

To update documentation:
1. Edit relevant `.md` file
2. Update "Last Updated" date
3. Increment version if major changes
4. Update this index if adding new docs

---

## ✅ Checklist for New Users

- [ ] Read QUICKSTART.md
- [ ] Run ./install.sh OR follow manual setup
- [ ] Obtain at least one API key
- [ ] Configure .env file
- [ ] Create required directories
- [ ] Start both services
- [ ] Test with http://localhost:5000
- [ ] Verify AI backends initialized
- [ ] Upload test file
- [ ] Bookmark TROUBLESHOOTING.md

---

**Ready to get started?** → [QUICKSTART.md](QUICKSTART.md)

**Need detailed setup?** → [SETUP.md](SETUP.md)

**Having issues?** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Want to learn more?** → [README.md](README.md)

---

*Documentation complete. Happy analyzing! 📦✨*
