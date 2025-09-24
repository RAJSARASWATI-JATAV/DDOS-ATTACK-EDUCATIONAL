#!/usr/bin/env python3
"""
📊 Performance Monitor - Real-time System Monitoring
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import time
import threading
import psutil
from collections import deque
from colorama import Fore, Style

class PerformanceMonitor:
    """Real-time Performance Monitoring System"""
    
    def __init__(self):
        self.monitoring = False
        self.start_time = None
        self.monitor_thread = None
        
        # Statistics
        self.requests_sent = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.active_threads = 0
        
        # Performance data (last 60 seconds)
        self.request_history = deque(maxlen=60)
        self.cpu_history = deque(maxlen=60)
        self.memory_history = deque(maxlen=60)
        
        # System info
        self.cpu_count = psutil.cpu_count()
        self.memory_total = psutil.virtual_memory().total
        
    def start_monitoring(self):
        """Start performance monitoring"""
        self.monitoring = True
        self.start_time = time.time()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"{Fore.GREEN}📊 Performance monitoring started{Style.RESET_ALL}")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print(f"{Fore.YELLOW}📊 Performance monitoring stopped{Style.RESET_ALL}")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Store metrics
                self.cpu_history.append(cpu_percent)
                self.memory_history.append(memory.percent)
                
                # Calculate request rate
                current_time = time.time()
                if len(self.request_history) > 0:
                    time_diff = current_time - self.request_history[-1]['time']
                    if time_diff > 0:
                        request_rate = self.requests_sent / time_diff
                    else:
                        request_rate = 0
                else:
                    request_rate = 0
                
                self.request_history.append({
                    'time': current_time,
                    'requests': self.requests_sent,
                    'rate': request_rate
                })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"{Fore.RED}Monitoring error: {e}{Style.RESET_ALL}")
    
    def get_stats(self):
        """Get current statistics"""
        current_time = time.time()
        duration = current_time - self.start_time if self.start_time else 0
        
        # Calculate rates
        requests_per_second = self.requests_sent / duration if duration > 0 else 0
        success_rate = (self.successful_requests / self.requests_sent * 100) if self.requests_sent > 0 else 0
        
        # System metrics
        cpu_usage = self.cpu_history[-1] if self.cpu_history else 0
        memory_usage = self.memory_history[-1] if self.memory_history else 0
        
        return {
            'requests_sent': self.requests_sent,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'active_threads': self.active_threads,
            'requests_per_second': round(requests_per_second, 2),
            'success_rate': round(success_rate, 2),
            'duration': round(duration, 2),
            'cpu_usage': round(cpu_usage, 2),
            'memory_usage': round(memory_usage, 2),
            'cpu_count': self.cpu_count
        }
    
    def get_final_stats(self):
        """Get final comprehensive statistics"""
        stats = self.get_stats()
        
        # Calculate averages
        avg_cpu = sum(self.cpu_history) / len(self.cpu_history) if self.cpu_history else 0
        avg_memory = sum(self.memory_history) / len(self.memory_history) if self.memory_history else 0
        
        # Calculate peak values
        peak_cpu = max(self.cpu_history) if self.cpu_history else 0
        peak_memory = max(self.memory_history) if self.memory_history else 0
        
        # Request rate analysis
        request_rates = [r['rate'] for r in self.request_history if 'rate' in r]
        peak_rate = max(request_rates) if request_rates else 0
        avg_rate = sum(request_rates) / len(request_rates) if request_rates else 0
        
        stats.update({
            'total_requests': self.requests_sent,
            'peak_speed': round(peak_rate, 2),
            'avg_speed': round(avg_rate, 2)
        })
        
        return stats