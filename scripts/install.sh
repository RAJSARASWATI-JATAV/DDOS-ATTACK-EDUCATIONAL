#!/bin/bash
# DDOS Attack Educational Toolkit - Installation Script
# Created By: Rajsaraswati Jatav
# GitHub: https://github.com/RAJSARASWATI-JATAV

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "============================================"
echo "  DDOS ATTACK EDUCATIONAL TOOLKIT"
echo "  Created By: Rajsaraswati Jatav"
echo "  GitHub: @RAJSARASWATI-JATAV"
echo "============================================"
echo -e "${NC}"

echo -e "${YELLOW}⚠️  FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️${NC}\n"

# Check if Python is installed
echo -e "${BLUE}[INFO]${NC} Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d" " -f2)
    echo -e "${GREEN}[OK]${NC} Python ${PYTHON_VERSION} found"
else
    echo -e "${RED}[ERROR]${NC} Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
echo -e "${BLUE}[INFO]${NC} Checking pip installation..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} pip3 found"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}[OK]${NC} pip found"
    PIP_CMD="pip"
else
    echo -e "${RED}[ERROR]${NC} pip not found. Please install pip."
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}[INFO]${NC} Creating virtual environment..."
if python3 -m venv venv; then
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
else
    echo -e "${YELLOW}[WARNING]${NC} Could not create virtual environment, continuing with system Python"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${BLUE}[INFO]${NC} Activating virtual environment..."
    source venv/bin/activate
    echo -e "${GREEN}[OK]${NC} Virtual environment activated"
fi

# Upgrade pip
echo -e "${BLUE}[INFO]${NC} Upgrading pip..."
$PIP_CMD install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}[OK]${NC} pip upgraded"

# Install requirements
echo -e "${BLUE}[INFO]${NC} Installing Python dependencies..."
if $PIP_CMD install -r requirements.txt; then
    echo -e "${GREEN}[OK]${NC} Dependencies installed successfully"
else
    echo -e "${RED}[ERROR]${NC} Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo -e "${BLUE}[INFO]${NC} Creating directories..."
mkdir -p logs
mkdir -p assets/sounds
mkdir -p assets/visuals
echo -e "${GREEN}[OK]${NC} Directories created"

# Set permissions
echo -e "${BLUE}[INFO]${NC} Setting permissions..."
chmod +x main.py
chmod +x scripts/*.py
echo -e "${GREEN}[OK]${NC} Permissions set"

# Test installation
echo -e "${BLUE}[INFO]${NC} Testing installation..."
if python3 -c "import main; print('Import successful')"; then
    echo -e "${GREEN}[OK]${NC} Installation test passed"
else
    echo -e "${RED}[ERROR]${NC} Installation test failed"
    exit 1
fi

# Installation complete
echo -e "\n${GREEN}🎉 INSTALLATION COMPLETED SUCCESSFULLY! 🎉${NC}\n"

echo -e "${BLUE}📚 QUICK START GUIDE:${NC}"
echo -e "1. Run interactive mode: ${YELLOW}python3 main.py --interactive${NC}"
echo -e "2. Get help: ${YELLOW}python3 main.py --help${NC}"
echo -e "3. Example usage: ${YELLOW}python3 main.py --target localhost --method http --threads 100${NC}\n"

echo -e "${YELLOW}⚠️  IMPORTANT REMINDERS:${NC}"
echo -e "• Only test systems you own or have explicit permission to test"
echo -e "• This tool is for educational and ethical testing purposes only"
echo -e "• Always follow responsible disclosure practices"
echo -e "• Respect applicable laws and regulations\n"

echo -e "${BLUE}📞 SUPPORT:${NC}"
echo -e "• GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL"
echo -e "• Email: rajsaraswati.jatav@gmail.com"
echo -e "• YouTube: @rajsaraswatijatav\n"

echo -e "${GREEN}Happy Learning! 🚀${NC}"