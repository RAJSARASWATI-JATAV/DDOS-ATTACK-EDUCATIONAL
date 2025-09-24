#!/bin/bash

# DDOS Educational Toolkit - Startup Script
# Author: Rajsaraswati Jatav  
# GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
# Purpose: Easy startup and environment management
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

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/venv"
LOG_FILE="$PROJECT_DIR/logs/startup.log"
PID_FILE="$PROJECT_DIR/temp/ddos_toolkit.pid"

# Startup banner
show_banner() {
    clear
    echo -e "${PURPLE}"
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    🚀 DDOS EDUCATIONAL TOOLKIT LAUNCHER 🚀                   ║
║                                                                ║
║              Created by: Rajsaraswati Jatav                    ║
║              Version: 2.0 | Year: 2025                        ║
║              Purpose: Educational & Ethical Testing            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Logging functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo -e "$1"
}

log_info() {
    log "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    log "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    log "${RED}[ERROR]${NC} $1"
}

log_step() {
    log "${CYAN}[STEP]${NC} $1"
}

# Check if running as root (not recommended)
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warn "⚠️ Running as root is not recommended for security reasons!"
        echo -e "${YELLOW}Press Enter to continue or Ctrl+C to exit...${NC}"
        read
    fi
}

# Setup logging directory
setup_logging() {
    mkdir -p "$(dirname "$LOG_FILE")"
    mkdir -p "$PROJECT_DIR/temp"
    
    # Rotate log files if they get too large
    if [[ -f "$LOG_FILE" ]] && [[ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo 0) -gt 10485760 ]]; then
        mv "$LOG_FILE" "$LOG_FILE.old"
    fi
    
    # Start fresh log session
    echo "=== DDOS Educational Toolkit Startup $(date) ===" >> "$LOG_FILE"
}

# Detect operating system
detect_system() {
    log_step "🔍 Detecting system environment..."
    
    OS="unknown"
    ARCH="unknown"
    
    # Detect OS
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="macOS";;
        CYGWIN*)    OS="Windows";;
        MINGW*)     OS="Windows";;
        MSYS*)      OS="Windows";;
        *)          OS="Unknown";;
    esac
    
    # Detect architecture
    case "$(uname -m)" in
        x86_64|amd64)   ARCH="x64";;
        i386|i686)      ARCH="x86";;
        arm64|aarch64)  ARCH="arm64";;
        armv7l)         ARCH="arm32";;
        *)              ARCH="unknown";;
    esac
    
    log_info "🖥️ System: $OS ($ARCH)"
    
    # System-specific adjustments
    case $OS in
        "Linux")
            if command -v termux-setup-storage &> /dev/null; then
                log_info "📱 Termux environment detected"
                TERMUX=true
            else
                TERMUX=false
            fi
            ;;
        "macOS")
            log_info "🍎 macOS environment detected"
            ;;
        "Windows")
            log_info "🪟 Windows environment detected"
            ;;
    esac
}

# Check Python installation
check_python() {
    log_step "🐍 Checking Python installation..."
    
    # Find Python executable
    PYTHON_CMD=""
    for cmd in python3.12 python3.11 python3.10 python3.9 python3.8 python3 python; do
        if command -v "$cmd" &> /dev/null; then
            PYTHON_VERSION=$($cmd --version 2>&1 | cut -d' ' -f2)
            PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
            PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)
            
            if [[ $PYTHON_MAJOR -eq 3 ]] && [[ $PYTHON_MINOR -ge 8 ]]; then
                PYTHON_CMD="$cmd"
                log_info "✅ Found Python $PYTHON_VERSION: $cmd"
                break
            fi
        fi
    done
    
    if [[ -z "$PYTHON_CMD" ]]; then
        log_error "❌ Python 3.8+ not found!"
        log_error "Please install Python 3.8 or higher and try again"
        echo -e "\n${YELLOW}Installation guides:${NC}"
        echo -e "  ${WHITE}Ubuntu/Debian:${NC} sudo apt install python3 python3-pip"
        echo -e "  ${WHITE}CentOS/RHEL:${NC}   sudo yum install python3 python3-pip"
        echo -e "  ${WHITE}macOS:${NC}         brew install python3"
        echo -e "  ${WHITE}Windows:${NC}       Download from python.org"
        exit 1
    fi
    
    # Check pip
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        log_error "❌ pip not available"
        log_error "Please install pip: $PYTHON_CMD -m ensurepip --upgrade"
        exit 1
    fi
    
    log_info "✅ pip available"
}

