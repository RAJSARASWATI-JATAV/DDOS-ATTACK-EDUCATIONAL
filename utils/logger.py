#!/usr/bin/env python3
"""
📝 Logger - Advanced Logging System
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import logging
import os
from datetime import datetime
from colorama import Fore, Style

class Logger:
    """Advanced Logging System with File and Console Output"""
    
    def __init__(self, name='DDOS_TOOLKIT', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create logs directory if not exists
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # File handler
        log_file = f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    def error(self, message):
        """Log error message"""
        self.logger.error(f"{Fore.RED}{message}{Style.RESET_ALL}")
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(f"{Fore.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}")