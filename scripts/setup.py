#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Setup Script
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("\033[94m" + "="*50)
    print("  DDOS ATTACK EDUCATIONAL TOOLKIT SETUP")
    print("  Created By: Rajsaraswati Jatav")
    print("  GitHub: @RAJSARASWATI-JATAV")
    print("="*50 + "\033[0m")
    print("\033[93m⚠️  FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️\033[0m\n")

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("\033[91m[ERROR]\033[0m Python 3.8 or higher is required")
        sys.exit(1)
    print(f"\033[92m[OK]\033[0m Python {sys.version.split()[0]} detected")

def install_requirements():
    """Install Python requirements"""
    print("\033[94m[INFO]\033[0m Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\033[92m[OK]\033[0m Requirements installed")
    except subprocess.CalledProcessError:
        print("\033[91m[ERROR]\033[0m Failed to install requirements")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "assets/sounds",
        "assets/visuals",
        "config",
        "docs",
        "tests",
        "scripts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("\033[92m[OK]\033[0m Directories created")

def create_default_config():
    """Create default configuration files"""
    config_dir = Path("config")
    
    # Default settings
    default_settings = {
        "application": {
            "name": "DDOS Attack Educational Toolkit",
            "version": "1.0.0",
            "author": "Rajsaraswati Jatav"
        },
        "attack_settings": {
            "default_threads": 1000,
            "max_threads": "unlimited",
            "default_duration": 60,
            "default_port": 80
        },
        "interface": {
            "sound_effects": True,
            "visual_effects": True,
            "colored_output": True
        }
    }
    
    # Write settings.json if it doesn't exist
    settings_file = config_dir / "settings.json"
    if not settings_file.exists():
        with open(settings_file, "w") as f:
            json.dump(default_settings, f, indent=2)
    
    # Create empty proxy list if it doesn't exist
    proxy_file = config_dir / "proxies.txt"
    if not proxy_file.exists():
        with open(proxy_file, "w") as f:
            f.write("# Add your proxy servers here (IP:PORT)\n")
            f.write("# Example: 127.0.0.1:8080\n")
    
    print("\033[92m[OK]\033[0m Configuration files created")

def set_permissions():
    """Set file permissions"""
    if os.name != 'nt':  # Not Windows
        try:
            os.chmod("main.py", 0o755)
            for script in Path("scripts").glob("*.py"):
                os.chmod(script, 0o755)
            for script in Path("scripts").glob("*.sh"):
                os.chmod(script, 0o755)
            print("\033[92m[OK]\033[0m Permissions set")
        except Exception as e:
            print(f"\033[93m[WARNING]\033[0m Could not set permissions: {e}")

def test_installation():
    """Test the installation"""
    print("\033[94m[INFO]\033[0m Testing installation...")
    try:
        # Test imports
        import requests
        import colorama
        import psutil
        print("\033[92m[OK]\033[0m All dependencies imported successfully")
        
        # Test main module
        import main
        print("\033[92m[OK]\033[0m Main module loaded successfully")
        
    except ImportError as e:
        print(f"\033[91m[ERROR]\033[0m Import failed: {e}")
        sys.exit(1)

def main():
    """Main setup function"""
    print_banner()
    
    print("\033[94m[INFO]\033[0m Starting setup process...\n")
    
    # Setup steps
    check_python_version()
    install_requirements()
    create_directories()
    create_default_config()
    set_permissions()
    test_installation()
    
    print("\n\033[92m🎉 SETUP COMPLETED SUCCESSFULLY! 🎉\033[0m\n")
    
    print("\033[94m📚 NEXT STEPS:\033[0m")
    print("1. Run: python3 main.py --interactive")
    print("2. Read: docs/usage.md")
    print("3. Configure: config/settings.json\n")
    
    print("\033[93m⚠️  REMEMBER:\033[0m")
    print("• Only test systems you own or have permission to test")
    print("• This tool is for educational purposes only")
    print("• Always follow ethical hacking principles\n")
    
    print("\033[94m📞 SUPPORT:\033[0m")
    print("• GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL")
    print("• Email: rajsaraswati.jatav@gmail.com\n")
    
    print("\033[92mHappy Learning! 🚀\033[0m")

if __name__ == "__main__":
    main()