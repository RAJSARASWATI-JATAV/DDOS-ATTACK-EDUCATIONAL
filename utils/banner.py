#!/usr/bin/env python3
"""
🎨 Banner - ASCII Art Display System
Created By: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import random
import time
from colorama import Fore, Style, Back

def display_banner():
    """Display animated ASCII banner"""
    
    banner = f"""
{Fore.RED}{Style.BRIGHT}
██████╗ ██████╗ ██████╗ ██████╗    ███████╗███████╗███████╗██████╗ ██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗   ██╔════╝╚══██╔══╝╚══██╔══╝██╔══██╗██║ ██╔╝
██║  ██║██║  ██║██║  ██║██████╔╝   █████╗     ██║      ██║   ██████╔╝███████║
██║  ██║██║  ██║██║  ██║██╔══██╗   ██╔══╝     ██║      ██║   ██╔══██╗██╔════╝
██████╔╝██████╔╝██████╔╝██║  ██║   ███████╗   ██║      ██║   ██║  ██║███████╗
╚═════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚══════╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚══════╝
{Style.RESET_ALL}
{Fore.CYAN}{Style.BRIGHT}
            ┌──────────────────────────────────────────────────────────────────────┐
            │{Style.RESET_ALL}     {Fore.YELLOW}♥{Style.RESET_ALL} {Fore.RED}WORLD'S MOST POWERFUL DDOS EDUCATIONAL TOOLKIT{Style.RESET_ALL} {Fore.YELLOW}♥{Style.RESET_ALL}     {Fore.CYAN}│{Style.RESET_ALL}
            │{Style.RESET_ALL}                                                                  {Fore.CYAN}│{Style.RESET_ALL}
            │{Style.RESET_ALL}              {Fore.GREEN}⚡ UNLIMITED THREADS | NEXT LEVEL FEATURES{Style.RESET_ALL}              {Fore.CYAN}│{Style.RESET_ALL}
            │{Style.RESET_ALL}                                                                  {Fore.CYAN}│{Style.RESET_ALL}
            │{Style.RESET_ALL}                    {Fore.MAGENTA}Created By: Rajsaraswati Jatav{Style.RESET_ALL}                   {Fore.CYAN}│{Style.RESET_ALL}
            │{Style.RESET_ALL}                  {Fore.BLUE}GitHub: @RAJSARASWATI-JATAV{Style.RESET_ALL}                     {Fore.CYAN}│{Style.RESET_ALL}
            │{Style.RESET_ALL}                                                                  {Fore.CYAN}│{Style.RESET_ALL}
            │{Style.RESET_ALL}               {Fore.RED}⚠️  FOR EDUCATIONAL PURPOSES ONLY  ⚠️{Style.RESET_ALL}               {Fore.CYAN}│{Style.RESET_ALL}
            └──────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}
    """
    
    # Animated display
    lines = banner.split('\n')
    for line in lines:
        print(line)
        time.sleep(0.05)
    
    # Loading animation
    print(f"\n{Fore.YELLOW}Loading toolkit", end="")
    for i in range(3):
        for dot in [".", "..", "..."]:
            print(f"\r{Fore.YELLOW}Loading toolkit{dot}   ", end="")
            time.sleep(0.3)
    print(f"\r{Fore.GREEN}Toolkit loaded successfully! ✓{Style.RESET_ALL}\n")

def display_loading_bar(duration=3):
    """Display animated loading bar"""
    bar_length = 50
    for i in range(bar_length + 1):
        percent = (i / bar_length) * 100
        bar = '█' * i + '░' * (bar_length - i)
        print(f"\r{Fore.CYAN}[{{bar}}] {percent:.1f}%{Style.RESET_ALL}", end="")
        time.sleep(duration / bar_length)
    print()