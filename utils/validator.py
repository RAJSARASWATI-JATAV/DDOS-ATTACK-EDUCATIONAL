#!/usr/bin/env python3
"""
✅ Input Validator
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import re
import socket
import ipaddress
from urllib.parse import urlparse
from colorama import Fore, Style

class InputValidator:
    """Advanced Input Validation System"""
    
    def __init__(self):
        self.ip_pattern = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        self.domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)$'
        )
    
    def validate_target(self, target):
        """Validate target IP or domain"""
        if not target:
            return False
        
        # Remove protocol if present
        if target.startswith(('http://', 'https://')):
            parsed = urlparse(target)
            target = parsed.hostname or parsed.netloc
        
        # Check if it's a valid IP
        if self.validate_ip(target):
            return True
        
        # Check if it's a valid domain
        if self.validate_domain(target):
            return True
        
        return False
    
    def validate_ip(self, ip):
        """Validate IP address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def validate_domain(self, domain):
        """Validate domain name"""
        if len(domain) > 253:
            return False
        
        if domain[-1] == '.':
            domain = domain[:-1]
        
        return bool(self.domain_pattern.match(domain))
    
    def validate_port(self, port):
        """Validate port number"""
        try:
            port = int(port)
            return 1 <= port <= 65535
        except (ValueError, TypeError):
            return False
    
    def validate_threads(self, threads):
        """Validate thread count"""
        if isinstance(threads, str) and threads.lower() == 'unlimited':
            return True
        
        try:
            threads = int(threads)
            return threads > 0
        except (ValueError, TypeError):
            return False
    
    def validate_duration(self, duration):
        """Validate attack duration"""
        try:
            duration = int(duration)
            return 1 <= duration <= 3600  # Max 1 hour
        except (ValueError, TypeError):
            return False
    
    def is_local_target(self, target):
        """Check if target is local/private"""
        try:
            ip = ipaddress.ip_address(target)
            return ip.is_private or ip.is_loopback
        except ValueError:
            # If it's a domain, try to resolve it
            try:
                resolved_ip = socket.gethostbyname(target)
                ip = ipaddress.ip_address(resolved_ip)
                return ip.is_private or ip.is_loopback
            except (socket.gaierror, ValueError):
                return False
    
    def get_validation_message(self, field, value):
        """Get validation error message"""
        messages = {
            'target': f"Invalid target '{value}'. Please provide a valid IP address or domain name.",
            'port': f"Invalid port '{value}'. Port must be between 1 and 65535.",
            'threads': f"Invalid thread count '{value}'. Use a positive number or 'unlimited'.",
            'duration': f"Invalid duration '{value}'. Duration must be between 1 and 3600 seconds."
        }
        return messages.get(field, f"Invalid value for {field}: {value}")