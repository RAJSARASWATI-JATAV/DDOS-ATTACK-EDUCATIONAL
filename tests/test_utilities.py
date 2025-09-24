#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Utilities Testing Suite
Author: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
Purpose: Comprehensive testing framework for utility modules

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import unittest
import tempfile
import os
import json
import time
import threading
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import utility modules
from utils.logger import Logger
from utils.statistics import Statistics
from utils.config_manager import ConfigManager
from utils.banner import Banner
from utils.validator import Validator
from utils.report_generator import ReportGenerator
from proxy_handler import ProxyHandler
from network_scanner import NetworkScanner
from payload_generator import PayloadGenerator

class TestUtilities(unittest.TestCase):
    """Base test class for utilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data = {
            'test_key': 'test_value',
            'nested': {'key': 'value'},
            'list': [1, 2, 3]
        }
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

class TestLogger(TestUtilities):
    """Test Logger utility"""
    
    def test_logger_initialization(self):
        """Test logger initialization"""
        logger = Logger()
        self.assertIsNotNone(logger)
        self.assertTrue(hasattr(logger, 'info'))
        self.assertTrue(hasattr(logger, 'error'))
        self.assertTrue(hasattr(logger, 'warning'))
        self.assertTrue(hasattr(logger, 'debug'))
    
    def test_logger_levels(self):
        """Test different logging levels"""
        with patch('builtins.print') as mock_print:
            logger = Logger()
            
            # Test info level
            logger.info("Test info message")
            mock_print.assert_called()
            
            # Test error level
            logger.error("Test error message")
            mock_print.assert_called()
            
            # Test warning level
            logger.warning("Test warning message")
            mock_print.assert_called()
            
            # Test debug level
            logger.debug("Test debug message")
            mock_print.assert_called()
    
    def test_logger_formatting(self):
        """Test logger message formatting"""
        with patch('builtins.print') as mock_print:
            logger = Logger()
            
            test_message = "Test formatting message"
            logger.info(test_message)
            
            # Check if print was called with formatted message
            args, kwargs = mock_print.call_args
            self.assertIn(test_message, str(args))
    
    def test_logger_with_colors(self):
        """Test logger color formatting"""
        logger = Logger()
        
        # Test that color methods don't raise exceptions
        try:
            logger.info("Info with colors")
            logger.error("Error with colors")
            logger.warning("Warning with colors")
            logger.success("Success with colors")
        except Exception as e:
            self.fail(f"Logger color formatting failed: {e}")

class TestStatistics(TestUtilities):
    """Test Statistics utility"""
    
    def test_statistics_initialization(self):
        """Test statistics initialization"""
        stats = Statistics()
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats.attack_stats, dict)
        self.assertIsInstance(stats.global_stats, dict)
    
    def test_attack_tracking_lifecycle(self):
        """Test complete attack tracking lifecycle"""
        stats = Statistics()
        attack_id = "test_attack_123"
        
        # Start tracking
        stats.start_tracking(attack_id)
        self.assertIn(attack_id, stats.attack_stats)
        
        # Record some requests
        stats.record_request(attack_id, success=True, response_time=0.1, bytes_sent=1024)
        stats.record_request(attack_id, success=False, response_time=0.2, bytes_sent=512)
        
        # Get stats
        attack_stats = stats.get_attack_stats(attack_id)
        self.assertIsNotNone(attack_stats)
        self.assertEqual(attack_stats['requests_sent'], 2)
        self.assertEqual(attack_stats['successful_requests'], 1)
        self.assertEqual(attack_stats['failed_requests'], 1)
        self.assertEqual(attack_stats['bytes_sent'], 1536)
        
        # Stop tracking
        stats.stop_tracking(attack_id)
        self.assertEqual(stats.attack_stats[attack_id]['status'], 'completed')
    
    def test_error_recording(self):
        """Test error recording functionality"""
        stats = Statistics()
        attack_id = "test_attack_errors"
        
        stats.start_tracking(attack_id)
        
        # Record different types of errors
        stats.record_error(attack_id, "Connection timeout")
        stats.record_error(attack_id, "DNS resolution failed")
        stats.record_error(attack_id, "Connection timeout")  # Duplicate
        
        attack_stats = stats.get_attack_stats(attack_id)
        errors = attack_stats.get('errors', {})
        
        self.assertEqual(errors.get("Connection timeout", 0), 2)
        self.assertEqual(errors.get("DNS resolution failed", 0), 1)
    
    def test_global_statistics(self):
        """Test global statistics tracking"""
        stats = Statistics()
        
        # Create multiple attacks
        for i in range(3):
            attack_id = f"test_attack_{i}"
            stats.start_tracking(attack_id)
            stats.record_request(attack_id, success=True, bytes_sent=1000)
            stats.record_request(attack_id, success=False, bytes_sent=500)
        
        global_stats = stats.get_global_stats()
        
        self.assertEqual(global_stats['total_attacks'], 3)
        self.assertEqual(global_stats['total_requests'], 6)
        self.assertEqual(global_stats['total_errors'], 3)
        self.assertEqual(global_stats['total_bytes_sent'], 4500)
    
    def test_statistics_calculations(self):
        """Test statistics calculations"""
        stats = Statistics()
        attack_id = "test_calculations"
        
        stats.start_tracking(attack_id)
        
        # Record requests with known values
        for i in range(10):
            success = i < 8  # 80% success rate
            response_time = 0.1 + (i * 0.01)  # Increasing response times
            stats.record_request(attack_id, success=success, response_time=response_time, bytes_sent=1000)
        
        attack_stats = stats.get_attack_stats(attack_id)
        
        # Check calculated values
        self.assertEqual(attack_stats['success_rate'], 80.0)
        self.assertAlmostEqual(attack_stats['avg_response_time'], 0.145, places=3)
        self.assertGreater(attack_stats['requests_per_second_avg'], 0)

class TestConfigManager(TestUtilities):
    """Test ConfigManager utility"""
    
    def test_config_manager_initialization(self):
        """Test config manager initialization"""
        config_file = os.path.join(self.temp_dir, "test_config.json")
        
        # Create test config file
        with open(config_file, 'w') as f:
            json.dump(self.test_data, f)
        
        config = ConfigManager(config_file)
        self.assertIsNotNone(config)
    
    def test_config_loading(self):
        """Test configuration loading"""
        config_file = os.path.join(self.temp_dir, "test_config.json")
        
        # Create test config
        with open(config_file, 'w') as f:
            json.dump(self.test_data, f)
        
        config = ConfigManager(config_file)
        
        # Test getting values
        self.assertEqual(config.get('test_key'), 'test_value')
        self.assertEqual(config.get('nested.key'), 'value')  # Nested access
        self.assertEqual(config.get('nonexistent', 'default'), 'default')
    
    def test_config_updating(self):
        """Test configuration updating"""
        config_file = os.path.join(self.temp_dir, "test_config.json")
        
        config = ConfigManager(config_file)
        
        # Set values
        config.set('new_key', 'new_value')
        config.set('nested.new_nested', 'nested_value')
        
        # Check values are set
        self.assertEqual(config.get('new_key'), 'new_value')
        self.assertEqual(config.get('nested.new_nested'), 'nested_value')
    
    def test_config_validation(self):
        """Test configuration validation"""
        config_file = os.path.join(self.temp_dir, "test_config.json")
        
        config = ConfigManager(config_file)
        
        # Test validation schema
        schema = {
            'required_key': str,
            'optional_key': int
        }
        
        # Valid config
        config.set('required_key', 'value')
        config.set('optional_key', 123)
        
        self.assertTrue(config.validate(schema))
    
    def test_config_file_operations(self):
        """Test config file save/load operations"""
        config_file = os.path.join(self.temp_dir, "test_config.json")
        
        config = ConfigManager(config_file)
        config.set('test_save', 'save_value')
        
        # Save and reload
        config.save()
        
        # Create new instance and check if data persisted
        new_config = ConfigManager(config_file)
        self.assertEqual(new_config.get('test_save'), 'save_value')

class TestBanner(TestUtilities):
    """Test Banner utility"""
    
    def test_banner_initialization(self):
        """Test banner initialization"""
        banner = Banner()
        self.assertIsNotNone(banner)
    
    def test_banner_display(self):
        """Test banner display functionality"""
        with patch('builtins.print') as mock_print:
            banner = Banner()
            banner.show_banner()
            
            # Should have called print
            self.assertTrue(mock_print.called)
            
            # Check that banner contains expected text
            calls = [str(call) for call in mock_print.call_args_list]
            banner_text = ''.join(calls)
            self.assertIn('DDOS', banner_text.upper())
    
    def test_banner_colors(self):
        """Test banner color functionality"""
        banner = Banner()
        
        # Should not raise exceptions
        try:
            banner.show_banner()
            banner.show_startup_animation()
        except Exception as e:
            self.fail(f"Banner color functionality failed: {e}")
    
    def test_banner_animation(self):
        """Test banner animation"""
        with patch('time.sleep'):  # Speed up animation for testing
            banner = Banner()
            
            try:
                banner.show_startup_animation()
            except Exception as e:
                self.fail(f"Banner animation failed: {e}")

class TestValidator(TestUtilities):
    """Test Validator utility"""
    
    def test_validator_initialization(self):
        """Test validator initialization"""
        validator = Validator()
        self.assertIsNotNone(validator)
    
    def test_ip_validation(self):
        """Test IP address validation"""
        validator = Validator()
        
        # Valid IPs
        valid_ips = ['192.168.1.1', '10.0.0.1', '172.16.0.1', '127.0.0.1']
        for ip in valid_ips:
            self.assertTrue(validator.is_valid_ip(ip), f"{ip} should be valid")
        
        # Invalid IPs
        invalid_ips = ['256.1.1.1', '192.168.1', 'not.an.ip', '']
        for ip in invalid_ips:
            self.assertFalse(validator.is_valid_ip(ip), f"{ip} should be invalid")
    
    def test_domain_validation(self):
        """Test domain name validation"""
        validator = Validator()
        
        # Valid domains
        valid_domains = ['example.com', 'sub.example.org', 'test-site.net']
        for domain in valid_domains:
            self.assertTrue(validator.is_valid_domain(domain), f"{domain} should be valid")
        
        # Invalid domains
        invalid_domains = ['', 'invalid', '...com', 'space domain.com']
        for domain in invalid_domains:
            self.assertFalse(validator.is_valid_domain(domain), f"{domain} should be invalid")
    
    def test_port_validation(self):
        """Test port number validation"""
        validator = Validator()
        
        # Valid ports
        valid_ports = [1, 80, 443, 8080, 65535]
        for port in valid_ports:
            self.assertTrue(validator.is_valid_port(port), f"Port {port} should be valid")
        
        # Invalid ports
        invalid_ports = [0, -1, 65536, 100000, 'not_a_port']
        for port in invalid_ports:
            self.assertFalse(validator.is_valid_port(port), f"Port {port} should be invalid")
    
    def test_url_validation(self):
        """Test URL validation"""
        validator = Validator()
        
        # Valid URLs
        valid_urls = [
            'http://example.com',
            'https://www.example.org',
            'http://192.168.1.1:8080',
            'https://sub.domain.com/path'
        ]
        for url in valid_urls:
            self.assertTrue(validator.is_valid_url(url), f"URL {url} should be valid")
        
        # Invalid URLs
        invalid_urls = ['not_a_url', 'ftp://example.com', '', 'http://']
        for url in invalid_urls:
            self.assertFalse(validator.is_valid_url(url), f"URL {url} should be invalid")
    
    def test_thread_count_validation(self):
        """Test thread count validation"""
        validator = Validator()
        
        # Valid thread counts
        valid_counts = [1, 10, 100, 1000]
        for count in valid_counts:
            self.assertTrue(validator.is_valid_thread_count(count))
        
        # Invalid thread counts
        invalid_counts = [0, -1, 'not_a_number', 100000]
        for count in invalid_counts:
            self.assertFalse(validator.is_valid_thread_count(count))

class TestReportGenerator(TestUtilities):
    """Test ReportGenerator utility"""
    
    def setUp(self):
        """Set up test fixtures"""
        super().setUp()
        self.stats = Statistics()
        self.report_gen = ReportGenerator()
        
        # Create test attack data
        attack_id = "test_attack_report"
        self.stats.start_tracking(attack_id)
        for i in range(10):
            self.stats.record_request(attack_id, success=(i % 3 != 0), response_time=0.1, bytes_sent=1000)
        self.stats.stop_tracking(attack_id)
        self.attack_id = attack_id
    
    def test_report_generator_initialization(self):
        """Test report generator initialization"""
        report_gen = ReportGenerator()
        self.assertIsNotNone(report_gen)
    
    def test_html_report_generation(self):
        """Test HTML report generation"""
        report_file = os.path.join(self.temp_dir, "test_report.html")
        
        # Mock statistics
        with patch.object(self.report_gen, 'stats', self.stats):
            result = self.report_gen.generate_html_report(self.attack_id, report_file)
        
        self.assertEqual(result, report_file)
        self.assertTrue(os.path.exists(report_file))
        
        # Check file contents
        with open(report_file, 'r') as f:
            content = f.read()
            self.assertIn('DDOS Attack Analysis Report', content)
            self.assertIn(self.attack_id, content)
    
    def test_csv_report_generation(self):
        """Test CSV report generation"""
        report_file = os.path.join(self.temp_dir, "test_report.csv")
        
        with patch.object(self.report_gen, 'stats', self.stats):
            result = self.report_gen.generate_csv_report(report_file)
        
        self.assertEqual(result, report_file)
        self.assertTrue(os.path.exists(report_file))
        
        # Check CSV format
        import csv
        with open(report_file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertIn('Attack_ID', headers)
            self.assertIn('Status', headers)
    
    def test_json_report_generation(self):
        """Test JSON report generation"""
        report_file = os.path.join(self.temp_dir, "test_report.json")
        
        with patch.object(self.report_gen, 'stats', self.stats):
            result = self.report_gen.generate_json_report(self.attack_id, report_file)
        
        self.assertEqual(result, report_file)
        self.assertTrue(os.path.exists(report_file))
        
        # Check JSON format
        with open(report_file, 'r') as f:
            data = json.load(f)
            self.assertIn('report_metadata', data)
            self.assertIn('attack_statistics', data)

class TestProxyHandler(TestUtilities):
    """Test ProxyHandler utility"""
    
    def test_proxy_handler_initialization(self):
        """Test proxy handler initialization"""
        proxy_handler = ProxyHandler()
        self.assertIsNotNone(proxy_handler)
        self.assertIsInstance(proxy_handler.proxy_list, list)
        self.assertIsInstance(proxy_handler.working_proxies, list)
    
    def test_proxy_loading(self):
        """Test proxy loading from file"""
        proxy_file = os.path.join(self.temp_dir, "test_proxies.txt")
        
        # Create test proxy file
        proxies = ["192.168.1.1:8080", "10.0.0.1:3128", "127.0.0.1:9050"]
        with open(proxy_file, 'w') as f:
            for proxy in proxies:
                f.write(f"{proxy}\n")
        
        proxy_handler = ProxyHandler()
        result = proxy_handler.load_proxies(proxy_file)
        
        self.assertTrue(result)
        self.assertEqual(len(proxy_handler.proxy_list), 3)
        self.assertIn("192.168.1.1:8080", proxy_handler.proxy_list)
    
    @patch('requests.get')
    def test_proxy_validation(self, mock_get):
        """Test proxy validation"""
        # Mock successful proxy response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.5
        mock_get.return_value = mock_response
        
        proxy_handler = ProxyHandler()
        proxy_handler.proxy_list = ["127.0.0.1:8080"]
        
        working_count = proxy_handler.validate_proxies(max_workers=1)
        
        self.assertGreater(working_count, 0)
        self.assertIn("127.0.0.1:8080", proxy_handler.working_proxies)
    
    def test_proxy_rotation(self):
        """Test proxy rotation functionality"""
        proxy_handler = ProxyHandler()
        proxy_handler.working_proxies = ["proxy1:8080", "proxy2:8080", "proxy3:8080"]
        
        # Initialize stats
        for proxy in proxy_handler.working_proxies:
            proxy_handler.proxy_stats[proxy] = {
                'response_time': 0.5,
                'success_count': 0,
                'error_count': 0,
                'last_used': None
            }
        
        # Get proxies in rotation
        proxies_gotten = []
        for i in range(6):  # Get more than the number of proxies
            proxy = proxy_handler.get_next_proxy()
            proxies_gotten.append(proxy)
        
        # Should rotate through all proxies
        unique_proxies = set(proxies_gotten)
        self.assertEqual(len(unique_proxies), 3)
    
    def test_proxy_statistics(self):
        """Test proxy usage statistics"""
        proxy_handler = ProxyHandler()
        proxy_handler.proxy_list = ["proxy1:8080", "proxy2:8080"]
        proxy_handler.working_proxies = ["proxy1:8080"]
        proxy_handler.proxy_stats = {
            "proxy1:8080": {
                'response_time': 0.5,
                'success_count': 10,
                'error_count': 2,
                'last_used': time.time()
            }
        }
        
        stats = proxy_handler.get_proxy_statistics()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_loaded', stats)
        self.assertIn('working_proxies', stats)
        self.assertIn('success_rate', stats)
        self.assertEqual(stats['working_proxies'], 1)

class TestNetworkScanner(TestUtilities):
    """Test NetworkScanner utility"""
    
    def test_network_scanner_initialization(self):
        """Test network scanner initialization"""
        scanner = NetworkScanner()
        self.assertIsNotNone(scanner)
        self.assertIsInstance(scanner.open_ports, list)
        self.assertIsInstance(scanner.services, dict)
    
    @patch('subprocess.call')
    def test_ping_host(self, mock_call):
        """Test host ping functionality"""
        # Mock successful ping
        mock_call.return_value = 0
        
        scanner = NetworkScanner()
        result = scanner.ping_host("127.0.0.1")
        
        self.assertTrue(result)
        mock_call.assert_called_once()
    
    @patch('socket.socket')
    def test_port_scanning(self, mock_socket):
        """Test port scanning functionality"""
        # Mock successful connection
        mock_sock = Mock()
        mock_socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 0  # Success
        mock_sock.close.return_value = None
        
        scanner = NetworkScanner()
        ports = [80, 443]
        open_ports = scanner.port_scan("127.0.0.1", ports, threads=2)
        
        self.assertEqual(len(open_ports), 2)
        self.assertIn(80, open_ports)
        self.assertIn(443, open_ports)
    
    def test_comprehensive_scan(self):
        """Test comprehensive scan functionality"""
        with patch.object(NetworkScanner, 'ping_host', return_value=True), \
             patch.object(NetworkScanner, 'port_scan', return_value=[80, 443]), \
             patch.object(NetworkScanner, 'service_detection', return_value="HTTP Server"):
            
            scanner = NetworkScanner()
            results = scanner.comprehensive_scan("127.0.0.1")
            
            self.assertIsInstance(results, dict)
            self.assertTrue(results['alive'])
            self.assertIn(80, results['open_ports'])
            self.assertIn(443, results['open_ports'])

class TestPayloadGenerator(TestUtilities):
    """Test PayloadGenerator utility"""
    
    def test_payload_generator_initialization(self):
        """Test payload generator initialization"""
        generator = PayloadGenerator()
        self.assertIsNotNone(generator)
        self.assertIsInstance(generator.user_agents, list)
        self.assertGreater(len(generator.user_agents), 0)
    
    def test_http_payload_generation(self):
        """Test HTTP payload generation"""
        generator = PayloadGenerator()
        
        # Test GET payload
        get_payload = generator.generate_http_payload("http://example.com", method='GET')
        self.assertIsInstance(get_payload, bytes)
        self.assertIn(b'GET', get_payload)
        self.assertIn(b'HTTP/1.1', get_payload)
        
        # Test POST payload
        post_payload = generator.generate_http_payload("http://example.com", method='POST')
        self.assertIsInstance(post_payload, bytes)
        self.assertIn(b'POST', post_payload)
        self.assertIn(b'Content-Length', post_payload)
    
    def test_tcp_payload_generation(self):
        """Test TCP payload generation"""
        generator = PayloadGenerator()
        
        payload = generator.generate_tcp_payload(size=1024)
        self.assertIsInstance(payload, bytes)
        self.assertEqual(len(payload), 1024)
        
        # Test different sizes
        for size in [64, 256, 512, 2048]:
            payload = generator.generate_tcp_payload(size=size)
            self.assertEqual(len(payload), size)
    
    def test_udp_payload_generation(self):
        """Test UDP payload generation"""
        generator = PayloadGenerator()
        
        payload = generator.generate_udp_payload(size=512)
        self.assertIsInstance(payload, bytes)
        # UDP payload might be different sizes due to different types
        self.assertGreater(len(payload), 0)
    
    def test_dns_payload_generation(self):
        """Test DNS payload generation"""
        generator = PayloadGenerator()
        
        dns_data = generator.generate_dns_payload(query_type='A')
        self.assertIsInstance(dns_data, dict)
        self.assertIn('transaction_id', dns_data)
        self.assertIn('domain', dns_data)
        self.assertIn('query_type', dns_data)
        self.assertEqual(dns_data['query_type'], 'A')
    
    def test_payload_randomization(self):
        """Test payload randomization"""
        generator = PayloadGenerator()
        
        # Generate multiple payloads and check for variation
        payloads = []
        for _ in range(5):
            payload = generator.generate_tcp_payload(size=100)
            payloads.append(payload)
        
        # Should have some variation
        unique_payloads = set(payloads)
        self.assertGreater(len(unique_payloads), 1, "Payloads should be randomized")

def create_test_suite():
    """Create comprehensive utilities test suite"""
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestLogger,
        TestStatistics,
        TestConfigManager,
        TestBanner,
        TestValidator,
        TestReportGenerator,
        TestProxyHandler,
        TestNetworkScanner,
        TestPayloadGenerator
    ]
    
    for test_class in test_classes:
        test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
    
    return test_suite

def run_tests():
    """Run all utility tests"""
    print("🧪 Starting DDOS Educational Toolkit - Utilities Test Suite")
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
    print("🧪 UTILITIES TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\n🚨 ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if result.wasSuccessful():
        print("\n✅ ALL UTILITY TESTS PASSED! All utilities are functioning correctly.")
        return True
    else:
        print("\n❌ SOME UTILITY TESTS FAILED! Please review and fix issues.")
        return False

if __name__ == "__main__":
    # Add command line options
    import argparse
    
    parser = argparse.ArgumentParser(description="DDOS Educational Toolkit - Utilities Testing")
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--utility', '-u', help='Test specific utility only')
    parser.add_argument('--list', '-l', action='store_true', help='List available utilities')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available utility tests:")
        print("- logger: Logging system tests")
        print("- statistics: Performance statistics tests")
        print("- config: Configuration management tests")
        print("- banner: Banner display tests")
        print("- validator: Input validation tests")
        print("- report: Report generation tests")
        print("- proxy: Proxy handler tests")
        print("- scanner: Network scanner tests")
        print("- payload: Payload generator tests")
        sys.exit(0)
    
    # Run specific utility tests if requested
    if args.utility:
        utility_tests = {
            'logger': TestLogger,
            'statistics': TestStatistics,
            'config': TestConfigManager,
            'banner': TestBanner,
            'validator': TestValidator,
            'report': TestReportGenerator,
            'proxy': TestProxyHandler,
            'scanner': TestNetworkScanner,
            'payload': TestPayloadGenerator
        }
        
        if args.utility in utility_tests:
            suite = unittest.TestLoader().loadTestsFromTestCase(utility_tests[args.utility])
            runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
            result = runner.run(suite)
            sys.exit(0 if result.wasSuccessful() else 1)
        else:
            print(f"Unknown utility: {args.utility}")
            print("Use --list to see available utilities")
            sys.exit(1)
    
    # Run all tests
    success = run_tests()
    sys.exit(0 if success else 1)