# Setup virtual environment
setup_virtualenv() {
    log_step "🏠 Setting up virtual environment..."
    
    if [[ ! -d "$VENV_DIR" ]]; then
        log_info "📦 Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        
        if [[ $? -ne 0 ]]; then
            log_error "❌ Failed to create virtual environment"
            exit 1
        fi
        
        log_info "✅ Virtual environment created"
    else
        log_info "✅ Virtual environment exists"
    fi
    
    # Activate virtual environment
    if [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
        log_info "✅ Virtual environment activated"
        PYTHON_CMD="python"  # Use venv python
    elif [[ -f "$VENV_DIR/Scripts/activate" ]]; then  # Windows
        source "$VENV_DIR/Scripts/activate"
        log_info "✅ Virtual environment activated (Windows)"
        PYTHON_CMD="python"
    else
        log_warn "⚠️ Could not activate virtual environment"
    fi
}

# Check and install dependencies
check_dependencies() {
    log_step "📚 Checking dependencies..."
    
    # Check if requirements.txt exists
    if [[ ! -f "$PROJECT_DIR/requirements.txt" ]]; then
        log_warn "⚠️ requirements.txt not found, installing basic dependencies"
        
        # Install essential dependencies
        $PYTHON_CMD -m pip install --upgrade pip setuptools wheel
        $PYTHON_CMD -m pip install requests colorama psutil
        
        return
    fi
    
    # Check if dependencies are installed
    log_info "🔍 Verifying installed packages..."
    
    missing_deps=()
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^#.*$ ]] || [[ -z "$line" ]] && continue
        
        # Extract package name (before any version specifiers)
        package=$(echo "$line" | sed 's/[>=<].*//' | tr '[:upper:]' '[:lower:]')
        
        if ! $PYTHON_CMD -c "import $package" 2>/dev/null; then
            missing_deps+=("$line")
        fi
    done < "$PROJECT_DIR/requirements.txt"
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_info "📦 Installing missing dependencies..."
        $PYTHON_CMD -m pip install --upgrade pip
        $PYTHON_CMD -m pip install -r "$PROJECT_DIR/requirements.txt"
        
        if [[ $? -ne 0 ]]; then
            log_error "❌ Failed to install dependencies"
            log_error "Try running: pip install -r requirements.txt"
            exit 1
        fi
        
        log_info "✅ Dependencies installed"
    else
        log_info "✅ All dependencies satisfied"
    fi
}

# Check system resources
check_system_resources() {
    log_step "🔧 Checking system resources..."
    
    # Check available memory
    if command -v free &> /dev/null; then
        mem_total=$(free -m | awk 'NR==2{print $2}')
        mem_available=$(free -m | awk 'NR==2{print $7}')
        
        if [[ $mem_available -lt 256 ]]; then
            log_warn "⚠️ Low available memory: ${mem_available}MB"
            log_warn "The toolkit may run slower with limited memory"
        else
            log_info "✅ Memory: ${mem_available}MB available"
        fi
    fi
    
    # Check disk space
    disk_free=$(df -h "$PROJECT_DIR" | awk 'NR==2{print $4}' | sed 's/[^0-9.]//g')
    if [[ -n "$disk_free" ]] && [[ $(echo "$disk_free < 100" | bc -l 2>/dev/null || echo 0) -eq 1 ]]; then
        log_warn "⚠️ Low disk space: ${disk_free}MB free"
    else
        log_info "✅ Sufficient disk space available"
    fi
    
    # Check network connectivity
    if ping -c 1 8.8.8.8 &> /dev/null; then
        log_info "✅ Network connectivity available"
    else
        log_warn "⚠️ No network connectivity detected"
        log_warn "Some features may not work properly"
    fi
}

# Check for updates
check_updates() {
    if [[ "$SKIP_UPDATE_CHECK" != "true" ]]; then
        log_step "🔍 Checking for updates..."
        
        if [[ -f "$PROJECT_DIR/scripts/auto_update.py" ]]; then
            $PYTHON_CMD "$PROJECT_DIR/scripts/auto_update.py" --check &
            UPDATE_PID=$!
            
            # Don't wait too long for update check
            sleep 2
            if kill -0 $UPDATE_PID 2>/dev/null; then
                log_info "⏳ Update check running in background..."
            fi
        else
            log_info "📋 Manual update check: git pull origin main"
        fi
    fi
}

# Validate installation
validate_installation() {
    log_step "✅ Validating installation..."
    
    # Check main files exist
    required_files=(
        "main.py"
        "attack_modules.py"
        "utils/statistics.py"
        "utils/logger.py"
    )
    
    missing_files=()
    for file in "${required_files[@]}"; do
        if [[ ! -f "$PROJECT_DIR/$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        log_error "❌ Missing required files:"
        for file in "${missing_files[@]}"; do
            log_error "   - $file"
        done
        log_error "Please reinstall or run the installation script"
        exit 1
    fi
    
    # Test Python imports
    if $PYTHON_CMD -c "
import sys, os
sys.path.insert(0, '$PROJECT_DIR')
try:
    from utils.logger import Logger
    from utils.statistics import Statistics
    print('✅ Core modules import successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
" 2>/dev/null; then
        log_info "✅ Installation validation passed"
    else
        log_error "❌ Installation validation failed"
        log_error "Some core modules cannot be imported"
        exit 1
    fi
}

# Show startup menu
show_menu() {
    echo -e "\n${CYAN}🎯 DDOS Educational Toolkit - Startup Options${NC}\n"
    echo -e "${WHITE}1.${NC} Interactive Mode (Recommended)"
    echo -e "${WHITE}2.${NC} Command Line Mode"
    echo -e "${WHITE}3.${NC} Run Tests"
    echo -e "${WHITE}4.${NC} Show Help"
    echo -e "${WHITE}5.${NC} Update Toolkit"
    echo -e "${WHITE}6.${NC} System Information"
    echo -e "${WHITE}7.${NC} Configuration"
    echo -e "${WHITE}8.${NC} Exit"
    echo
}

# Handle menu selection
handle_menu_selection() {
    local choice="$1"
    
    case $choice in
        1)
            log_info "🚀 Starting Interactive Mode..."
            cd "$PROJECT_DIR"
            $PYTHON_CMD main.py --interactive
            ;;
        2)
            log_info "⌨️ Starting Command Line Mode..."
            cd "$PROJECT_DIR"
            echo -e "${YELLOW}Enter command line arguments (or press Enter for help):${NC}"
            read -r args
            if [[ -z "$args" ]]; then
                args="--help"
            fi
            $PYTHON_CMD main.py $args
            ;;
        3)
            log_info "🧪 Running Tests..."
            cd "$PROJECT_DIR"
            if [[ -d "tests" ]]; then
                $PYTHON_CMD -m pytest tests/ -v
            else
                log_warn "⚠️ No tests directory found"
            fi
            ;;
        4)
            log_info "📖 Showing Help..."
            cd "$PROJECT_DIR"
            $PYTHON_CMD main.py --help
            ;;
        5)
            log_info "🔄 Checking for Updates..."
            cd "$PROJECT_DIR"
            if [[ -f "scripts/auto_update.py" ]]; then
                $PYTHON_CMD scripts/auto_update.py --update
            else
                log_info "Manual update: git pull origin main"
            fi
            ;;
        6)
            show_system_info
            ;;
        7)
            configure_toolkit
            ;;
        8)
            log_info "👋 Goodbye!"
            cleanup
            exit 0
            ;;
        *)
            log_error "❌ Invalid selection: $choice"
            return 1
            ;;
    esac
}

