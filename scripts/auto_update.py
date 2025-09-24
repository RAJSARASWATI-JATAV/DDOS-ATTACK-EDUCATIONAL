#!/usr/bin/env python3
"""
DDOS Educational Toolkit - Auto Update System
Author: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
Purpose: Automatic updates and version management

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import os
import sys
import json
import requests
import subprocess
import hashlib
import shutil
import tempfile
import zipfile
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

# Add parent directory for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from utils.logger import Logger
    from utils.config_manager import ConfigManager
except ImportError:
    # Fallback logger if utils not available
    class Logger:
        def info(self, msg): print(f"[INFO] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
        def warning(self, msg): print(f"[WARN] {msg}")
        def success(self, msg): print(f"[SUCCESS] {msg}")

class AutoUpdater:
    """Automatic update system for DDOS Educational Toolkit"""
    
    def __init__(self):
        self.logger = Logger()
        self.current_version = self._get_current_version()
        self.repo_url = "https://api.github.com/repos/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL"
        self.download_url = "https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL"
        self.backup_dir = "backups"
        self.temp_dir = tempfile.mkdtemp(prefix="ddos_update_")
        self.config_file = "config/update_config.json"
        self.update_lock = threading.Lock()
        
        # Load update configuration
        self.config = self._load_update_config()
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def _get_current_version(self):
        """Get current installed version"""
        try:
            # Try to read from VERSION file
            if os.path.exists('VERSION'):
                with open('VERSION', 'r') as f:
                    return f.read().strip()
            
            # Try to read from setup.py
            if os.path.exists('setup.py'):
                with open('setup.py', 'r') as f:
                    content = f.read()
                    import re
                    match = re.search(r'version=["\']([^"\']+)["\']', content)
                    if match:
                        return match.group(1)
            
            # Default version
            return "2.0.0"
            
        except Exception as e:
            self.logger.error(f"Could not determine current version: {e}")
            return "unknown"
    
    def _load_update_config(self):
        """Load update configuration"""
        default_config = {
            "auto_check": True,
            "auto_download": False,
            "auto_install": False,
            "check_interval_hours": 24,
            "backup_before_update": True,
            "restore_config_after_update": True,
            "update_channel": "stable",  # stable, beta, dev
            "last_check": None,
            "update_notifications": True,
            "skip_versions": []
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            else:
                # Create default config
                self._save_update_config(default_config)
            
            return default_config
            
        except Exception as e:
            self.logger.error(f"Error loading update config: {e}")
            return default_config
    
    def _save_update_config(self, config):
        """Save update configuration"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving update config: {e}")
    
    def check_for_updates(self, force=False):
        """Check for available updates"""
        self.logger.info("🔍 Checking for updates...")
        
        try:
            # Check if we should skip this check
            if not force and not self._should_check_for_updates():
                self.logger.info("⏭️ Skipping update check (too recent)")
                return None
            
            # Get latest release info
            response = requests.get(f"{self.repo_url}/releases/latest", timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            release_notes = release_data['body']
            download_url = release_data['zipball_url']
            published_date = release_data['published_at']
            
            # Update last check time
            self.config['last_check'] = datetime.now().isoformat()
            self._save_update_config(self.config)
            
            # Compare versions
            if self._is_newer_version(latest_version, self.current_version):
                self.logger.success(f"🆕 New version available: {latest_version} (current: {self.current_version})")
                
                update_info = {
                    'available': True,
                    'current_version': self.current_version,
                    'latest_version': latest_version,
                    'release_notes': release_notes,
                    'download_url': download_url,
                    'published_date': published_date,
                    'release_data': release_data
                }
                
                return update_info
            else:
                self.logger.info(f"✅ You have the latest version: {self.current_version}")
                return {'available': False, 'current_version': self.current_version}
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Failed to check for updates: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error during update check: {e}")
            return None
    
    def _should_check_for_updates(self):
        """Check if we should perform an update check"""
        if not self.config.get('auto_check', True):
            return False
        
        last_check = self.config.get('last_check')
        if not last_check:
            return True
        
        try:
            last_check_date = datetime.fromisoformat(last_check)
            hours_since_check = (datetime.now() - last_check_date).total_seconds() / 3600
            interval = self.config.get('check_interval_hours', 24)
            
            return hours_since_check >= interval
        except Exception:
            return True
    
    def _is_newer_version(self, version1, version2):
        """Compare two version strings"""
        try:
            def version_tuple(v):
                return tuple(map(int, (v.split("."))))
            
            return version_tuple(version1) > version_tuple(version2)
        except Exception:
            return version1 != version2
    
    def download_update(self, update_info):
        """Download the update package"""
        self.logger.info("⬇️ Downloading update...")
        
        try:
            download_url = update_info['download_url']
            version = update_info['latest_version']
            
            # Download with progress
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            zip_path = os.path.join(self.temp_dir, f"ddos-toolkit-{version}.zip")
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r📥 Download progress: {progress:.1f}%", end='', flush=True)
            
            print()  # New line after progress
            self.logger.success(f"✅ Download completed: {zip_path}")
            
            # Verify download
            if os.path.getsize(zip_path) < 1000:  # Basic size check
                raise Exception("Downloaded file appears to be too small")
            
            return zip_path
            
        except Exception as e:
            self.logger.error(f"❌ Download failed: {e}")
            return None
    
    def create_backup(self):
        """Create backup of current installation"""
        self.logger.info("💾 Creating backup...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{self.current_version}_{timestamp}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Files and directories to backup
            items_to_backup = [
                'main.py',
                'attack_modules.py',
                'network_scanner.py',
                'payload_generator.py',
                'proxy_handler.py',
                'utils/',
                'modules/',
                'config/',
                'assets/',
                'docs/',
                'scripts/',
                'requirements.txt',
                'VERSION'
            ]
            
            os.makedirs(backup_path, exist_ok=True)
            
            for item in items_to_backup:
                if os.path.exists(item):
                    if os.path.isfile(item):
                        shutil.copy2(item, backup_path)
                    elif os.path.isdir(item):
                        shutil.copytree(item, os.path.join(backup_path, os.path.basename(item)), 
                                      dirs_exist_ok=True)
            
            self.logger.success(f"✅ Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"❌ Backup failed: {e}")
            return None
    
    def install_update(self, zip_path, backup_path=None):
        """Install the downloaded update"""
        self.logger.info("🚀 Installing update...")
        
        try:
            with self.update_lock:
                # Extract update
                extract_path = os.path.join(self.temp_dir, "extracted")
                os.makedirs(extract_path, exist_ok=True)
                
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                # Find the extracted directory (GitHub creates a subdirectory)
                extracted_dirs = [d for d in os.listdir(extract_path) 
                                if os.path.isdir(os.path.join(extract_path, d))]
                
                if not extracted_dirs:
                    raise Exception("No extracted directory found")
                
                source_dir = os.path.join(extract_path, extracted_dirs[0])
                
                # Preserve user configuration
                user_configs = {}
                if self.config.get('restore_config_after_update', True):
                    user_configs = self._backup_user_configs()
                
                # Install files
                self._install_files(source_dir)
                
                # Restore user configuration
                if user_configs:
                    self._restore_user_configs(user_configs)
                
                # Update version information
                self._update_version_info()
                
                # Run post-update tasks
                self._run_post_update_tasks()
                
                self.logger.success("✅ Update installed successfully!")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Update installation failed: {e}")
            
            # Attempt to restore backup
            if backup_path and os.path.exists(backup_path):
                self.logger.info("🔄 Attempting to restore backup...")
                try:
                    self._restore_backup(backup_path)
                    self.logger.success("✅ Backup restored successfully")
                except Exception as restore_error:
                    self.logger.error(f"❌ Backup restoration failed: {restore_error}")
            
            return False
    
    def _backup_user_configs(self):
        """Backup user configuration files"""
        configs = {}
        
        config_files = [
            'config/settings.json',
            'config/user_preferences.json',
            'config/update_config.json',
            'config/proxies.txt'
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        configs[config_file] = f.read()
                except Exception as e:
                    self.logger.warning(f"Could not backup {config_file}: {e}")
        
        return configs
    
    def _restore_user_configs(self, configs):
        """Restore user configuration files"""
        for config_file, content in configs.items():
            try:
                os.makedirs(os.path.dirname(config_file), exist_ok=True)
                with open(config_file, 'w') as f:
                    f.write(content)
                self.logger.info(f"Restored config: {config_file}")
            except Exception as e:
                self.logger.warning(f"Could not restore {config_file}: {e}")
    
    def _install_files(self, source_dir):
        """Install files from source directory"""
        # Files to skip during update
        skip_files = [
            'config/settings.json',
            'config/user_preferences.json',
            'logs/',
            'reports/',
            'backups/',
            '.git/',
            '__pycache__/',
            '*.pyc',
            '.env'
        ]
        
        for root, dirs, files in os.walk(source_dir):
            # Calculate relative path
            rel_path = os.path.relpath(root, source_dir)
            
            # Skip certain directories
            dirs[:] = [d for d in dirs if not any(skip in os.path.join(rel_path, d) for skip in skip_files)]
            
            # Create directory structure
            if rel_path != '.':
                dest_dir = rel_path
                os.makedirs(dest_dir, exist_ok=True)
            
            # Copy files
            for file in files:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(rel_path, file) if rel_path != '.' else file
                
                # Skip files in skip list
                if any(skip in dest_file for skip in skip_files):
                    continue
                
                try:
                    shutil.copy2(source_file, dest_file)
                    self.logger.info(f"Updated: {dest_file}")
                except Exception as e:
                    self.logger.warning(f"Could not update {dest_file}: {e}")
    
    def _update_version_info(self):
        """Update version information"""
        try:
            # Try to read new version from extracted files
            if os.path.exists('VERSION'):
                with open('VERSION', 'r') as f:
                    new_version = f.read().strip()
                    self.current_version = new_version
                    self.logger.info(f"Updated to version: {new_version}")
        except Exception as e:
            self.logger.warning(f"Could not update version info: {e}")
    
    def _run_post_update_tasks(self):
        """Run post-update tasks"""
        try:
            # Set file permissions
            script_files = ['scripts/install.sh', 'scripts/start.sh', 'main.py']
            for script in script_files:
                if os.path.exists(script):
                    os.chmod(script, 0o755)
            
            # Install new dependencies if requirements.txt changed
            if os.path.exists('requirements.txt'):
                self.logger.info("📦 Updating dependencies...")
                try:
                    subprocess.run([
                        sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
                    ], check=True, capture_output=True)
                    self.logger.success("✅ Dependencies updated")
                except subprocess.CalledProcessError as e:
                    self.logger.warning(f"Dependency update failed: {e}")
            
        except Exception as e:
            self.logger.warning(f"Post-update tasks failed: {e}")
    
    def _restore_backup(self, backup_path):
        """Restore from backup"""
        if not os.path.exists(backup_path):
            raise Exception(f"Backup path not found: {backup_path}")
        
        # Restore files from backup
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                backup_file = os.path.join(root, file)
                rel_path = os.path.relpath(backup_file, backup_path)
                dest_file = rel_path
                
                try:
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    shutil.copy2(backup_file, dest_file)
                except Exception as e:
                    self.logger.warning(f"Could not restore {dest_file}: {e}")
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.logger.info("🧹 Cleanup completed")
        except Exception as e:
            self.logger.warning(f"Cleanup failed: {e}")
    
    def auto_update_check(self):
        """Automatic update check (background)"""
        if not self.config.get('auto_check', True):
            return
        
        def check_worker():
            try:
                update_info = self.check_for_updates()
                
                if update_info and update_info.get('available'):
                    self.logger.info("🆕 Automatic update available!")
                    
                    if self.config.get('update_notifications', True):
                        self._show_update_notification(update_info)
                    
                    if self.config.get('auto_download', False):
                        self.logger.info("⬇️ Auto-downloading update...")
                        zip_path = self.download_update(update_info)
                        
                        if zip_path and self.config.get('auto_install', False):
                            self.logger.info("🚀 Auto-installing update...")
                            backup_path = self.create_backup() if self.config.get('backup_before_update', True) else None
                            self.install_update(zip_path, backup_path)
                
            except Exception as e:
                self.logger.error(f"Auto-update check failed: {e}")
        
        # Run in background thread
        thread = threading.Thread(target=check_worker, daemon=True)
        thread.start()
    
    def _show_update_notification(self, update_info):
        """Show update notification"""
        print("\n" + "="*60)
        print("🆕 UPDATE AVAILABLE!")
        print("="*60)
        print(f"Current Version: {update_info['current_version']}")
        print(f"Latest Version:  {update_info['latest_version']}")
        print(f"Published:       {update_info['published_date']}")
        print("\nTo update manually, run:")
        print("   python3 scripts/auto_update.py --update")
        print("="*60)
    
    def configure_updates(self, **kwargs):
        """Configure update settings"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                self.logger.info(f"Updated setting: {key} = {value}")
            else:
                self.logger.warning(f"Unknown setting: {key}")
        
        self._save_update_config(self.config)
    
    def list_backups(self):
        """List available backups"""
        if not os.path.exists(self.backup_dir):
            self.logger.info("No backups found")
            return []
        
        backups = []
        for item in os.listdir(self.backup_dir):
            backup_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(backup_path):
                stat = os.stat(backup_path)
                backups.append({
                    'name': item,
                    'path': backup_path,
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'size': self._get_dir_size(backup_path)
                })
        
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    def _get_dir_size(self, path):
        """Get directory size"""
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total += os.path.getsize(filepath)
        except Exception:
            pass
        return total
    
    def rollback_update(self, backup_name=None):
        """Rollback to a previous version"""
        backups = self.list_backups()
        
        if not backups:
            self.logger.error("No backups available for rollback")
            return False
        
        # Use latest backup if none specified
        if not backup_name:
            backup_to_restore = backups[0]
        else:
            backup_to_restore = next((b for b in backups if b['name'] == backup_name), None)
            if not backup_to_restore:
                self.logger.error(f"Backup not found: {backup_name}")
                return False
        
        self.logger.info(f"🔄 Rolling back to: {backup_to_restore['name']}")
        
        try:
            # Create current state backup before rollback
            current_backup = self.create_backup()
            
            # Restore from backup
            self._restore_backup(backup_to_restore['path'])
            
            # Update version info
            self._update_version_info()
            
            self.logger.success("✅ Rollback completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Rollback failed: {e}")
            return False

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(
        description="DDOS Educational Toolkit Auto-Update System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/auto_update.py --check
  python3 scripts/auto_update.py --update
  python3 scripts/auto_update.py --configure auto_check=true
  python3 scripts/auto_update.py --list-backups
  python3 scripts/auto_update.py --rollback
        """
    )
    
    parser.add_argument('--check', action='store_true', help='Check for updates')
    parser.add_argument('--update', action='store_true', help='Download and install updates')
    parser.add_argument('--download-only', action='store_true', help='Download update without installing')
    parser.add_argument('--configure', nargs='*', help='Configure update settings (key=value)')
    parser.add_argument('--list-backups', action='store_true', help='List available backups')
    parser.add_argument('--rollback', nargs='?', const='', help='Rollback to backup (specify backup name or latest)')
    parser.add_argument('--cleanup', action='store_true', help='Clean up temporary files')
    parser.add_argument('--force', action='store_true', help='Force operation')
    parser.add_argument('--version', action='store_true', help='Show current version')
    
    args = parser.parse_args()
    
    # Initialize updater
    updater = AutoUpdater()
    
    try:
        if args.version:
            print(f"Current version: {updater.current_version}")
            
        elif args.check:
            update_info = updater.check_for_updates(force=args.force)
            if update_info:
                if update_info.get('available'):
                    print(f"✅ Update available: {update_info['latest_version']}")
                    print(f"Release notes:\n{update_info['release_notes'][:200]}...")
                else:
                    print("✅ You have the latest version")
            
        elif args.update:
            update_info = updater.check_for_updates(force=True)
            if update_info and update_info.get('available'):
                # Create backup
                backup_path = updater.create_backup()
                
                # Download update
                zip_path = updater.download_update(update_info)
                if zip_path:
                    # Install update
                    success = updater.install_update(zip_path, backup_path)
                    if success:
                        print("🎉 Update completed successfully!")
                    else:
                        print("❌ Update failed")
                        sys.exit(1)
            else:
                print("No updates available")
                
        elif args.download_only:
            update_info = updater.check_for_updates(force=True)
            if update_info and update_info.get('available'):
                zip_path = updater.download_update(update_info)
                if zip_path:
                    print(f"✅ Update downloaded to: {zip_path}")
                else:
                    print("❌ Download failed")
                    sys.exit(1)
            
        elif args.configure:
            if args.configure:
                settings = {}
                for setting in args.configure:
                    if '=' in setting:
                        key, value = setting.split('=', 1)
                        # Convert string values to appropriate types
                        if value.lower() in ('true', 'false'):
                            value = value.lower() == 'true'
                        elif value.isdigit():
                            value = int(value)
                        settings[key] = value
                
                updater.configure_updates(**settings)
                print("✅ Configuration updated")
            else:
                print("Current configuration:")
                for key, value in updater.config.items():
                    print(f"  {key}: {value}")
        
        elif args.list_backups:
            backups = updater.list_backups()
            if backups:
                print("Available backups:")
                for backup in backups:
                    size_mb = backup['size'] / (1024 * 1024)
                    print(f"  {backup['name']} ({size_mb:.1f}MB) - {backup['created']}")
            else:
                print("No backups found")
        
        elif args.rollback is not None:
            backup_name = args.rollback if args.rollback else None
            success = updater.rollback_update(backup_name)
            if not success:
                sys.exit(1)
        
        elif args.cleanup:
            updater.cleanup()
            
        else:
            # Default: check for updates if auto-check is enabled
            updater.auto_update_check()
            print(f"DDOS Educational Toolkit Auto-Updater v{updater.current_version}")
            print("Use --help for available options")
    
    finally:
        # Always cleanup
        if not args.download_only:  # Keep downloaded files if download-only
            updater.cleanup()

if __name__ == "__main__":
    main()
