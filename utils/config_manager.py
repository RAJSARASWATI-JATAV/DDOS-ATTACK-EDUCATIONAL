#!/usr/bin/env python3
"""
⚙️ Configuration Manager
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import json
import os
from colorama import Fore, Style

class ConfigManager:
    """Advanced Configuration Management System"""
    
    def __init__(self, config_file='config/settings.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not load config, using defaults: {e}{Style.RESET_ALL}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            'application': {
                'name': 'DDOS Attack Educational Toolkit',
                'version': '1.0.0',
                'author': 'Rajsaraswati Jatav'
            },
            'attack_settings': {
                'default_threads': 1000,
                'max_threads': 'unlimited',
                'default_duration': 60,
                'default_port': 80,
                'timeout': 5
            },
            'interface': {
                'sound_effects': True,
                'visual_effects': True,
                'colored_output': True
            }
        }
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error saving config: {e}{Style.RESET_ALL}")
            return False