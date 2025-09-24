#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Attack Modules Testing Suite
Author: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
Purpose: Comprehensive testing framework for all attack modules

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import unittest
import threading
import time
import socket
import json
import requests
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import attack modules
from attack_modules import AttackController
from modules.http_flood import HttpFlood
from modules.tcp_flood import TcpFlood
from modules.udp_flood import UdpFlood
from modules.syn_flood import SynFlood
from modules.slowloris import Slowloris
from modules.rudy_attack import RudyAttack
from modules.dns_flood import DnsFlood
from modules.cc_attack import CcAttack
from utils.logger import Logger
from utils.statistics import Statistics

class TestAttackModules(unittest.TestCase):
    """Test suite for all attack modules"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_target = "127.0.0.1"  # Localhost for safe testing
        self.test_port = 8080
        self.test_threads = 10
        self.test_duration = 2  # Short duration for tests
        self.logger = Logger()
        self.stats = Statistics()
        
        # Create test server for some tests
        self.test_server_running = False
        self.setup_test_server()
    
    def setUp_test_server(self):
        """Set up a simple test HTTP server"""
        try:
            # Start a simple test server in background
            import http.server
            import socketserver
            import threading
            
            handler = http.server.SimpleHTTPRequestHandler
            self.test_server = socketserver.TCPServer(("", self.test_port), handler)
            
            server_thread = threading.Thread(target=self.test_server.serve_forever, daemon=True)
            server_thread.start()
            self.test_server_running = True
            time.sleep(0.5)  # Allow server to start
            
        except Exception as e:
            print(f"Warning: Could not start test server: {e}")
            self.test_server_running = False
    
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'test_server') and self.test_server_running:
            try:
                self.test_server.shutdown()
                self.test_server.server_close()
            except:
                pass

class TestHttpFloodModule(TestAttackModules):
    """Test HTTP Flood attack module"""
    
    def test_http_flood_initialization(self):
        """Test HTTP Flood module initialization"""
        http_attack = HttpFlood(target=self.test_target, port=self.test_port)
        
        self.assertEqual(http_attack.target, self.test_target)
        self.assertEqual(http_attack.port, self.test_port)
        self.assertIsNotNone(http_attack.logger)
        self.assertIn('GET', http_attack.methods)
    
    def test_http_flood_payload_generation(self):
        """Test HTTP payload generation"""
        http_attack = HttpFlood(target=self.test_target, port=self.test_port)
        
        # Test GET payload
        get_payload = http_attack.generate_payload(method='GET')
        self.assertIsInstance(get_payload, bytes)
        self.assertIn(b'GET', get_payload)
        self.assertIn(b'HTTP/1.1', get_payload)
        
        # Test POST payload
        post_payload = http_attack.generate_payload(method='POST')
        self.assertIsInstance(post_payload, bytes)
        self.assertIn(b'POST', post_payload)
        self.assertIn(b'Content-Length', post_payload)
    
    def test_http_flood_user_agent_rotation(self):
        """Test user agent rotation functionality"""
        http_attack = HttpFlood(target=self.test_target, port=self.test_port)
        
        agents = []
        for _ in range(10):
            payload = http_attack.generate_payload()
            payload_str = payload.decode('utf-8', errors='ignore')
            # Extract user agent
            for line in payload_str.split('\r\n'):
                if line.startswith('User-Agent:'):
                    agents.append(line)
                    break
        
        # Should have some variety in user agents
        unique_agents = set(agents)
        self.assertGreater(len(unique_agents), 1, "User agents should rotate")
    
    @patch('socket.socket')
    def test_http_flood_execution(self, mock_socket):
        """Test HTTP flood attack execution"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.send.return_value = 100
        mock_sock.recv.return_value = b'HTTP/1.1 200 OK\r\n\r\n'
        mock_sock.close.return_value = None
        
        http_attack = HttpFlood(target=self.test_target, port=self.test_port)
        result = http_attack.execute_attack()
        
        self.assertTrue(result)
        mock_socket.assert_called()
        mock_sock.connect.assert_called_with((self.test_target, self.test_port))
        mock_sock.send.assert_called()
    
    def test_http_flood_error_handling(self):
        """Test HTTP flood error handling"""
        # Test with invalid target
        http_attack = HttpFlood(target="invalid.invalid.invalid", port=80)
        result = http_attack.execute_attack()
        
        # Should handle errors gracefully
        self.assertIsInstance(result, bool)

