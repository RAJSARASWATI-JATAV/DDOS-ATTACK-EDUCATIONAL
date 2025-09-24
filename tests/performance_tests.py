#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Performance Testing Suite
Author: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
Purpose: Comprehensive performance benchmarking and load testing

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import unittest
import time
import threading
import psutil
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os
import json
import memory_profiler
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import modules for testing
from attack_modules import AttackController
from utils.statistics import Statistics
from utils.logger import Logger
from proxy_handler import ProxyHandler
from payload_generator import PayloadGenerator

class PerformanceTestBase(unittest.TestCase):
    """Base class for performance tests"""
    
    def setUp(self):
        """Set up performance test environment"""
        self.start_time = time.time()
        self.initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.initial_cpu = psutil.cpu_percent(interval=1)
        
        # Performance thresholds
        self.max_memory_usage_mb = 500  # Maximum memory usage
        self.max_cpu_usage_percent = 95  # Maximum CPU usage
        self.max_response_time_ms = 1000  # Maximum response time
        self.min_throughput_rps = 10  # Minimum requests per second
        
        print(f"🚀 Starting performance test: {self._testMethodName}")
        print(f"📊 Initial Memory: {self.initial_memory:.2f} MB")
        print(f"🖥️ Initial CPU: {self.initial_cpu:.1f}%")
    
    def tearDown(self):
        """Clean up and report performance metrics"""
        end_time = time.time()
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        final_cpu = psutil.cpu_percent(interval=1)
        
        execution_time = end_time - self.start_time
        memory_delta = final_memory - self.initial_memory
        
        print(f"\n📈 Performance Results for {self._testMethodName}:")
        print(f"⏱️ Execution Time: {execution_time:.2f} seconds")
        print(f"💾 Memory Usage: {memory_delta:+.2f} MB (Final: {final_memory:.2f} MB)")
        print(f"🖥️ CPU Usage: {final_cpu:.1f}%")
        
        # Performance assertions
        if memory_delta > self.max_memory_usage_mb:
            self.fail(f"Memory usage exceeded threshold: {memory_delta:.2f} MB > {self.max_memory_usage_mb} MB")
        
        if final_cpu > self.max_cpu_usage_percent:
            print(f"⚠️ Warning: CPU usage high: {final_cpu:.1f}%")

class TestThreadingPerformance(PerformanceTestBase):
    """Test threading performance and scalability"""
    
    def test_thread_creation_performance(self):
        """Test thread creation and management performance"""
        thread_counts = [10, 50, 100, 500, 1000]
        results = {}
        
        for thread_count in thread_counts:
            start_time = time.time()
            
            # Create and manage threads
            threads = []
            for i in range(thread_count):
                thread = threading.Thread(target=self._dummy_work, args=(0.001,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            end_time = time.time()
            execution_time = end_time - start_time
            results[thread_count] = execution_time
            
            print(f"📊 {thread_count} threads: {execution_time:.3f}s")
        
        # Performance assertions
        self.assertLess(results[100], 2.0, "100 threads should complete within 2 seconds")
        self.assertLess(results[500], 10.0, "500 threads should complete within 10 seconds")
        
        return results
    
    def test_thread_pool_performance(self):
        """Test thread pool executor performance"""
        task_counts = [100, 500, 1000, 2000]
        results = {}
        
        for task_count in task_counts:
            start_time = time.time()
            
            # Use thread pool executor
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(self._dummy_work, 0.001) for _ in range(task_count)]
                
                # Wait for completion
                for future in as_completed(futures):
                    future.result()
            
            end_time = time.time()
            execution_time = end_time - start_time
            results[task_count] = execution_time
            
            print(f"📊 {task_count} tasks: {execution_time:.3f}s")
        
        # Calculate throughput
        throughput = task_counts[-1] / results[task_counts[-1]]
        print(f"🚀 Throughput: {throughput:.1f} tasks/second")
        
        self.assertGreater(throughput, 100, "Should achieve > 100 tasks/second")
        
        return results
    
    def test_concurrent_attack_performance(self):
        """Test performance with multiple concurrent attacks"""
        with patch('socket.socket') as mock_socket:
            mock_sock = Mock()
            mock_socket.return_value = mock_sock
            mock_sock.connect.return_value = None
            mock_sock.send.return_value = 100
            mock_sock.recv.return_value = b'HTTP/1.1 200 OK\r\n\r\n'
            mock_sock.close.return_value = None
            
            controller = AttackController()
            attack_ids = []
            
            start_time = time.time()
            
            # Start multiple attacks simultaneously
            for i in range(5):
                attack_id = controller.start_attack(
                    attack_type='http_flood',
                    target='127.0.0.1',
                    threads=20,
                    duration=2
                )
                if attack_id:
                    attack_ids.append(attack_id)
            
            # Wait for attacks to complete
            time.sleep(3)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"📊 {len(attack_ids)} concurrent attacks: {execution_time:.3f}s")
            
            # Stop any remaining attacks
            for attack_id in attack_ids:
                controller.stop_attack(attack_id)
        
        self.assertLess(execution_time, 5.0, "Concurrent attacks should complete efficiently")
    
    def _dummy_work(self, duration):
        """Dummy work function for testing"""
        time.sleep(duration)
        return True

