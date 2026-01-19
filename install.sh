#!/bin/bash

# File Parser - Automated Installation Script
# This script automates the setup process for new users

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print header
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     File Parser - Automated Installation Script       ║"
echo "║              AI-Powered Test Analysis                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check pip
print_info "Checking pip..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

# Ask about virtual environment
echo ""
read -p "Do you want to create a virtual environment? (recommended) [y/N]: " CREATE_VENV
if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
    
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
fi

# Create directories
print_info "Creating required directories..."
mkdir -p data logs uploads extracted
print_success "Directories created: data, logs, uploads, extracted"

# Install base dependencies
echo ""
print_info "Installing base dependencies (Flask app)..."
pip3 install -r requirements/base.txt
if [ $? -eq 0 ]; then
    print_success "Base dependencies installed"
else
    print_warning "Some base dependencies may have failed. Continuing..."
fi

# Install analysis dependencies
echo ""
print_info "Installing analysis service dependencies..."
pip3 install -r requirements/analysis.txt
if [ $? -eq 0 ]; then
    print_success "Analysis dependencies installed"
else
    print_warning "Some analysis dependencies may have failed. Continuing..."
fi

# Install Google GenAI
echo ""
print_info "Installing Google GenAI SDK..."
pip3 install google-genai
if [ $? -eq 0 ]; then
    print_success "Google GenAI SDK installed"
else
    print_warning "Google GenAI SDK installation failed. Gemini plugin may not work."
fi

# Upgrade SQLAlchemy
print_info "Upgrading SQLAlchemy for compatibility..."
pip3 install --upgrade SQLAlchemy
print_success "SQLAlchemy upgraded"

# Optional: Install MCP support
echo ""
read -p "Do you want to install MCP (Model Context Protocol) support? [y/N]: " INSTALL_MCP
if [[ $INSTALL_MCP =~ ^[Yy]$ ]]; then
    print_info "Installing aiohttp for MCP support..."
    pip3 install aiohttp
    print_success "MCP support installed"
fi

# Configure environment
echo ""
if [ -f .env ]; then
    print_warning ".env file already exists"
    read -p "Do you want to overwrite it? [y/N]: " OVERWRITE_ENV
    if [[ ! $OVERWRITE_ENV =~ ^[Yy]$ ]]; then
        print_info "Keeping existing .env file"
    else
        cp .env.example .env
        print_success ".env file created from template"
    fi
else
    print_info "Creating .env configuration file..."
    cp .env.example .env
    print_success ".env file created from template"
fi

# Ask for API keys
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║              API Key Configuration                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
print_info "You need at least ONE AI API key for the application to work."
echo ""
echo "Available options:"
echo "  1. Google Gemini (Free tier available)"
echo "     Get key from: https://makersuite.google.com/app/apikey"
echo ""
echo "  2. Anthropic Claude (Paid service)"
echo "     Get key from: https://console.anthropic.com/"
echo ""

read -p "Do you have a Gemini API key to configure now? [y/N]: " HAS_GEMINI
if [[ $HAS_GEMINI =~ ^[Yy]$ ]]; then
    read -p "Enter your Gemini API key: " GEMINI_KEY
    if [ ! -z "$GEMINI_KEY" ]; then
        # Update .env file with Gemini key
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_KEY/" .env
        else
            # Linux
            sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_KEY/" .env
        fi
        print_success "Gemini API key configured"
    fi
fi

echo ""
read -p "Do you have a Claude API key to configure now? [y/N]: " HAS_CLAUDE
if [[ $HAS_CLAUDE =~ ^[Yy]$ ]]; then
    read -p "Enter your Claude API key: " CLAUDE_KEY
    if [ ! -z "$CLAUDE_KEY" ]; then
        # Update .env file with Claude key
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/CLAUDE_API_KEY=.*/CLAUDE_API_KEY=$CLAUDE_KEY/" .env
        else
            # Linux
            sed -i "s/CLAUDE_API_KEY=.*/CLAUDE_API_KEY=$CLAUDE_KEY/" .env
        fi
        print_success "Claude API key configured"
    fi
fi

# Final summary
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║              Installation Complete!                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
print_success "File Parser has been successfully installed!"
echo ""
echo "Next steps:"
echo ""
echo "  1. If you haven't configured API keys yet, edit .env file:"
echo "     nano .env"
echo ""
echo "  2. Start the services in two separate terminals:"
echo ""
echo "     Terminal 1 - Main Flask App:"
if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
echo "       source venv/bin/activate"
fi
echo "       python run_main.py"
echo ""
echo "     Terminal 2 - Analysis Service:"
if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
echo "       source venv/bin/activate"
fi
echo "       python run_analysis.py"
echo ""
echo "  3. Open your browser:"
echo "     http://localhost:5000"
echo ""
echo "For detailed documentation, see:"
echo "  - QUICKSTART.md - Quick start guide"
echo "  - SETUP.md      - Comprehensive setup documentation"
echo "  - README.md     - Feature overview"
echo ""
print_success "Happy analyzing! 📦✨"
echo ""