class TestTcpFloodModule(TestAttackModules):
    """Test TCP Flood attack module"""
    
    def test_tcp_flood_initialization(self):
        """Test TCP Flood module initialization"""
        tcp_attack = TcpFlood(target=self.test_target, port=self.test_port)
        
        self.assertEqual(tcp_attack.target, self.test_target)
        self.assertEqual(tcp_attack.port, self.test_port)
        self.assertIsNotNone(tcp_attack.logger)
    
    @patch('socket.socket')
    def test_tcp_flood_connection(self, mock_socket):
        """Test TCP connection establishment"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.send.return_value = 1024
        mock_sock.close.return_value = None
        
        tcp_attack = TcpFlood(target=self.test_target, port=self.test_port)
        result = tcp_attack.execute_attack()
        
        self.assertTrue(result)
        mock_sock.connect.assert_called_with((self.test_target, self.test_port))
    
    def test_tcp_flood_payload_generation(self):
        """Test TCP payload generation"""
        tcp_attack = TcpFlood(target=self.test_target, port=self.test_port)
        
        payload = tcp_attack.generate_payload(size=1024)
        self.assertIsInstance(payload, bytes)
        self.assertEqual(len(payload), 1024)
    
    def test_tcp_flood_random_payload(self):
        """Test TCP random payload generation"""
        tcp_attack = TcpFlood(target=self.test_target, port=self.test_port)
        
        payload1 = tcp_attack.generate_payload(size=512)
        payload2 = tcp_attack.generate_payload(size=512)
        
        # Payloads should be different (random)
        self.assertNotEqual(payload1, payload2)

class TestUdpFloodModule(TestAttackModules):
    """Test UDP Flood attack module"""
    
    def test_udp_flood_initialization(self):
        """Test UDP Flood module initialization"""
        udp_attack = UdpFlood(target=self.test_target, port=self.test_port)
        
        self.assertEqual(udp_attack.target, self.test_target)
        self.assertEqual(udp_attack.port, self.test_port)
        self.assertIsNotNone(udp_attack.logger)
    
    @patch('socket.socket')
    def test_udp_flood_execution(self, mock_socket):
        """Test UDP flood attack execution"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.sendto.return_value = 512
        mock_sock.close.return_value = None
        
        udp_attack = UdpFlood(target=self.test_target, port=self.test_port)
        result = udp_attack.execute_attack()
        
        self.assertTrue(result)
        mock_sock.sendto.assert_called()
    
    def test_udp_flood_payload_sizes(self):
        """Test UDP payload with different sizes"""
        udp_attack = UdpFlood(target=self.test_target, port=self.test_port)
        
        # Test various payload sizes
        sizes = [64, 256, 512, 1024, 8192]
        for size in sizes:
            payload = udp_attack.generate_payload(size=size)
            self.assertEqual(len(payload), size)
            self.assertIsInstance(payload, bytes)

class TestSynFloodModule(TestAttackModules):
    """Test SYN Flood attack module"""
    
    def test_syn_flood_initialization(self):
        """Test SYN Flood module initialization"""
        syn_attack = SynFlood(target=self.test_target, port=self.test_port)
        
        self.assertEqual(syn_attack.target, self.test_target)
        self.assertEqual(syn_attack.port, self.test_port)
        self.assertIsNotNone(syn_attack.logger)
    
    def test_syn_packet_generation(self):
        """Test SYN packet generation"""
        syn_attack = SynFlood(target=self.test_target, port=self.test_port)
        
        packet_info = syn_attack.generate_syn_packet()
        
        self.assertIsInstance(packet_info, dict)
        self.assertIn('src_port', packet_info)
        self.assertIn('dst_port', packet_info)
        self.assertIn('seq_num', packet_info)
        self.assertIn('flags', packet_info)
        self.assertEqual(packet_info['flags'], 'SYN')
    
    def test_syn_flood_random_ports(self):
        """Test SYN flood random source port generation"""
        syn_attack = SynFlood(target=self.test_target, port=self.test_port)
        
        ports = []
        for _ in range(10):
            packet = syn_attack.generate_syn_packet()
            ports.append(packet['src_port'])
        
        # Should have variety in source ports
        unique_ports = set(ports)
        self.assertGreater(len(unique_ports), 5, "Source ports should vary")

