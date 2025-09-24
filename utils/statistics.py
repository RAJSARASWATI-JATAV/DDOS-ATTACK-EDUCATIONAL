#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Statistics Module
Author: Rajsaraswati Jatav
Purpose: Real-time performance monitoring and analytics
"""

import time
import threading
from collections import defaultdict, deque
from datetime import datetime

class Statistics:
    def __init__(self):
        self.attack_stats = {}
        self.global_stats = {
            'total_attacks': 0,
            'total_requests': 0,
            'total_errors': 0,
            'start_time': time.time()
        }
        self.lock = threading.Lock()
        
    def start_tracking(self, attack_id):
        """Start tracking statistics for an attack"""
        with self.lock:
            self.attack_stats[attack_id] = {
                'start_time': time.time(),
                'end_time': None,
                'requests_sent': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'bytes_sent': 0,
                'errors': defaultdict(int),
                'response_times': deque(maxlen=1000),
                'requests_per_second': deque(maxlen=60),
                'last_request_time': time.time(),
                'status': 'running'
            }
            self.global_stats['total_attacks'] += 1
    
    def stop_tracking(self, attack_id):
        """Stop tracking statistics for an attack"""
        with self.lock:
            if attack_id in self.attack_stats:
                self.attack_stats[attack_id]['end_time'] = time.time()
                self.attack_stats[attack_id]['status'] = 'completed'
    
    def record_request(self, attack_id, success=True, response_time=None, bytes_sent=0):
        """Record a request attempt"""
        current_time = time.time()
        
        with self.lock:
            if attack_id not in self.attack_stats:
                return
            
            stats = self.attack_stats[attack_id]
            stats['requests_sent'] += 1
            stats['last_request_time'] = current_time
            stats['bytes_sent'] += bytes_sent
            
            if success:
                stats['successful_requests'] += 1
            else:
                stats['failed_requests'] += 1
            
            if response_time:
                stats['response_times'].append(response_time)
            
            self.global_stats['total_requests'] += 1
            if not success:
                self.global_stats['total_errors'] += 1
    
    def record_error(self, attack_id, error_type):
        """Record an error"""
        with self.lock:
            if attack_id in self.attack_stats:
                self.attack_stats[attack_id]['errors'][error_type] += 1
                self.attack_stats[attack_id]['failed_requests'] += 1
                self.global_stats['total_errors'] += 1
    
    def get_attack_stats(self, attack_id):
        """Get statistics for a specific attack"""
        with self.lock:
            if attack_id not in self.attack_stats:
                return None
            
            stats = self.attack_stats[attack_id].copy()
            
            duration = (stats['end_time'] or time.time()) - stats['start_time']
            stats['duration'] = duration
            stats['requests_per_second_avg'] = stats['requests_sent'] / duration if duration > 0 else 0
            stats['success_rate'] = (stats['successful_requests'] / stats['requests_sent'] * 100) if stats['requests_sent'] > 0 else 0
            
            if stats['response_times']:
                response_times = list(stats['response_times'])
                stats['avg_response_time'] = sum(response_times) / len(response_times)
                stats['min_response_time'] = min(response_times)
                stats['max_response_time'] = max(response_times)
            else:
                stats['avg_response_time'] = 0
                stats['min_response_time'] = 0
                stats['max_response_time'] = 0
            
            return stats
    
    def get_global_stats(self):
        """Get global application statistics"""
        with self.lock:
            current_time = time.time()
            uptime = current_time - self.global_stats['start_time']
            
            active_attacks = sum(1 for stats in self.attack_stats.values() 
                               if stats['status'] == 'running')
            
            total_bytes_sent = sum(stats['bytes_sent'] for stats in self.attack_stats.values())
            
            return {
                'uptime': uptime,
                'active_attacks': active_attacks,
                'total_attacks': self.global_stats['total_attacks'],
                'total_requests': self.global_stats['total_requests'],
                'total_errors': self.global_stats['total_errors'],
                'total_bytes_sent': total_bytes_sent,
                'success_rate': ((self.global_stats['total_requests'] - self.global_stats['total_errors']) / 
                               self.global_stats['total_requests'] * 100) if self.global_stats['total_requests'] > 0 else 0,
                'requests_per_second': self.global_stats['total_requests'] / uptime if uptime > 0 else 0
            }