class TestMemoryPerformance(PerformanceTestBase):
    """Test memory usage and efficiency"""
    
    @memory_profiler.profile
    def test_memory_usage_scaling(self):
        """Test memory usage with increasing load"""
        thread_counts = [10, 50, 100, 500]
        memory_usage = {}
        
        for thread_count in thread_counts:
            # Measure memory before
            memory_before = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Create mock attack controller
            controller = AttackController()
            
            # Simulate thread creation
            threads = []
            for i in range(thread_count):
                thread = threading.Thread(target=self._memory_intensive_work)
                threads.append(thread)
                thread.start()
            
            # Measure peak memory
            peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Clean up
            for thread in threads:
                thread.join()
            
            memory_delta = peak_memory - memory_before
            memory_usage[thread_count] = memory_delta
            
            print(f"📊 {thread_count} threads: {memory_delta:.2f} MB")
        
        # Test memory efficiency
        memory_per_thread = memory_usage[100] / 100
        print(f"💾 Memory per thread: {memory_per_thread:.3f} MB")
        
        self.assertLess(memory_per_thread, 5.0, "Memory per thread should be < 5 MB")
    
    def test_memory_leak_detection(self):
        """Test for memory leaks in repeated operations"""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_readings = []
        
        # Perform repeated operations
        for iteration in range(10):
            # Simulate attack operations
            controller = AttackController()
            stats = Statistics()
            
            # Create and destroy objects
            for i in range(100):
                attack_id = f"test_attack_{i}"
                stats.start_tracking(attack_id)
                stats.record_request(attack_id, success=True, bytes_sent=1000)
                stats.stop_tracking(attack_id)
            
            # Measure memory
            current_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_readings.append(current_memory)
            
            print(f"🔄 Iteration {iteration + 1}: {current_memory:.2f} MB")
            
            # Force garbage collection
            import gc
            gc.collect()
        
        # Analyze memory trend
        memory_trend = statistics.linear_regression_slope(range(len(memory_readings)), memory_readings)
        print(f"📈 Memory trend: {memory_trend:.3f} MB/iteration")
        
        # Should not have significant memory leak
        self.assertLess(abs(memory_trend), 1.0, "Memory leak detected: trend > 1 MB/iteration")
    
    def _memory_intensive_work(self):
        """Memory intensive work for testing"""
        # Create some data structures
        data = []
        for i in range(1000):
            data.append({'id': i, 'data': 'x' * 100})
        
        # Simulate work
        time.sleep(0.1)
        
        # Clean up
        del data