class TestSlowlorisModule(TestAttackModules):
    """Test Slowloris attack module"""
    
    def test_slowloris_initialization(self):
        """Test Slowloris module initialization"""
        slowloris = Slowloris(target=self.test_target, port=self.test_port)
        
        self.assertEqual(slowloris.target, self.test_target)
        self.assertEqual(slowloris.port, self.test_port)
        self.assertIsNotNone(slowloris.logger)
        self.assertIsNotNone(slowloris.connections)
    
    def test_slowloris_partial_header_generation(self):
        """Test partial HTTP header generation"""
        slowloris = Slowloris(target=self.test_target, port=self.test_port)
        
        headers = slowloris.generate_partial_headers()
        self.assertIsInstance(headers, bytes)
        self.assertIn(b'GET', headers)
        self.assertIn(b'HTTP/1.1', headers)
        self.assertIn(b'Host:', headers)
        # Should NOT end with double CRLF (incomplete)
        self.assertNotIn(b'\r\n\r\n', headers)
    
    @patch('socket.socket')
    def test_slowloris_connection_management(self, mock_socket):
        """Test Slowloris connection management"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.send.return_value = 100
        mock_sock.close.return_value = None
        
        slowloris = Slowloris(target=self.test_target, port=self.test_port)
        
        # Test connection creation
        result = slowloris.create_connection()
        self.assertTrue(result)
        
        # Test sending keep-alive headers
        result = slowloris.send_keep_alive()
        self.assertTrue(result)

class TestRudyAttackModule(TestAttackModules):
    """Test RUDY (R-U-Dead-Yet) attack module"""
    
    def test_rudy_initialization(self):
        """Test RUDY module initialization"""
        rudy = RudyAttack(target=self.test_target, port=self.test_port)
        
        self.assertEqual(rudy.target, self.test_target)
        self.assertEqual(rudy.port, self.test_port)
        self.assertIsNotNone(rudy.logger)
    
    def test_rudy_post_headers(self):
        """Test RUDY POST headers generation"""
        rudy = RudyAttack(target=self.test_target, port=self.test_port)
        
        headers, boundary = rudy.generate_post_headers()
        
        self.assertIsInstance(headers, dict)
        self.assertIn('Content-Type', headers)
        self.assertIn('multipart/form-data', headers['Content-Type'])
        self.assertIn('Content-Length', headers)
        self.assertIsInstance(boundary, str)
    
    def test_rudy_slow_post_data(self):
        """Test RUDY slow POST data generation"""
        rudy = RudyAttack(target=self.test_target, port=self.test_port)
        
        data_chunk = rudy.generate_slow_post_data()
        
        self.assertIsInstance(data_chunk, bytes)
        self.assertGreater(len(data_chunk), 0)
    
    @patch('socket.socket')
    def test_rudy_attack_execution(self, mock_socket):
        """Test RUDY attack execution"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.send.return_value = 100
        mock_sock.close.return_value = None
        
        rudy = RudyAttack(target=self.test_target, port=self.test_port)
        result = rudy.execute_attack()
        
        self.assertTrue(result)
        mock_sock.connect.assert_called()

class TestDnsFloodModule(TestAttackModules):
    """Test DNS Flood attack module"""
    
    def test_dns_flood_initialization(self):
        """Test DNS Flood module initialization"""
        dns_attack = DnsFlood(target=self.test_target, port=53)
        
        self.assertEqual(dns_attack.target, self.test_target)
        self.assertEqual(dns_attack.port, 53)
        self.assertIsNotNone(dns_attack.logger)
    
    def test_dns_query_generation(self):
        """Test DNS query generation"""
        dns_attack = DnsFlood(target=self.test_target, port=53)
        
        query_data = dns_attack.generate_dns_query()
        
        self.assertIsInstance(query_data, dict)
        self.assertIn('transaction_id', query_data)
        self.assertIn('domain', query_data)
        self.assertIn('query_type', query_data)
        self.assertIn('payload', query_data)
    
    def test_dns_query_types(self):
        """Test different DNS query types"""
        dns_attack = DnsFlood(target=self.test_target, port=53)
        
        query_types = ['A', 'AAAA', 'MX', 'TXT', 'NS']
        for qtype in query_types:
            query = dns_attack.generate_dns_query(query_type=qtype)
            self.assertEqual(query['query_type'], qtype)
    
    def test_dns_domain_randomization(self):
        """Test DNS domain randomization"""
        dns_attack = DnsFlood(target=self.test_target, port=53)
        
        domains = []
        for _ in range(10):
            query = dns_attack.generate_dns_query()
            domains.append(query['domain'])
        
        # Should have variety in domains
        unique_domains = set(domains)
        self.assertGreater(len(unique_domains), 5, "Domains should vary")

