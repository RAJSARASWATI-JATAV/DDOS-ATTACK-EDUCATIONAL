#!/bin/bash

# DDOS Educational Toolkit - Installation Script
# Author: Rajsaraswati Jatav
# GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
# Purpose: Automated installation and setup
# 
# ⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║         🎯 DDOS EDUCATIONAL TOOLKIT INSTALLER 🎯           ║"
    echo "║                                                              ║"
    echo "║              Created by: Rajsaraswati Jatav                  ║"
    echo "║              Version: 2.0 | Year: 2025                      ║"
    echo "║              Purpose: Educational & Ethical Testing          ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warn "Running as root. This is not recommended for security reasons."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Installation cancelled."
            exit 1
        fi
    fi
}

# Detect operating system
detect_os() {
    log_step "Detecting operating system..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/debian_version ]; then
            OS="debian"
            PKG_MANAGER="apt"
            log_info "Detected: Debian/Ubuntu-based system"
        elif [ -f /etc/redhat-release ]; then
            OS="redhat"
            PKG_MANAGER="yum"
            log_info "Detected: Red Hat/CentOS-based system"
        elif [ -f /etc/arch-release ]; then
            OS="arch"
            PKG_MANAGER="pacman"
            log_info "Detected: Arch Linux-based system"
        else
            OS="linux"
            PKG_MANAGER="unknown"
            log_warn "Unknown Linux distribution. Manual installation may be required."
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        PKG_MANAGER="brew"
        log_info "Detected: macOS"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
        PKG_MANAGER="choco"
        log_info "Detected: Windows (Git Bash/Cygwin)"
    else
        OS="unknown"
        PKG_MANAGER="unknown"
        log_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Check Python installation
check_python() {
    log_step "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [[ $PYTHON_MAJOR -eq 3 ]] && [[ $PYTHON_MINOR -ge 8 ]]; then
            log_info "Python $PYTHON_VERSION found ✓"
            PYTHON_CMD="python3"
        else
            log_error "Python 3.8+ required. Found: $PYTHON_VERSION"
            install_python
        fi
    else
        log_warn "Python3 not found. Installing..."
        install_python
    fi
}

# Install Python
install_python() {
    log_step "Installing Python..."
    
    case $OS in
        "debian")
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv python3-dev
            ;;
        "redhat")
            sudo yum install -y python3 python3-pip python3-devel
            ;;
        "arch")
            sudo pacman -S --noconfirm python python-pip
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew install python3
            else
                log_error "Homebrew not found. Please install Python manually."
                exit 1
            fi
            ;;
        "windows")
            log_error "Please install Python 3.8+ from python.org"
            exit 1
            ;;
        *)
            log_error "Cannot auto-install Python on this system."
            exit 1
            ;;
    esac
    
    PYTHON_CMD="python3"
}

# Check pip installation
check_pip() {
    log_step "Checking pip installation..."
    
    if command -v pip3 &> /dev/null; then
        log_info "pip3 found ✓"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        log_info "pip found ✓"
        PIP_CMD="pip"
    else
        log_error "pip not found. Installing..."
        install_pip
    fi
}

# Install pip
install_pip() {
    log_step "Installing pip..."
    
    if command -v python3 &> /dev/null; then
        python3 -m ensurepip --upgrade
        PIP_CMD="python3 -m pip"
    else
        case $OS in
            "debian")
                sudo apt install -y python3-pip
                ;;
            "redhat")
                sudo yum install -y python3-pip
                ;;
            "arch")
                sudo pacman -S --noconfirm python-pip
                ;;
            *)
                log_error "Cannot install pip automatically."
                exit 1
                ;;
        esac
        PIP_CMD="pip3"
    fi
}

# Install system dependencies
install_system_dependencies() {
    log_step "Installing system dependencies..."
    
    case $OS in
        "debian")
            sudo apt update
            sudo apt install -y \
                curl wget git \
                build-essential \
                libssl-dev libffi-dev \
                python3-dev \
                net-tools \
                nmap \
                dnsutils \
                iputils-ping \
                netcat-openbsd \
                sox \
                ffmpeg
            ;;
        "redhat")
            sudo yum groupinstall -y "Development Tools"
            sudo yum install -y \
                curl wget git \
                openssl-devel libffi-devel \
                python3-devel \
                net-tools \
                nmap \
                bind-utils \
                iputils \
                nc \
                sox \
                ffmpeg
            ;;
        "arch")
            sudo pacman -S --noconfirm \
                curl wget git \
                base-devel \
                openssl libffi \
                python \
                net-tools \
                nmap \
                dnsutils \
                iputils \
                netcat \
                sox \
                ffmpeg
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew install curl wget git nmap sox ffmpeg
            else
                log_warn "Homebrew not found. Some features may not work."
            fi
            ;;
        *)
            log_warn "Cannot install system dependencies automatically."
            ;;
    esac
}

