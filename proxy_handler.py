#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Proxy Handler
Author: Rajsaraswati Jatav
Purpose: Proxy management and rotation system
"""

import random
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from utils.logger import Logger

class ProxyHandler:
    def __init__(self):
        self.logger = Logger()
        self.proxy_list = []
        self.working_proxies = []
        self.proxy_stats = {}
        self.current_proxy_index = 0
        self.lock = threading.Lock()
        
    def load_proxies(self, file_path='config/proxies.txt'):
        """Load proxies from file"""
        try:
            with open(file_path, 'r') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            
            self.proxy_list = []
            for proxy in proxies:
                if ':' in proxy and not proxy.startswith('#'):
                    self.proxy_list.append(proxy)
            
            self.logger.info(f"Loaded {len(self.proxy_list)} proxies from {file_path}")
            return True
            
        except FileNotFoundError:
            self.logger.error(f"Proxy file not found: {file_path}")
            return False
    
    def test_proxy(self, proxy, timeout=10):
        """Test if proxy is working"""
        try:
            proxy_dict = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            
            response = requests.get('http://httpbin.org/ip', 
                                  proxies=proxy_dict, 
                                  timeout=timeout)
            
            if response.status_code == 200:
                response_time = response.elapsed.total_seconds()
                return True, response_time
            else:
                return False, None
                
        except Exception as e:
            self.logger.debug(f"Proxy {proxy} failed: {e}")
            return False, None
    
    def validate_proxies(self, max_workers=50):
        """Validate all loaded proxies"""
        self.logger.info("Validating proxies...")
        self.working_proxies = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {
                executor.submit(self.test_proxy, proxy): proxy 
                for proxy in self.proxy_list
            }
            
            for future in future_to_proxy:
                proxy = future_to_proxy[future]
                try:
                    is_working, response_time = future.result()
                    if is_working:
                        self.working_proxies.append(proxy)
                        self.proxy_stats[proxy] = {
                            'response_time': response_time,
                            'success_count': 0,
                            'error_count': 0,
                            'last_used': None
                        }
                except Exception as e:
                    self.logger.error(f"Error testing proxy {proxy}: {e}")
        
        self.logger.info(f"Found {len(self.working_proxies)} working proxies")
        return len(self.working_proxies)
    
    def get_next_proxy(self):
        """Get next proxy in rotation"""
        if not self.working_proxies:
            return None
            
        with self.lock:
            proxy = self.working_proxies[self.current_proxy_index]
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.working_proxies)
            self.proxy_stats[proxy]['last_used'] = time.time()
            return proxy
    
    def get_random_proxy(self):
        """Get random proxy from working list"""
        if not self.working_proxies:
            return None
        
        proxy = random.choice(self.working_proxies)
        self.proxy_stats[proxy]['last_used'] = time.time()
        return proxy
    
    def create_proxy_dict(self, proxy):
        """Create proxy dictionary for requests"""
        if not proxy:
            return None
            
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
    
    def get_proxy_statistics(self):
        """Get proxy usage statistics"""
        total_proxies = len(self.proxy_list)
        working_proxies = len(self.working_proxies)
        
        if not self.proxy_stats:
            return {
                'total_loaded': total_proxies,
                'working_proxies': working_proxies,
                'success_rate': 0,
                'average_response_time': 0
            }
        
        total_success = sum(stats['success_count'] for stats in self.proxy_stats.values())
        total_errors = sum(stats['error_count'] for stats in self.proxy_stats.values())
        total_requests = total_success + total_errors
        
        avg_response_time = sum(stats['response_time'] for stats in self.proxy_stats.values()) / len(self.proxy_stats)
        
        return {
            'total_loaded': total_proxies,
            'working_proxies': working_proxies,
            'total_requests': total_requests,
            'successful_requests': total_success,
            'failed_requests': total_errors,
            'success_rate': (total_success / total_requests * 100) if total_requests > 0 else 0,
            'average_response_time': avg_response_time
        }
