#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Network Scanner
Author: Rajsaraswati Jatav
Purpose: Target reconnaissance and analysis
"""

import socket
import threading
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor
from utils.logger import Logger

class NetworkScanner:
    def __init__(self):
        self.logger = Logger()
        self.open_ports = []
        self.services = {}
        self.vulnerabilities = []
        
    def ping_host(self, target):
        """Check if host is alive"""
        try:
            if subprocess.call(['ping', '-c', '1', target], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL) == 0:
                return True
        except:
            pass
        return False
    
    def port_scan(self, target, ports=None, threads=50):
        """Scan ports on target"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080]
        
        self.logger.info(f"Scanning {len(ports)} ports on {target}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(self._scan_port, target, port): port for port in ports}
            
            for future in futures:
                port = futures[future]
                try:
                    if future.result():
                        self.open_ports.append(port)
                        self.logger.info(f"Port {port} is open on {target}")
                except Exception as e:
                    self.logger.error(f"Error scanning port {port}: {e}")
        
        return self.open_ports
    
    def _scan_port(self, target, port):
        """Scan individual port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def service_detection(self, target, port):
        """Detect service running on port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            
            if port in [80, 443, 8080]:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                service = self._parse_http_banner(banner)
            else:
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                service = self._parse_service_banner(banner, port)
            
            sock.close()
            self.services[port] = service
            return service
            
        except Exception as e:
            self.logger.error(f"Service detection failed for {target}:{port} - {e}")
            return "Unknown"
    
    def comprehensive_scan(self, target):
        """Run complete reconnaissance"""
        results = {
            'target': target,
            'alive': False,
            'open_ports': [],
            'services': {},
            'vulnerabilities': []
        }
        
        results['alive'] = self.ping_host(target)
        
        if results['alive']:
            results['open_ports'] = self.port_scan(target)
            
            for port in results['open_ports']:
                service = self.service_detection(target, port)
                results['services'][port] = service
        
        return results