# Show system information
show_system_info() {
    echo -e "\n${CYAN}🖥️ System Information${NC}\n"
    echo -e "${WHITE}Operating System:${NC} $OS ($ARCH)"
    echo -e "${WHITE}Python Version:${NC} $($PYTHON_CMD --version 2>&1)"
    echo -e "${WHITE}Python Path:${NC} $(which $PYTHON_CMD)"
    echo -e "${WHITE}Project Directory:${NC} $PROJECT_DIR"
    echo -e "${WHITE}Virtual Environment:${NC} $VENV_DIR"
    
    if command -v git &> /dev/null && [[ -d "$PROJECT_DIR/.git" ]]; then
        echo -e "${WHITE}Git Branch:${NC} $(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null || echo 'N/A')"
        echo -e "${WHITE}Git Commit:${NC} $(git -C "$PROJECT_DIR" rev-parse --short HEAD 2>/dev/null || echo 'N/A')"
    fi
    
    echo -e "${WHITE}Current Time:${NC} $(date)"
    
    # Show resource usage
    if command -v free &> /dev/null; then
        echo -e "${WHITE}Memory Usage:${NC}"
        free -h | head -2 | tail -1
    fi
    
    if command -v df &> /dev/null; then
        echo -e "${WHITE}Disk Usage:${NC}"
        df -h "$PROJECT_DIR" | tail -1
    fi
    
    echo
    read -p "Press Enter to continue..."
}