class TestCcAttackModule(TestAttackModules):
    """Test Challenge Collapsar (CC) attack module"""
    
    def test_cc_attack_initialization(self):
        """Test CC attack module initialization"""
        cc_attack = CcAttack(target=self.test_target, port=self.test_port)
        
        self.assertEqual(cc_attack.target, self.test_target)
        self.assertEqual(cc_attack.port, self.test_port)
        self.assertIsNotNone(cc_attack.logger)
    
    def test_cc_cache_buster_generation(self):
        """Test CC cache buster parameter generation"""
        cc_attack = CcAttack(target=self.test_target, port=self.test_port)
        
        url1 = cc_attack.generate_cache_buster_url("/test")
        url2 = cc_attack.generate_cache_buster_url("/test")
        
        # URLs should be different (cache busting)
        self.assertNotEqual(url1, url2)
        self.assertIn("/test", url1)
        self.assertIn("?", url1)  # Should have parameters
    
    def test_cc_session_simulation(self):
        """Test CC session simulation"""
        cc_attack = CcAttack(target=self.test_target, port=self.test_port)
        
        session_headers = cc_attack.generate_session_headers()
        
        self.assertIsInstance(session_headers, dict)
        self.assertIn('Referer', session_headers)
        self.assertIn('Cache-Control', session_headers)
    
    @patch('socket.socket')
    def test_cc_attack_execution(self, mock_socket):
        """Test CC attack execution"""
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None
        mock_sock.send.return_value = 100
        mock_sock.recv.return_value = b'HTTP/1.1 200 OK\r\n\r\n'
        mock_sock.close.return_value = None
        
        cc_attack = CcAttack(target=self.test_target, port=self.test_port)
        result = cc_attack.execute_attack()
        
        self.assertTrue(result)
        mock_sock.connect.assert_called()

class TestAttackController(TestAttackModules):
    """Test Attack Controller functionality"""
    
    def test_attack_controller_initialization(self):
        """Test AttackController initialization"""
        controller = AttackController()
        
        self.assertIsNotNone(controller.logger)
        self.assertIsNotNone(controller.stats)
        self.assertIsInstance(controller.active_attacks, dict)
    
    def test_module_loading(self):
        """Test dynamic module loading"""
        controller = AttackController()
        
        # Test loading valid module
        http_class = controller.load_module('http_flood')
        self.assertIsNotNone(http_class)
        
        # Test loading invalid module
        invalid_class = controller.load_module('invalid_module')
        self.assertIsNone(invalid_class)
    
    @patch.object(AttackController, 'load_module')
    def test_attack_start_stop(self, mock_load_module):
        """Test attack start and stop functionality"""
        # Mock the module loading
        mock_attack_class = Mock()
        mock_attack_instance = Mock()
        mock_attack_class.return_value = mock_attack_instance
        mock_attack_instance.execute_attack.return_value = True
        mock_load_module.return_value = mock_attack_class
        
        controller = AttackController()
        
        # Test starting attack
        attack_id = controller.start_attack(
            attack_type='http_flood',
            target=self.test_target,
            threads=5,
            duration=1
        )
        
        self.assertIsNotNone(attack_id)
        self.assertIn(attack_id, controller.active_attacks)
        
        # Let it run briefly
        time.sleep(0.5)
        
        # Test stopping attack
        result = controller.stop_attack(attack_id)
        self.assertTrue(result)
    
    def test_active_attacks_tracking(self):
        """Test active attacks tracking"""
        controller = AttackController()
        
        # Initially should be empty
        active = controller.get_active_attacks()
        self.assertIsInstance(active, dict)
        self.assertEqual(len(active), 0)

class TestAttackModuleIntegration(TestAttackModules):
    """Integration tests for attack modules"""
    
    def test_all_modules_importable(self):
        """Test that all attack modules can be imported"""
        modules = [
            'http_flood', 'tcp_flood', 'udp_flood', 'syn_flood',
            'slowloris', 'rudy_attack', 'dns_flood', 'cc_attack'
        ]
        
        controller = AttackController()
        
        for module_name in modules:
            with self.subTest(module=module_name):
                module_class = controller.load_module(module_name)
                self.assertIsNotNone(module_class, f"Failed to load {module_name}")
    
    def test_module_parameter_validation(self):
        """Test parameter validation across modules"""
        test_cases = [
            ('http_flood', {'target': self.test_target, 'port': self.test_port}),
            ('tcp_flood', {'target': self.test_target, 'port': self.test_port}),
            ('udp_flood', {'target': self.test_target, 'port': self.test_port}),
        ]
        
        for module_name, params in test_cases:
            with self.subTest(module=module_name):
                controller = AttackController()
                module_class = controller.load_module(module_name)
                
                if module_class:
                    # Should not raise exception
                    instance = module_class(**params)
                    self.assertIsNotNone(instance)

