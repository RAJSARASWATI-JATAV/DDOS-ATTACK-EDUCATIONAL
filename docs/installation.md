# 🚀 Installation Guide

**DDOS Attack Educational Toolkit**
*Created By: Rajsaraswati Jatav*

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL.git
cd DDOS-ATTACK-EDUCATIONAL
```

### 2. Auto Installation
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### 3. Run Toolkit
```bash
python main.py --interactive
```

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Storage**: 50 MB
- **Network**: Internet connection

### Recommended Requirements
- **Python**: 3.10 or higher
- **RAM**: 2 GB or more
- **CPU**: Multi-core processor
- **Storage**: 100 MB
- **OS**: Linux (preferred), Windows, Android (Termux)

## 📱 Platform-Specific Installation

### Linux (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Clone and setup
git clone https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL.git
cd DDOS-ATTACK-EDUCATIONAL

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run toolkit
python main.py
```

### Windows
```powershell
# Install Python from python.org if not installed

# Clone repository
git clone https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL.git
cd DDOS-ATTACK-EDUCATIONAL

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run toolkit
python main.py
```

### Android (Termux)
```bash
# Install Termux from F-Droid or Play Store

# Update packages
pkg update && pkg upgrade -y

# Install dependencies
pkg install python git -y

# Clone repository
git clone https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL.git
cd DDOS-ATTACK-EDUCATIONAL

# Install Python dependencies
pip install -r requirements.txt

# Run toolkit
python main.py
```

## 🔧 Manual Installation

### Step 1: Python Dependencies
```bash
pip install requests>=2.31.0
pip install colorama>=0.4.6
pip install psutil>=5.9.0
pip install scapy>=2.5.0
pip install pygame>=2.5.0
```

### Step 2: Optional Dependencies
```bash
# For GUI interface (optional)
pip install PyQt5>=5.15.0

# For development (optional)
pip install pytest>=7.0.0
pip install black>=22.0.0
pip install flake8>=5.0.0
```

## ⚙️ Configuration

### Basic Setup
1. **Edit Configuration**
   ```bash
   nano config/settings.json
   ```

2. **Customize Settings**
   - Thread limits
   - Sound effects
   - Visual effects
   - Logging levels

3. **Add Targets** (Optional)
   ```bash
   nano config/targets.json
   ```

### Advanced Setup
1. **Proxy Configuration**
   ```bash
   echo "proxy1:port" >> config/proxies.txt
   echo "proxy2:port" >> config/proxies.txt
   ```

2. **User Agents**
   ```bash
   nano config/user_agents.txt
   ```

## 🔍 Verification

### Test Installation
```bash
# Basic test
python main.py --help

# Interactive mode test
python main.py --interactive

# Module test
python -c "import main; print('Installation successful!')"
```

### Check Dependencies
```bash
# List installed packages
pip list | grep -E "(requests|colorama|psutil|scapy|pygame)"

# Version check
python --version
```

## 🐛 Troubleshooting

### Common Issues

#### Permission Errors (Linux)
```bash
# Fix permissions
chmod +x scripts/*.sh
sudo chown -R $USER:$USER .
```

#### Missing Dependencies
```bash
# Force reinstall
pip install --force-reinstall -r requirements.txt

# Update pip
python -m pip install --upgrade pip
```

#### Audio Issues
```bash
# Install audio libraries (Linux)
sudo apt install python3-pygame

# Disable sound if needed
python main.py --no-sound
```

#### Network Issues
```bash
# Test connectivity
ping google.com

# Check firewall
sudo ufw status
```

### Advanced Troubleshooting

#### Debug Mode
```bash
export DEBUG=1
python main.py --interactive
```

#### Clean Installation
```bash
# Remove virtual environment
rm -rf venv/

# Reinstall
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📞 Support

If you encounter issues:

1. **Check Documentation**: Read the full documentation
2. **GitHub Issues**: Search existing issues
3. **Community**: Ask in discussions
4. **Contact**: rajsaraswati.jatav@gmail.com

---

**Happy Learning! 🎆**