# Configure toolkit
configure_toolkit() {
    echo -e "\n${CYAN}⚙️ Toolkit Configuration${NC}\n"
    
    config_file="$PROJECT_DIR/config/settings.json"
    
    if [[ -f "$config_file" ]]; then
        echo -e "${WHITE}Current Configuration:${NC}"
        cat "$config_file" | $PYTHON_CMD -m json.tool 2>/dev/null || cat "$config_file"
    else
        log_warn "⚠️ Configuration file not found: $config_file"
    fi
    
    echo
    echo -e "${YELLOW}Configuration options:${NC}"
    echo -e "${WHITE}1.${NC} Edit configuration file"
    echo -e "${WHITE}2.${NC} Reset to defaults"
    echo -e "${WHITE}3.${NC} Backup configuration"
    echo -e "${WHITE}4.${NC} Return to main menu"
    
    read -p "Select option [1-4]: " config_choice
    
    case $config_choice in
        1)
            if command -v nano &> /dev/null; then
                nano "$config_file"
            elif command -v vim &> /dev/null; then
                vim "$config_file"
            else
                log_error "❌ No text editor found (nano/vim)"
            fi
            ;;
        2)
            log_info "🔄 Resetting configuration to defaults..."
            if [[ -f "$PROJECT_DIR/scripts/install.sh" ]]; then
                bash "$PROJECT_DIR/scripts/install.sh" --generate-config
            fi
            ;;
        3)
            backup_file="$PROJECT_DIR/backups/config_$(date +%Y%m%d_%H%M%S).json"
            mkdir -p "$(dirname "$backup_file")"
            cp "$config_file" "$backup_file" 2>/dev/null && \
                log_info "✅ Configuration backed up to: $backup_file" || \
                log_error "❌ Backup failed"
            ;;
        4)
            return
            ;;
    esac
}

# Cleanup function
cleanup() {
    log_step "🧹 Cleaning up..."
    
    # Remove PID file
    [[ -f "$PID_FILE" ]] && rm -f "$PID_FILE"
    
    # Kill any background processes
    if [[ -n "$UPDATE_PID" ]] && kill -0 $UPDATE_PID 2>/dev/null; then
        kill $UPDATE_PID 2>/dev/null
    fi
    
    log_info "✅ Cleanup completed"
}

# Error handler
handle_error() {
    log_error "❌ An error occurred in startup script"
    log_error "Check log file: $LOG_FILE"
    cleanup
    exit 1
}

# Signal handlers
trap cleanup EXIT
trap handle_error ERR

# Main startup function
main() {
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Setup environment
    setup_logging
    show_banner
    
    # Legal warning
    echo -e "${RED}⚠️ LEGAL WARNING ⚠️${NC}"
    echo "This tool is for EDUCATIONAL and AUTHORIZED TESTING purposes only."
    echo "Unauthorized use is ILLEGAL and may result in severe penalties."
    echo
    
    # Startup checks
    check_root
    detect_system
    check_python
    setup_virtualenv
    check_dependencies
    check_system_resources
    validate_installation
    check_updates
    
    echo -e "\n${GREEN}🎉 Startup completed successfully!${NC}"
    
    # Create PID file
    echo $$ > "$PID_FILE"
    
    # Handle command line arguments
    if [[ $# -gt 0 ]]; then
        case "$1" in
            --interactive|-i)
                handle_menu_selection 1
                ;;
            --help|-h)
                handle_menu_selection 4
                ;;
            --test|-t)
                handle_menu_selection 3
                ;;
            --update|-u)
                handle_menu_selection 5
                ;;
            --info)
                show_system_info
                ;;
            --config)
                configure_toolkit
                ;;
            *)
                log_info "⌨️ Passing arguments to main.py..."
                $PYTHON_CMD main.py "$@"
                ;;
        esac
    else
        # Interactive menu
        while true; do
            show_menu
            read -p "Select option [1-8]: " choice
            
            if ! handle_menu_selection "$choice"; then
                continue
            fi
            
            echo
            read -p "Press Enter to return to menu (or 'q' to quit): " continue_choice
            if [[ "$continue_choice" == "q" ]]; then
                break
            fi
        done
    fi
    
    cleanup
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