class TestNetworkPerformance(PerformanceTestBase):
    """Test network-related performance"""
    
    def test_connection_performance(self):
        """Test connection establishment performance"""
        connection_counts = [10, 50, 100, 200]
        results = {}
        
        for count in connection_counts:
            with patch('socket.socket') as mock_socket:
                mock_sock = Mock()
                mock_socket.return_value = mock_sock
                mock_sock.connect.return_value = None
                mock_sock.close.return_value = None
                
                start_time = time.time()
                
                # Simulate connections
                threads = []
                for i in range(count):
                    thread = threading.Thread(target=self._simulate_connection)
                    threads.append(thread)
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                end_time = time.time()
                execution_time = end_time - start_time
                results[count] = execution_time
                
                connections_per_second = count / execution_time
                print(f"📊 {count} connections: {execution_time:.3f}s ({connections_per_second:.1f} conn/s)")
        
        # Performance assertions
        self.assertGreater(results[100] / 100, 50, "Should achieve > 50 connections/second")
    
    def test_payload_generation_performance(self):
        """Test payload generation performance"""
        generator = PayloadGenerator()
        payload_counts = [100, 500, 1000, 5000]
        results = {}
        
        for count in payload_counts:
            start_time = time.time()
            
            # Generate payloads
            payloads = []
            for i in range(count):
                payload = generator.generate_http_payload('http://example.com')
                payloads.append(payload)
            
            end_time = time.time()
            execution_time = end_time - start_time
            results[count] = execution_time
            
            payloads_per_second = count / execution_time
            print(f"📊 {count} payloads: {execution_time:.3f}s ({payloads_per_second:.1f} payloads/s)")
        
        # Should generate > 1000 payloads per second
        self.assertGreater(results[1000] / 1000, 1000, "Should generate > 1000 payloads/second")
    
    def test_proxy_handling_performance(self):
        """Test proxy handling performance"""
        proxy_handler = ProxyHandler()
        
        # Create test proxy list
        test_proxies = [f"192.168.1.{i}:808{i%10}" for i in range(1, 101)]
        proxy_handler.proxy_list = test_proxies
        proxy_handler.working_proxies = test_proxies
        
        # Initialize stats
        for proxy in test_proxies:
            proxy_handler.proxy_stats[proxy] = {
                'response_time': 0.5,
                'success_count': 0,
                'error_count': 0,
                'last_used': None
            }
        
        # Test proxy rotation performance
        start_time = time.time()
        
        proxy_requests = 10000
        for i in range(proxy_requests):
            proxy = proxy_handler.get_next_proxy()
            self.assertIsNotNone(proxy)
        
        end_time = time.time()
        execution_time = end_time - start_time
        requests_per_second = proxy_requests / execution_time
        
        print(f"📊 Proxy rotation: {requests_per_second:.1f} requests/s")
        
        self.assertGreater(requests_per_second, 10000, "Should handle > 10k proxy requests/second")
    
    def _simulate_connection(self):
        """Simulate network connection"""
        import socket
        try:
            sock = socket.socket()
            # Mock connection work
            time.sleep(0.001)
            sock.close()
        except:
            pass