class TestAttackModuleErrorHandling(TestAttackModules):
    """Test error handling in attack modules"""
    
    def test_invalid_target_handling(self):
        """Test handling of invalid targets"""
        invalid_targets = [
            "invalid.invalid.invalid",
            "999.999.999.999",
            "localhost:invalid_port",
            ""
        ]
        
        for target in invalid_targets:
            with self.subTest(target=target):
                try:
                    http_attack = HttpFlood(target=target, port=80)
                    result = http_attack.execute_attack()
                    # Should handle gracefully
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    # Should not raise unhandled exceptions
                    self.fail(f"Unhandled exception for target {target}: {e}")
    
    def test_network_error_handling(self):
        """Test network error handling"""
        # Test with unreachable target
        http_attack = HttpFlood(target="192.0.2.1", port=80)  # TEST-NET-1
        
        # Should handle network errors gracefully
        try:
            result = http_attack.execute_attack()
            self.assertIsInstance(result, bool)
        except Exception as e:
            self.fail(f"Unhandled network exception: {e}")
    
    def test_resource_cleanup(self):
        """Test proper resource cleanup"""
        modules_to_test = [
            HttpFlood(self.test_target, self.test_port),
            TcpFlood(self.test_target, self.test_port),
            UdpFlood(self.test_target, self.test_port),
        ]
        
        for module in modules_to_test:
            with self.subTest(module=type(module).__name__):
                # Execute attack briefly
                try:
                    result = module.execute_attack()
                    # Should complete without resource leaks
                    self.assertIsInstance(result, bool)
                except Exception as e:
                    # Log but don't fail on expected network errors
                    if "Connection refused" not in str(e):
                        self.fail(f"Unexpected exception: {e}")

def create_test_suite():
    """Create comprehensive test suite"""
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestHttpFloodModule,
        TestTcpFloodModule,
        TestUdpFloodModule,
        TestSynFloodModule,
        TestSlowlorisModule,
        TestRudyAttackModule,
        TestDnsFloodModule,
        TestCcAttackModule,
        TestAttackController,
        TestAttackModuleIntegration,
        TestAttackModuleErrorHandling
    ]
    
    for test_class in test_classes:
        test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
    
    return test_suite

def run_tests():
    """Run all attack module tests"""
    print("🧪 Starting DDOS Educational Toolkit - Attack Modules Test Suite")
    print("=" * 70)
    
    # Create test suite
    test_suite = create_test_suite()
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=True,
        failfast=False
    )
    
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("🧪 TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print(f"\n🚨 ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED! Attack modules are functioning correctly.")
        return True
    else:
        print("\n❌ SOME TESTS FAILED! Please review and fix issues.")
        return False

if __name__ == "__main__":
    # Add command line options
    import argparse
    
    parser = argparse.ArgumentParser(description="DDOS Educational Toolkit - Attack Modules Testing")
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--module', '-m', help='Test specific module only')
    parser.add_argument('--list', '-l', action='store_true', help='List available test modules')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available test modules:")
        print("- http_flood: HTTP Flood attack tests")
        print("- tcp_flood: TCP Flood attack tests")
        print("- udp_flood: UDP Flood attack tests")
        print("- syn_flood: SYN Flood attack tests")
        print("- slowloris: Slowloris attack tests")
        print("- rudy_attack: RUDY attack tests")
        print("- dns_flood: DNS Flood attack tests")
        print("- cc_attack: CC attack tests")
        print("- controller: Attack controller tests")
        print("- integration: Integration tests")
        print("- error_handling: Error handling tests")
        sys.exit(0)
    
    # Run specific module tests if requested
    if args.module:
        module_tests = {
            'http_flood': TestHttpFloodModule,
            'tcp_flood': TestTcpFloodModule,
            'udp_flood': TestUdpFloodModule,
            'syn_flood': TestSynFloodModule,
            'slowloris': TestSlowlorisModule,
            'rudy_attack': TestRudyAttackModule,
            'dns_flood': TestDnsFloodModule,
            'cc_attack': TestCcAttackModule,
            'controller': TestAttackController,
            'integration': TestAttackModuleIntegration,
            'error_handling': TestAttackModuleErrorHandling
        }
        
        if args.module in module_tests:
            suite = unittest.TestLoader().loadTestsFromTestCase(module_tests[args.module])
            runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
            result = runner.run(suite)
            sys.exit(0 if result.wasSuccessful() else 1)
        else:
            print(f"Unknown module: {args.module}")
            print("Use --list to see available modules")
            sys.exit(1)
    
    # Run all tests
    success = run_tests()
    sys.exit(0 if success else 1)
