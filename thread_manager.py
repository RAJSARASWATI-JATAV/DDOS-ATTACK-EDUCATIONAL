#!/usr/bin/env python3
"""
🧵 Thread Manager - Unlimited Threading System
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import threading
import time
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

class ThreadManager:
    """Advanced Thread Management System"""
    
    def __init__(self, max_threads='unlimited'):
        self.max_threads = self._calculate_max_threads(max_threads)
        self.active_threads = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.thread_pool = None
        self.lock = threading.Lock()
        
    def _calculate_max_threads(self, max_threads):
        """Calculate optimal thread count"""
        if max_threads == 'unlimited':
            # Use CPU cores * 200 for maximum performance
            cpu_count = psutil.cpu_count()
            return cpu_count * 200
        elif isinstance(max_threads, int):
            return max_threads
        else:
            return 1000  # Default
    
    def start_thread_pool(self):
        """Initialize thread pool"""
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_threads)
        print(f"{Fore.GREEN}🚀 Thread pool started with {self.max_threads} max threads{Style.RESET_ALL}")
    
    def submit_task(self, func, *args, **kwargs):
        """Submit task to thread pool"""
        if not self.thread_pool:
            self.start_thread_pool()
        
        with self.lock:
            self.active_threads += 1
        
        future = self.thread_pool.submit(self._task_wrapper, func, *args, **kwargs)
        return future
    
    def _task_wrapper(self, func, *args, **kwargs):
        """Wrapper for task execution with error handling"""
        try:
            result = func(*args, **kwargs)
            with self.lock:
                self.completed_tasks += 1
            return result
        except Exception as e:
            with self.lock:
                self.failed_tasks += 1
            return None
        finally:
            with self.lock:
                self.active_threads -= 1
    
    def get_stats(self):
        """Get thread statistics"""
        return {
            'max_threads': self.max_threads,
            'active_threads': self.active_threads,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'total_tasks': self.completed_tasks + self.failed_tasks
        }
    
    def shutdown(self, wait=True):
        """Shutdown thread pool"""
        if self.thread_pool:
            self.thread_pool.shutdown(wait=wait)
            print(f"{Fore.YELLOW}🔄 Thread pool shutdown{Style.RESET_ALL}")