# Install Python dependencies
install_python_dependencies() {
    log_step "Installing Python dependencies..."
    
    # Upgrade pip first
    $PIP_CMD install --upgrade pip setuptools wheel
    
    # Check if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        log_info "Installing from requirements.txt..."
        $PIP_CMD install -r requirements.txt
    else
        log_info "Installing essential dependencies..."
        $PIP_CMD install \
            requests \
            colorama \
            psutil \
            numpy \
            pycryptodome \
            scapy \
            dnspython \
            paramiko \
            netifaces \
            python-nmap \
            selenium \
            beautifulsoup4 \
            lxml \
            pillow \
            pygame \
            matplotlib \
            plotly \
            jinja2 \
            click \
            tqdm \
            tabulate \
            pyfiglet \
            art \
            rich \
            typer
    fi
}

# Create virtual environment
create_virtual_environment() {
    log_step "Creating virtual environment..."
    
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        log_info "Virtual environment created ✓"
    else
        log_info "Virtual environment already exists ✓"
    fi
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        log_info "Virtual environment activated ✓"
    else
        log_error "Failed to activate virtual environment"
    fi
}

# Setup directories
setup_directories() {
    log_step "Setting up directory structure..."
    
    directories=(
        "logs"
        "reports" 
        "config"
        "backups"
        "temp"
        "assets/sounds"
        "assets/visuals"
        "docs"
        "tests"
        "modules"
        "utils"
        "scripts"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_info "Created directory: $dir"
        fi
    done
}

# Generate default configuration
generate_config() {
    log_step "Generating default configuration..."
    
    if [ ! -f "config/settings.json" ]; then
        cat > config/settings.json << 'EOF'
{
    "version": "2.0",
    "author": "Rajsaraswati Jatav",
    "default_settings": {
        "max_threads": 1000,
        "default_timeout": 30,
        "connection_timeout": 10,
        "max_retries": 3,
        "default_user_agent": "DDOS-Educational-Toolkit/2.0",
        "log_level": "INFO",
        "enable_colors": true,
        "enable_sounds": true,
        "enable_animations": true
    },
    "attack_limits": {
        "max_duration": 300,
        "max_threads_per_attack": 5000,
        "max_concurrent_attacks": 10
    },
    "safety_settings": {
        "require_confirmation": true,
        "enable_safety_checks": true,
        "auto_stop_on_error": false,
        "max_error_rate": 50
    },
    "proxy_settings": {
        "enable_proxy_rotation": true,
        "proxy_timeout": 10,
        "max_proxy_retries": 3,
        "proxy_validation_threads": 50
    },
    "reporting": {
        "auto_generate_reports": true,
        "report_formats": ["html", "json", "csv"],
        "save_statistics": true,
        "statistics_retention_days": 30
    }
}
EOF
        log_info "Default configuration created ✓"
    else
        log_info "Configuration file already exists ✓"
    fi
}

# Set file permissions
set_permissions() {
    log_step "Setting file permissions..."
    
    # Make scripts executable
    chmod +x scripts/*.sh 2>/dev/null || true
    chmod +x main.py 2>/dev/null || true
    
    # Set proper permissions for directories
    find . -type d -exec chmod 755 {} \; 2>/dev/null || true
    find . -type f -name "*.py" -exec chmod 644 {} \; 2>/dev/null || true
    
    log_info "File permissions set ✓"
}

# Create desktop entry (Linux only)
create_desktop_entry() {
    if [[ "$OS" == "debian" ]] || [[ "$OS" == "redhat" ]] || [[ "$OS" == "arch" ]]; then
        log_step "Creating desktop entry..."
        
        DESKTOP_FILE="$HOME/.local/share/applications/ddos-educational-toolkit.desktop"
        CURRENT_DIR=$(pwd)
        
        mkdir -p "$HOME/.local/share/applications"
        
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=DDOS Educational Toolkit
Comment=Educational cybersecurity testing toolkit
Exec=bash -c "cd '$CURRENT_DIR' && python3 main.py"
Icon=$CURRENT_DIR/assets/visuals/logo.png
Terminal=true
Type=Application
Categories=Development;Security;Education;
Keywords=security;ddos;testing;education;ethical;
StartupNotify=true
EOF
        
        chmod +x "$DESKTOP_FILE"
        log_info "Desktop entry created ✓"
    fi
}

# Run post-installation tests
run_tests() {
    log_step "Running post-installation tests..."
    
    # Test Python imports
    $PYTHON_CMD -c "
import sys
import requests
import colorama
import psutil
print('✓ Essential imports successful')
print(f'✓ Python version: {sys.version}')
print('✓ Installation appears successful!')
" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        log_info "Post-installation tests passed ✓"
    else
        log_error "Some post-installation tests failed"
    fi
}

# Cleanup function
cleanup() {
    log_step "Cleaning up temporary files..."
    
    # Remove temporary files
    rm -rf temp/* 2>/dev/null || true
    rm -rf __pycache__ 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    log_info "Cleanup completed ✓"
}

# Show completion message
show_completion() {
    echo
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                        ║${NC}"
    echo -e "${GREEN}║  🎉 INSTALLATION COMPLETED SUCCESSFULLY! 🎉          ║${NC}"
    echo -e "${GREEN}║                                                        ║${NC}"
    echo -e "${GREEN}║  📚 DDOS Educational Toolkit v2.0 is ready to use     ║${NC}"
    echo -e "${GREEN}║  👨‍💻 Created by: Rajsaraswati Jatav                    ║${NC}"
    echo -e "${GREEN}║                                                        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${CYAN}🚀 QUICK START:${NC}"
    echo -e "${WHITE}   Interactive Mode:${NC} python3 main.py --interactive"
    echo -e "${WHITE}   Command Line:${NC}    python3 main.py --help"
    echo -e "${WHITE}   Run Tests:${NC}       python3 -m pytest tests/"
    echo
    echo -e "${YELLOW}⚖️ LEGAL REMINDER:${NC}"
    echo -e "${WHITE}   • This tool is for EDUCATIONAL purposes only${NC}"
    echo -e "${WHITE}   • Always obtain written authorization before testing${NC}"
    echo -e "${WHITE}   • Follow all applicable laws and ethical guidelines${NC}"
    echo
    echo -e "${PURPLE}📞 SUPPORT:${NC}"
    echo -e "${WHITE}   • GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL${NC}"
    echo -e "${WHITE}   • Email: rajsaraswati.jatav@gmail.com${NC}"
    echo -e "${WHITE}   • YouTube: @rajsaraswatijatav${NC}"
    echo
}

# Error handler
handle_error() {
    log_error "Installation failed at step: $1"
    log_error "Check the error messages above for details"
    echo
    echo -e "${YELLOW}💡 TROUBLESHOOTING TIPS:${NC}"
    echo "  • Make sure you have internet connection"
    echo "  • Try running with sudo if permission errors occur"
    echo "  • Check if Python 3.8+ is properly installed"
    echo "  • Manually install dependencies if auto-install fails"
    echo
    exit 1
}

# Main installation function
main() {
    # Set up error handling
    trap 'handle_error "Unknown step"' ERR
    
    # Show banner
    print_banner
    
    # Legal warning
    echo -e "${RED}⚠️ LEGAL WARNING ⚠️${NC}"
    echo "This tool is for EDUCATIONAL and AUTHORIZED TESTING purposes only."
    echo "Unauthorized use is ILLEGAL and may result in severe penalties."
    echo "By proceeding, you agree to use this tool ethically and legally."
    echo
    read -p "Do you agree to these terms? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Installation cancelled. Please read the legal guidelines."
        exit 1
    fi
    
    # Installation steps
    check_root
    detect_os
    check_python
    check_pip
    install_system_dependencies || log_warn "Some system dependencies may not be installed"
    setup_directories
    create_virtual_environment || log_warn "Virtual environment setup failed"
    install_python_dependencies || handle_error "Python dependencies installation"
    generate_config
    set_permissions
    create_desktop_entry || log_warn "Desktop entry creation failed"
    run_tests || log_warn "Some tests failed"
    cleanup
    
    # Show completion message
    show_completion
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