class TestStatisticsPerformance(PerformanceTestBase):
    """Test statistics and monitoring performance"""
    
    def test_statistics_recording_performance(self):
        """Test performance of statistics recording"""
        stats = Statistics()
        request_counts = [1000, 5000, 10000, 50000]
        results = {}
        
        for count in request_counts:
            attack_id = f"perf_test_{count}"
            stats.start_tracking(attack_id)
            
            start_time = time.time()
            
            # Record requests
            for i in range(count):
                success = (i % 10) != 0  # 90% success rate
                response_time = 0.1 + (i % 100) * 0.001  # Variable response times
                bytes_sent = 1000 + (i % 500)  # Variable bytes
                
                stats.record_request(attack_id, success=success, 
                                   response_time=response_time, bytes_sent=bytes_sent)
            
            end_time = time.time()
            execution_time = end_time - start_time
            results[count] = execution_time
            
            records_per_second = count / execution_time
            print(f"📊 {count} records: {execution_time:.3f}s ({records_per_second:.1f} records/s)")
            
            # Test statistics calculation
            calc_start = time.time()
            attack_stats = stats.get_attack_stats(attack_id)
            calc_time = time.time() - calc_start
            
            print(f"🧮 Statistics calculation: {calc_time:.3f}s")
            
            stats.stop_tracking(attack_id)
        
        # Performance assertions
        self.assertGreater(results[10000] / 10000, 1000, "Should record > 1000 stats/second")
    
    def test_concurrent_statistics_performance(self):
        """Test statistics performance with concurrent access"""
        stats = Statistics()
        thread_count = 50
        requests_per_thread = 1000
        
        def record_stats_worker(worker_id):
            attack_id = f"concurrent_test_{worker_id}"
            stats.start_tracking(attack_id)
            
            for i in range(requests_per_thread):
                stats.record_request(attack_id, success=(i % 5) != 0, 
                                   response_time=0.1, bytes_sent=1000)
            
            stats.stop_tracking(attack_id)
        
        start_time = time.time()
        
        # Start concurrent workers
        threads = []
        for i in range(thread_count):
            thread = threading.Thread(target=record_stats_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        total_requests = thread_count * requests_per_thread
        requests_per_second = total_requests / execution_time
        
        print(f"📊 Concurrent stats: {requests_per_second:.1f} requests/s")
        print(f"🔄 {thread_count} threads, {requests_per_thread} requests each")
        
        # Verify data integrity
        global_stats = stats.get_global_stats()
        self.assertEqual(global_stats['total_attacks'], thread_count)
        
        self.assertGreater(requests_per_second, 5000, "Should handle > 5000 concurrent requests/s")

class TestLoadScalability(PerformanceTestBase):
    """Test system scalability under load"""
    
    def test_thread_scalability(self):
        """Test scalability with increasing thread count"""
        thread_counts = [10, 50, 100, 200, 500, 1000]
        performance_data = {}
        
        for thread_count in thread_counts:
            print(f"\n🧪 Testing scalability with {thread_count} threads")
            
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            start_time = time.time()
            
            # Simulate workload
            completed_tasks = self._simulate_workload(thread_count, task_duration=0.01)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            execution_time = end_time - start_time
            memory_used = end_memory - start_memory
            throughput = completed_tasks / execution_time
            
            performance_data[thread_count] = {
                'execution_time': execution_time,
                'memory_used': memory_used,
                'throughput': throughput,
                'completed_tasks': completed_tasks
            }
            
            print(f"📈 Results: {throughput:.1f} tasks/s, {memory_used:.2f} MB")
        
        # Analyze scalability
        self._analyze_scalability(performance_data)
        
        return performance_data
    
    def test_concurrent_attack_scalability(self):
        """Test scalability with multiple concurrent attacks"""
        with patch('socket.socket'):
            attack_counts = [1, 3, 5, 10, 15]
            results = {}
            
            controller = AttackController()
            
            for attack_count in attack_counts:
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                attack_ids = []
                for i in range(attack_count):
                    attack_id = controller.start_attack(
                        attack_type='http_flood',
                        target='127.0.0.1',
                        threads=50,
                        duration=2
                    )
                    if attack_id:
                        attack_ids.append(attack_id)
                
                # Wait for completion
                time.sleep(3)
                
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                # Clean up
                for attack_id in attack_ids:
                    controller.stop_attack(attack_id)
                
                results[attack_count] = {
                    'execution_time': end_time - start_time,
                    'memory_used': end_memory - start_memory,
                    'successful_attacks': len(attack_ids)
                }
                
                print(f"📊 {attack_count} attacks: {results[attack_count]}")
        
        # Verify scalability
        max_attacks = max(attack_counts)
        max_memory = results[max_attacks]['memory_used']
        self.assertLess(max_memory, 200, f"Memory usage should be < 200MB for {max_attacks} attacks")
    
    def _simulate_workload(self, thread_count, task_duration=0.01):
        """Simulate a workload with specified thread count"""
        completed_tasks = 0
        task_lock = threading.Lock()
        
        def worker():
            nonlocal completed_tasks
            time.sleep(task_duration)
            with task_lock:
                completed_tasks += 1
        
        # Create and start threads
        threads = []
        for i in range(thread_count):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        return completed_tasks
    
    def _analyze_scalability(self, performance_data):
        """Analyze scalability performance data"""
        thread_counts = list(performance_data.keys())
        throughputs = [performance_data[tc]['throughput'] for tc in thread_counts]
        memory_usage = [performance_data[tc]['memory_used'] for tc in thread_counts]
        
        print("\n📊 Scalability Analysis:")
        print("Thread Count | Throughput | Memory | Efficiency")
        print("-" * 50)
        
        for i, tc in enumerate(thread_counts):
            efficiency = throughputs[i] / tc  # Tasks per second per thread
            print(f"{tc:11d} | {throughputs[i]:8.1f} | {memory_usage[i]:6.1f} | {efficiency:8.3f}")
        
        # Calculate scalability metrics
        linear_scalability = throughputs[-1] / throughputs[0]
        expected_linear = thread_counts[-1] / thread_counts[0]
        scalability_efficiency = linear_scalability / expected_linear
        
        print(f"\n📈 Scalability Metrics:")
        print(f"Linear Scalability: {linear_scalability:.1f}x")
        print(f"Expected Linear: {expected_linear:.1f}x")
        print(f"Efficiency: {scalability_efficiency:.1f}%")
        
        # Scalability should be reasonable
        self.assertGreater(scalability_efficiency, 0.3, "Scalability efficiency should be > 30%")

class TestSystemResourceUsage(PerformanceTestBase):
    """Test system resource usage optimization"""
    
    def test_cpu_utilization(self):
        """Test CPU utilization efficiency"""
        cpu_before = psutil.cpu_percent(interval=1)
        
        # CPU intensive workload
        start_time = time.time()
        self._cpu_intensive_work(duration=3)
        end_time = time.time()
        
        cpu_after = psutil.cpu_percent(interval=1)
        execution_time = end_time - start_time
        
        print(f"🖥️ CPU Usage: {cpu_before:.1f}% → {cpu_after:.1f}%")
        print(f"⏱️ Execution Time: {execution_time:.2f}s")
        
        # CPU usage should be reasonable
        self.assertLess(cpu_after, 90, "CPU usage should be < 90%")
    
    def test_memory_efficiency(self):
        """Test memory usage efficiency"""
        import gc
        
        # Force garbage collection
        gc.collect()
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Memory intensive operations
        data_structures = self._create_large_data_structures(count=1000)
        peak_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        # Clean up
        del data_structures
        gc.collect()
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        memory_growth = peak_memory - initial_memory
        memory_recovered = peak_memory - final_memory
        recovery_rate = memory_recovered / memory_growth if memory_growth > 0 else 0
        
        print(f"💾 Memory Growth: {memory_growth:.2f} MB")
        print(f"♻️ Memory Recovered: {memory_recovered:.2f} MB ({recovery_rate:.1%})")
        
        # Memory should be properly recovered
        self.assertGreater(recovery_rate, 0.8, "Should recover > 80% of allocated memory")
    
    def test_network_resource_usage(self):
        """Test network resource efficiency"""
        # Monitor network stats before
        net_before = psutil.net_io_counters()
        
        # Simulate network operations
        payload_gen = PayloadGenerator()
        
        start_time = time.time()
        for i in range(1000):
            payload = payload_gen.generate_http_payload('http://example.com')
            # Simulate network send (without actual network)
        
        execution_time = time.time() - start_time
        net_after = psutil.net_io_counters()
        
        # Calculate efficiency
        operations_per_second = 1000 / execution_time
        
        print(f"📡 Network Operations: {operations_per_second:.1f} ops/s")
        print(f"📊 Bytes Sent: {net_after.bytes_sent - net_before.bytes_sent}")
        print(f"📊 Bytes Received: {net_after.bytes_recv - net_before.bytes_recv}")
        
        self.assertGreater(operations_per_second, 100, "Should achieve > 100 network ops/s")
    
    def _cpu_intensive_work(self, duration):
        """CPU intensive work for testing"""
        end_time = time.time() + duration
        result = 0
        
        while time.time() < end_time:
            # CPU intensive calculation
            for i in range(10000):
                result += i ** 2
        
        return result
    
    def _create_large_data_structures(self, count):
        """Create large data structures for memory testing"""
        data = []
        for i in range(count):
            item = {
                'id': i,
                'data': 'x' * 1000,  # 1KB of data per item
                'metadata': {
                    'timestamp': time.time(),
                    'index': i,
                    'extra': list(range(100))
                }
            }
            data.append(item)
        
        return data

def run_performance_tests():
    """Run comprehensive performance test suite"""
    print("🚀 Starting DDOS Educational Toolkit - Performance Test Suite")
    print("=" * 80)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add performance test classes
    test_classes = [
        TestThreadingPerformance,
        TestMemoryPerformance,
        TestNetworkPerformance,
        TestStatisticsPerformance,
        TestLoadScalability,
        TestSystemResourceUsage
    ]
    
    for test_class in test_classes:
        test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=False,  # Show real-time output for performance tests
        failfast=False
    )
    
    start_time = time.time()
    result = runner.run(test_suite)
    total_time = time.time() - start_time
    
    # Print comprehensive summary
    print("\n" + "=" * 80)
    print("🏁 PERFORMANCE TEST SUMMARY")
    print(f"⏱️ Total Execution Time: {total_time:.2f} seconds")
    print(f"🧪 Tests Run: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"🚨 Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ PERFORMANCE FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: Performance threshold not met")
    
    if result.errors:
        print(f"\n🚨 PERFORMANCE ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}: Execution error")
    
    # Overall assessment
    if result.wasSuccessful():
        print(f"\n🎉 ALL PERFORMANCE TESTS PASSED!")
        print(f"✅ System performance meets requirements")
        return True
    else:
        print(f"\n⚠️ SOME PERFORMANCE TESTS FAILED!")
        print(f"🔍 Review failed tests and optimize performance")
        return False

def benchmark_system():
    """Run system benchmark"""
    print("🔧 System Benchmark")
    print("=" * 40)
    
    # CPU benchmark
    print("🖥️ CPU Benchmark:")
    cpu_start = time.time()
    result = sum(i ** 2 for i in range(100000))
    cpu_time = time.time() - cpu_start
    print(f"   CPU calculation time: {cpu_time:.3f}s")
    
    # Memory benchmark
    print("💾 Memory Benchmark:")
    memory_start = psutil.Process().memory_info().rss / 1024 / 1024
    large_list = [i for i in range(100000)]
    memory_peak = psutil.Process().memory_info().rss / 1024 / 1024
    del large_list
    print(f"   Memory usage: {memory_peak - memory_start:.2f} MB")
    
    # Threading benchmark
    print("🧵 Threading Benchmark:")
    thread_start = time.time()
    threads = [threading.Thread(target=time.sleep, args=(0.1,)) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    thread_time = time.time() - thread_start
    print(f"   100 threads time: {thread_time:.3f}s")
    
    print("\n🏆 Benchmark Complete!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DDOS Educational Toolkit - Performance Testing")
    parser.add_argument('--benchmark', '-b', action='store_true', help='Run system benchmark')
    parser.add_argument('--test', '-t', help='Run specific test class')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--profile', '-p', action='store_true', help='Enable memory profiling')
    
    args = parser.parse_args()
    
    if args.benchmark:
        benchmark_system()
        sys.exit(0)
    
    if args.test:
        test_classes = {
            'threading': TestThreadingPerformance,
            'memory': TestMemoryPerformance,
            'network': TestNetworkPerformance,
            'statistics': TestStatisticsPerformance,
            'scalability': TestLoadScalability,
            'resources': TestSystemResourceUsage
        }
        
        if args.test in test_classes:
            suite = unittest.TestLoader().loadTestsFromTestCase(test_classes[args.test])
            runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
            result = runner.run(suite)
            sys.exit(0 if result.wasSuccessful() else 1)
        else:
            print(f"Unknown test class: {args.test}")
            print("Available tests:", list(test_classes.keys()))
            sys.exit(1)
    
    # Run all performance tests
    success = run_performance_tests()
    
    if not success:
        print("\n💡 Performance Optimization Tips:")
        print("  • Increase system memory if memory tests failed")
        print("  • Check CPU usage and close other applications") 
        print("  • Optimize thread count based on CPU cores")
        print("  • Review network configuration for network tests")
        print("  • Consider SSD storage for better I/O performance")
    
    sys.exit(0 if success else 1)
