#!/usr/bin/env python3
"""
DDOS Educational Toolkit - Python Setup Script
Author: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
Purpose: Python package setup and distribution

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import os
import sys
from setuptools import setup, find_packages

# Ensure Python version compatibility
if sys.version_info < (3, 8):
    print("❌ Error: Python 3.8 or higher is required")
    print(f"   Current version: {sys.version}")
    print("   Please upgrade Python and try again")
    sys.exit(1)

# Read long description from README
def read_long_description():
    """Read long description from README file"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "DDOS Educational Toolkit - Advanced cybersecurity testing platform for educational purposes"

# Read version from version file
def get_version():
    """Get version from version file"""
    try:
        with open('VERSION', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "2.0.0"

# Read requirements from requirements.txt
def get_requirements():
    """Get requirements from requirements.txt"""
    try:
        with open('requirements.txt', 'r') as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
            return requirements
    except FileNotFoundError:
        # Fallback requirements
        return [
            'requests>=2.28.0',
            'colorama>=0.4.4',
            'psutil>=5.9.0',
            'numpy>=1.21.0',
            'pycryptodome>=3.15.0',
            'dnspython>=2.2.0',
            'netifaces>=0.11.0',
            'pillow>=9.2.0',
            'click>=8.1.0',
            'tqdm>=4.64.0',
            'tabulate>=0.8.9',
            'rich>=12.5.0',
            'jinja2>=3.1.0',
            'matplotlib>=3.5.0',
            'plotly>=5.9.0'
        ]

# Optional dependencies for different features
extras_require = {
    'full': [
        'scapy>=2.4.5',
        'paramiko>=2.11.0',
        'selenium>=4.4.0',
        'beautifulsoup4>=4.11.0',
        'lxml>=4.9.0',
        'pygame>=2.1.0',
        'pyfiglet>=0.8.0',
        'art>=5.7',
        'typer>=0.6.0'
    ],
    'audio': [
        'pygame>=2.1.0',
        'pydub>=0.25.0',
        'simpleaudio>=1.0.0'
    ],
    'advanced': [
        'scapy>=2.4.5',
        'paramiko>=2.11.0',
        'python-nmap>=0.7.1'
    ],
    'web': [
        'selenium>=4.4.0',
        'beautifulsoup4>=4.11.0',
        'lxml>=4.9.0',
        'flask>=2.2.0'
    ],
    'visualization': [
        'matplotlib>=3.5.0',
        'plotly>=5.9.0',
        'seaborn>=0.11.0'
    ],
    'testing': [
        'pytest>=7.1.0',
        'pytest-cov>=3.0.0',
        'pytest-mock>=3.8.0',
        'memory-profiler>=0.60.0'
    ],
    'development': [
        'black>=22.6.0',
        'flake8>=5.0.0',
        'mypy>=0.971',
        'pre-commit>=2.20.0',
        'sphinx>=5.1.0',
        'sphinx-rtd-theme>=1.0.0'
    ]
}

# Development requirements (combination of testing and development)
extras_require['dev'] = list(set(
    extras_require['testing'] + 
    extras_require['development'] + 
    extras_require['full']
))

# Complete installation (all extras)
extras_require['complete'] = list(set(
    sum(extras_require.values(), [])
))

# Entry points for console scripts
entry_points = {
    'console_scripts': [
        'ddos-toolkit=main:main',
        'ddos-edu=main:main',
        'ddos-test=main:test_main',
        'ddos-install=scripts.install:main',
        'ddos-update=scripts.auto_update:main',
    ]
}

# Package data files
package_data = {
    'ddos_educational_toolkit': [
        'assets/sounds/*.wav',
        'assets/visuals/*.png',
        'assets/visuals/*.ascii',
        'config/*.json',
        'docs/*.md',
        'scripts/*.sh',
        'scripts/*.py',
        'templates/*.html',
        'templates/*.jinja2',
    ]
}

# Data files for installation
data_files = [
    ('share/ddos-educational-toolkit/config', ['config/settings.json']),
    ('share/ddos-educational-toolkit/docs', [
        'docs/features.md',
        'docs/legal.md',
        'docs/troubleshooting.md',
        'docs/api_reference.md'
    ]),
    ('share/ddos-educational-toolkit/assets/sounds', [
        'assets/sounds/startup.wav',
        'assets/sounds/attack_start.wav',
        'assets/sounds/attack_complete.wav',
        'assets/sounds/error.wav'
    ] if os.path.exists('assets/sounds') else []),
    ('share/ddos-educational-toolkit/scripts', [
        'scripts/install.sh',
        'scripts/start.sh',
        'scripts/auto_update.py'
    ]),
]

# Custom commands
class CustomCommand:
    """Base class for custom setup commands"""
    
    def __init__(self):
        self.commands = {}
    
    def run_command(self, command_name):
        """Run a custom command"""
        if command_name in self.commands:
            self.commands[command_name]()
        else:
            print(f"❌ Unknown command: {command_name}")

# Custom installation command
class InstallCommand(CustomCommand):
    """Custom installation command with additional setup"""
    
    def __init__(self):
        super().__init__()
        self.commands = {
            'install_system_deps': self.install_system_dependencies,
            'setup_dirs': self.setup_directories,
            'generate_config': self.generate_default_config,
            'set_permissions': self.set_file_permissions
        }
    
    def install_system_dependencies(self):
        """Install system-level dependencies"""
        print("🔧 Installing system dependencies...")
        import subprocess
        import platform
        
        system = platform.system().lower()
        
        try:
            if system == "linux":
                # Try different package managers
                if os.system("which apt-get > /dev/null 2>&1") == 0:
                    subprocess.run([
                        "sudo", "apt-get", "install", "-y",
                        "python3-dev", "build-essential", "libssl-dev",
                        "libffi-dev", "net-tools", "nmap"
                    ], check=True)
                elif os.system("which yum > /dev/null 2>&1") == 0:
                    subprocess.run([
                        "sudo", "yum", "install", "-y",
                        "python3-devel", "gcc", "openssl-devel",
                        "libffi-devel", "net-tools", "nmap"
                    ], check=True)
            
            print("✅ System dependencies installed successfully")
            
        except subprocess.CalledProcessError:
            print("⚠️ Warning: Some system dependencies may not be installed")
        except FileNotFoundError:
            print("⚠️ Warning: Package manager not found")
    
    def setup_directories(self):
        """Setup required directories"""
        print("📁 Setting up directories...")
        
        directories = [
            'logs', 'reports', 'config', 'backups', 'temp',
            'assets/sounds', 'assets/visuals', 'modules', 'utils'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created: {directory}")
    
    def generate_default_config(self):
        """Generate default configuration files"""
        print("⚙️ Generating default configuration...")
        
        import json
        
        config = {
            "version": get_version(),
            "author": "Rajsaraswati Jatav",
            "installation_date": str(datetime.now().isoformat()),
            "default_settings": {
                "max_threads": 1000,
                "default_timeout": 30,
                "log_level": "INFO",
                "enable_colors": True,
                "enable_sounds": True
            }
        }
        
        os.makedirs('config', exist_ok=True)
        with open('config/settings.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration generated")
    
    def set_file_permissions(self):
        """Set proper file permissions"""
        print("🔐 Setting file permissions...")
        
        # Make scripts executable
        script_files = [
            'scripts/install.sh',
            'scripts/start.sh',
            'main.py'
        ]
        
        for script in script_files:
            if os.path.exists(script):
                os.chmod(script, 0o755)
                print(f"✅ Made executable: {script}")

# Validate environment
def validate_environment():
    """Validate the installation environment"""
    print("🔍 Validating environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check if we're in a virtual environment (recommended)
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️ Warning: Not in a virtual environment (recommended)")
    
    # Check available space (basic check)
    import shutil
    total, used, free = shutil.disk_usage(".")
    free_mb = free // (1024*1024)
    
    if free_mb < 100:  # Require at least 100MB free
        print(f"⚠️ Warning: Low disk space ({free_mb}MB free)")
    else:
        print(f"✅ Sufficient disk space ({free_mb}MB free)")
    
    return True

# Post-installation hook
def post_install():
    """Run post-installation tasks"""
    print("\n🚀 Running post-installation setup...")
    
    try:
        # Validate environment
        validate_environment()
        
        # Run custom installation steps
        installer = InstallCommand()
        installer.run_command('setup_dirs')
        installer.run_command('generate_config')
        installer.run_command('set_permissions')
        
        print("\n🎉 Post-installation setup completed!")
        print("\n📚 Quick Start:")
        print("   python3 main.py --help")
        print("   python3 main.py --interactive")
        
        print("\n⚖️ Legal Reminder:")
        print("   This tool is for EDUCATIONAL purposes only")
        print("   Always obtain authorization before testing")
        
    except Exception as e:
        print(f"⚠️ Warning: Post-installation setup encountered issues: {e}")

# Main setup configuration
def main():
    """Main setup function"""
    
    setup(
        # Basic package information
        name="ddos-educational-toolkit",
        version=get_version(),
        author="Rajsaraswati Jatav",
        author_email="rajsaraswati.jatav@gmail.com",
        description="Advanced DDOS Educational Toolkit for Cybersecurity Learning",
        long_description=read_long_description(),
        long_description_content_type="text/markdown",
        url="https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL",
        download_url="https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL/archive/v2.0.tar.gz",
        
        # Package configuration
        packages=find_packages(),
        py_modules=['main'],
        include_package_data=True,
        package_data=package_data,
        data_files=data_files,
        
        # Dependencies
        python_requires=">=3.8",
        install_requires=get_requirements(),
        extras_require=extras_require,
        
        # Entry points
        entry_points=entry_points,
        
        # Classification
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Topic :: Security",
            "Topic :: Education :: Testing",
            "Topic :: System :: Networking",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Operating System :: OS Independent",
            "Environment :: Console",
            "Natural Language :: English",
        ],
        
        # Keywords
        keywords=[
            "ddos", "educational", "cybersecurity", "penetration-testing",
            "security-testing", "network-security", "ethical-hacking",
            "security-research", "vulnerability-assessment", "load-testing"
        ],
        
        # Project URLs
        project_urls={
            "Bug Reports": "https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL/issues",
            "Documentation": "https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL/blob/main/docs/",
            "Source": "https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL",
            "YouTube": "https://youtube.com/@rajsaraswatijatav",
            "Funding": "https://github.com/sponsors/RAJSARASWATI-JATAV",
        },
        
        # Additional metadata
        license="MIT",
        platforms=["any"],
        zip_safe=False,
    )
    
    # Run post-installation tasks
    if len(sys.argv) > 1 and sys.argv[1] in ('install', 'develop'):
        post_install()

if __name__ == "__main__":
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(__file__))
    
    try:
        from datetime import datetime
        main()
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   • Check Python version (3.8+ required)")
        print("   • Ensure internet connectivity")
        print("   • Try installing in a virtual environment")
        print("   • Check system dependencies")
        sys.exit(1)
