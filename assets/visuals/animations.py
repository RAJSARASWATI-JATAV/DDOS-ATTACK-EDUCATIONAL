#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Visual Animations
Author: Rajsaraswati Jatav
GitHub: https://github.com/RAJSARASWATI-JATAV
Purpose: Dynamic visual effects and animations

⚠️ FOR EDUCATIONAL AND ETHICAL TESTING PURPOSES ONLY ⚠️
"""

import time
import sys
import random
import threading
from colorama import init, Fore, Back, Style, Cursor
import os

# Initialize colorama
init(autoreset=True)

class VisualEffects:
    """Advanced visual effects and animations for the DDOS toolkit"""
    
    def __init__(self):
        self.colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
        self.bright_colors = [Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, 
                             Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]
        self.animation_running = False
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def hide_cursor(self):
        """Hide terminal cursor"""
        print('\033[?25l', end='')
        
    def show_cursor(self):
        """Show terminal cursor"""
        print('\033[?25h', end='')
    
    def loading_animation(self, text="Loading", duration=3, style="dots"):
        """Advanced loading animations with multiple styles"""
        
        if style == "dots":
            self._dots_loading(text, duration)
        elif style == "spinner":
            self._spinner_loading(text, duration)
        elif style == "progress":
            self._progress_loading(text, duration)
        elif style == "matrix":
            self._matrix_loading(text, duration)
        elif style == "pulse":
            self._pulse_loading(text, duration)
    
    def _dots_loading(self, text, duration):
        """Classic dots loading animation"""
        self.hide_cursor()
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                for i in range(4):
                    dots = "." * i
                    sys.stdout.write(f"\r{Fore.CYAN + Style.BRIGHT}{text}{dots}    ")
                    sys.stdout.flush()
                    time.sleep(0.3)
        finally:
            self.show_cursor()
            print(f"\r{Fore.GREEN + Style.BRIGHT}{text} Complete! ✅    ")
    
    def _spinner_loading(self, text, duration):
        """Spinner loading animation"""
        spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.hide_cursor()
        start_time = time.time()
        i = 0
        
        try:
            while time.time() - start_time < duration:
                spinner = spinners[i % len(spinners)]
                sys.stdout.write(f"\r{Fore.YELLOW + Style.BRIGHT}{spinner} {text}")
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
        finally:
            self.show_cursor()
            print(f"\r{Fore.GREEN + Style.BRIGHT}✅ {text} Complete!")
    
    def _progress_loading(self, text, duration):
        """Progress bar loading animation"""
        self.hide_cursor()
        bar_length = 40
        
        try:
            for i in range(bar_length + 1):
                progress = i / bar_length
                filled_length = int(bar_length * progress)
                
                bar = "█" * filled_length + "▒" * (bar_length - filled_length)
                percent = progress * 100
                
                color = Fore.RED if percent < 30 else Fore.YELLOW if percent < 70 else Fore.GREEN
                sys.stdout.write(f"\r{text}: {color + Style.BRIGHT}[{bar}] {percent:.1f}%")
                sys.stdout.flush()
                time.sleep(duration / bar_length)
        finally:
            self.show_cursor()
            print(f"\n{Fore.GREEN + Style.BRIGHT}🎉 {text} Complete!")
    
    def _matrix_loading(self, text, duration):
        """Matrix-style loading effect"""
        matrix_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.hide_cursor()
        
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                line = f"{Fore.GREEN + Style.BRIGHT}{text}: "
                for _ in range(50):
                    if random.random() > 0.7:
                        line += random.choice(matrix_chars)
                    else:
                        line += " "
                
                sys.stdout.write(f"\r{line}")
                sys.stdout.flush()
                time.sleep(0.1)
        finally:
            self.show_cursor()
            print(f"\r{Fore.GREEN + Style.BRIGHT}{text}: Complete! 🚀" + " " * 50)
    
    def _pulse_loading(self, text, duration):
        """Pulsing text effect"""
        self.hide_cursor()
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                # Fade in
                for intensity in range(0, 10):
                    color = f"\033[38;5;{21 + intensity}m"  # Blue gradient
                    sys.stdout.write(f"\r{color + Style.BRIGHT}{text}")
                    sys.stdout.flush()
                    time.sleep(0.05)
                
                # Fade out
                for intensity in range(10, 0, -1):
                    color = f"\033[38;5;{21 + intensity}m"
                    sys.stdout.write(f"\r{color + Style.BRIGHT}{text}")
                    sys.stdout.flush()
                    time.sleep(0.05)
        finally:
            self.show_cursor()
            print(f"\r{Fore.GREEN + Style.BRIGHT}{text} Complete! ✨")
    
    def animated_progress_bar(self, current, total, length=50, prefix="Progress", animate=True):
        """Enhanced animated progress bar"""
        percent = (current / total) * 100
        filled_length = int(length * current // total)
        
        # Color gradient based on progress
        if percent < 25:
            color = Fore.RED
            emoji = "🔴"
        elif percent < 50:
            color = Fore.YELLOW
            emoji = "🟡"
        elif percent < 75:
            color = Fore.BLUE
            emoji = "🔵"
        else:
            color = Fore.GREEN
            emoji = "🟢"
        
        # Different bar styles
        if animate:
            bar_chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
            bar_fill = "".join([random.choice(bar_chars) for _ in range(filled_length)])
            bar = bar_fill + "░" * (length - filled_length)
        else:
            bar = "█" * filled_length + "░" * (length - filled_length)
        
        sys.stdout.write(f"\r{emoji} {prefix}: {color + Style.BRIGHT}[{bar}] {percent:.1f}% ({current}/{total})")
        sys.stdout.flush()
        
        if current == total:
            print(f"\n{Fore.GREEN + Style.BRIGHT}🎉 {prefix} Complete!")
    
    def attack_status_animation(self, attack_name, rps, duration=10, style="fire"):
        """Animated attack status display with multiple styles"""
        
        if style == "fire":
            self._fire_attack_animation(attack_name, rps, duration)
        elif style == "lightning":
            self._lightning_attack_animation(attack_name, rps, duration)
        elif style == "matrix":
            self._matrix_attack_animation(attack_name, rps, duration)
        elif style == "pulse":
            self._pulse_attack_animation(attack_name, rps, duration)
    
    def _fire_attack_animation(self, attack_name, rps, duration):
        """Fire-themed attack animation"""
        fire_symbols = ["🔥", "💥", "⚡", "🌟"]
        self.hide_cursor()
        
        try:
            for i in range(duration * 2):
                symbol = random.choice(fire_symbols)
                color = random.choice([Fore.RED, Fore.YELLOW, Fore.LIGHTRED_EX])
                intensity = "█" * random.randint(10, 30)
                
                sys.stdout.write(f"\r{color + Style.BRIGHT}{symbol} {attack_name} - RPS: {rps} {symbol} {intensity}")
                sys.stdout.flush()
                time.sleep(0.5)
        finally:
            self.show_cursor()
            print(f"\n{Fore.GREEN + Style.BRIGHT}✅ {attack_name} Status Updated!")
    
    def _lightning_attack_animation(self, attack_name, rps, duration):
        """Lightning-themed attack animation"""
        lightning_symbols = ["⚡", "🌩️", "💫", "✨"]
        self.hide_cursor()
        
        try:
            for i in range(duration):
                symbol = random.choice(lightning_symbols)
                # Create lightning effect
                lightning = "".join([random.choice("╱╲│─") for _ in range(20)])
                
                sys.stdout.write(f"\r{Fore.LIGHTBLUE_EX + Style.BRIGHT}{symbol} {attack_name} ⚡ RPS: {rps} ⚡ {lightning}")
                sys.stdout.flush()
                time.sleep(1)
        finally:
            self.show_cursor()
            print(f"\n{Fore.CYAN + Style.BRIGHT}⚡ {attack_name} Lightning Strike Complete!")
    
    def matrix_effect(self, lines=20, duration=5, intensity="medium"):
        """Advanced Matrix digital rain effect"""
        
        if intensity == "low":
            chars = "01"
            density = 0.3
        elif intensity == "medium":
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            density = 0.5
        else:  # high
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
            density = 0.8
        
        self.clear_screen()
        self.hide_cursor()
        
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                # Get terminal width
                try:
                    columns = os.get_terminal_size().columns
                except:
                    columns = 80
                
                line = ""
                for _ in range(columns):
                    if random.random() < density:
                        char = random.choice(chars)
                        # Random green shades
                        green_shade = random.choice([Fore.GREEN, Fore.LIGHTGREEN_EX, "\033[38;5;46m", "\033[38;5;82m"])
                        line += f"{green_shade}{char}"
                    else:
                        line += " "
                
                print(line)
                time.sleep(0.05)
        finally:
            self.show_cursor()
    
    def countdown_timer(self, seconds, message="Starting attack in", style="digital"):
        """Advanced countdown timer with multiple styles"""
        
        if style == "digital":
            self._digital_countdown(seconds, message)
        elif style == "analog":
            self._analog_countdown(seconds, message)
        elif style == "neon":
            self._neon_countdown(seconds, message)
    
    def _digital_countdown(self, seconds, message):
        """Digital-style countdown"""
        self.hide_cursor()
        
        try:
            for i in range(seconds, 0, -1):
                # Color coding for urgency
                if i <= 3:
                    color = Fore.RED + Style.BRIGHT
                    effect = "🚨"
                elif i <= 5:
                    color = Fore.YELLOW + Style.BRIGHT
                    effect = "⚠️"
                else:
                    color = Fore.GREEN + Style.BRIGHT
                    effect = "🕐"
                
                # Large digit display
                digit_art = self._get_large_digit(i)
                
                self.clear_screen()
                print(f"{color}{effect} {message}")
                print(f"{color}{digit_art}")
                print(f"{color}{'=' * 50}")
                
                time.sleep(1)
        finally:
            self.show_cursor()
            self.clear_screen()
            print(f"{Fore.GREEN + Style.BRIGHT}🚀 ATTACK LAUNCHED! 🚀")
    
    def _get_large_digit(self, digit):
        """Get ASCII art representation of digit"""
        digits = {
            1: ["  ██  ", " ███  ", "  ██  ", "  ██  ", "██████"],
            2: ["██████", "     ██", "██████", "██     ", "██████"],
            3: ["██████", "     ██", "██████", "     ██", "██████"],
            4: ["██   ██", "██   ██", "███████", "     ██", "     ██"],
            5: ["███████", "██     ", "███████", "     ██", "███████"],
            6: ["███████", "██     ", "███████", "██   ██", "███████"],
            7: ["███████", "     ██", "     ██", "     ██", "     ██"],
            8: ["███████", "██   ██", "███████", "██   ██", "███████"],
            9: ["███████", "██   ██", "███████", "     ██", "███████"],
            0: ["███████", "██   ██", "██   ██", "██   ██", "███████"]
        }
        
        return "\n".join(digits.get(digit, digits[0]))
    
    def success_celebration(self, message="SUCCESS", style="fireworks"):
        """Success celebration animation"""
        
        if style == "fireworks":
            self._fireworks_celebration(message)
        elif style == "confetti":
            self._confetti_celebration(message)
        elif style == "rainbow":
            self._rainbow_celebration(message)
    
    def _fireworks_celebration(self, message):
        """Fireworks-style success animation"""
        fireworks = ["✨", "🎆", "🎇", "💫", "⭐", "🌟"]
        self.clear_screen()
        
        # Create fireworks display
        for round in range(3):
            positions = [(random.randint(0, 60), random.randint(5, 15)) for _ in range(5)]
            
            for frame in range(10):
                self.clear_screen()
                
                # Title
                print(f"{Fore.YELLOW + Style.BRIGHT}{'🎉' * 20}")
                print(f"{Fore.GREEN + Style.BRIGHT}{message.center(60)}")
                print(f"{Fore.YELLOW + Style.BRIGHT}{'🎉' * 20}")
                print()
                
                # Fireworks
                for x, y in positions:
                    for i in range(frame + 1):
                        if y + i < 20:
                            line_content = " " * x + random.choice(fireworks)
                            print(f"{random.choice(self.bright_colors)}{line_content}")
                
                time.sleep(0.2)
        
        # Final message
        print(f"\n{Fore.GREEN + Style.BRIGHT}🏆 MISSION ACCOMPLISHED! 🏆")
    
    def error_alert(self, error_message, severity="high"):
        """Animated error alert system"""
        
        if severity == "high":
            color = Fore.RED + Style.BRIGHT
            symbol = "🚨"
            flash_count = 5
        elif severity == "medium":
            color = Fore.YELLOW + Style.BRIGHT
            symbol = "⚠️"
            flash_count = 3
        else:  # low
            color = Fore.BLUE + Style.BRIGHT
            symbol = "ℹ️"
            flash_count = 1
        
        self.hide_cursor()
        
        try:
            for i in range(flash_count):
                # Flash effect
                print(f"{color}{symbol} ERROR: {error_message} {symbol}")
                time.sleep(0.3)
                
                # Clear line and move cursor up
                sys.stdout.write("\033[K")  # Clear line
                sys.stdout.write("\033[A")  # Move up
                print(" " * 80)  # Clear with spaces
                sys.stdout.write("\033[A")  # Move up again
                time.sleep(0.3)
        finally:
            self.show_cursor()
            print(f"{color}❌ {error_message}")
    
    def live_statistics_display(self, stats_callback, update_interval=1, duration=None):
        """Live updating statistics display with animations"""
        self.animation_running = True
        self.hide_cursor()
        
        try:
            start_time = time.time()
            
            while self.animation_running:
                if duration and (time.time() - start_time) > duration:
                    break
                
                stats = stats_callback()
                self.clear_screen()
                
                # Header with animation
                header_chars = ["▰", "▱"]
                animated_border = "".join([random.choice(header_chars) for _ in range(80)])
                
                print(f"{Fore.CYAN + Style.BRIGHT}{animated_border}")
                print(f"{Fore.CYAN + Style.BRIGHT}{'📊 REAL-TIME STATISTICS 📊'.center(80)}")
                print(f"{Fore.CYAN + Style.BRIGHT}{animated_border}")
                print()
                
                # Display stats with color coding and animations
                for key, value in stats.items():
                    # Format key
                    formatted_key = key.replace('_', ' ').title()
                    
                    # Color coding based on key type
                    if 'success' in key.lower() or 'rate' in key.lower():
                        color = Fore.GREEN if float(str(value).replace('%', '')) > 80 else Fore.YELLOW
                    elif 'error' in key.lower() or 'fail' in key.lower():
                        color = Fore.RED if int(str(value)) > 0 else Fore.GREEN
                    elif 'speed' in key.lower() or 'rps' in key.lower():
                        color = Fore.BLUE
                    else:
                        color = Fore.WHITE
                    
                    # Animated value display
                    bar_length = min(50, int(float(str(value).replace('%', '').replace(',', '')) / 10))
                    animated_bar = "█" * bar_length
                    
                    print(f"{color + Style.BRIGHT}{formatted_key:.<30} {value}")
                    if bar_length > 0:
                        print(f"{color}{animated_bar}")
                    print()
                
                print(f"{Fore.CYAN + Style.BRIGHT}{animated_border}")
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.animation_running = False
            self.show_cursor()
    
    def stop_live_display(self):
        """Stop live statistics display"""
        self.animation_running = False
    
    def glitch_effect(self, text, duration=3, intensity="medium"):
        """Advanced glitch text effect"""
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`¡¿αβγδεζηθικλμνξοπρστυφχψω"
        
        if intensity == "low":
            glitch_probability = 0.1
        elif intensity == "medium":
            glitch_probability = 0.2
        else:  # high
            glitch_probability = 0.4
        
        self.hide_cursor()
        original = list(text)
        
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                glitched = original.copy()
                
                # Apply glitch effects
                for i in range(len(glitched)):
                    if random.random() < glitch_probability:
                        glitched[i] = random.choice(glitch_chars)
                
                # Random color and positioning
                color = random.choice(self.colors + self.bright_colors)
                offset = random.choice([0, 1, -1, 2, -2])
                
                display_text = "".join(glitched)
                sys.stdout.write(f"\r{' ' * max(0, offset)}{color + Style.BRIGHT}{display_text}")
                sys.stdout.flush()
                time.sleep(0.05)
        finally:
            self.show_cursor()
            # Show original text
            print(f"\r{Fore.GREEN + Style.BRIGHT}{''.join(original)}")
    
    def typewriter_effect(self, text, delay=0.03, color=Fore.GREEN):
        """Enhanced typewriter animation with sound-like pauses"""
        
        for i, char in enumerate(text):
            sys.stdout.write(f"{color + Style.BRIGHT}{char}")
            sys.stdout.flush()
            
            # Variable delay based on character type
            if char in '.!?':
                time.sleep(delay * 10)  # Longer pause for sentence endings
            elif char in ',;:':
                time.sleep(delay * 5)   # Medium pause for punctuation
            elif char == ' ':
                time.sleep(delay * 2)   # Slight pause for spaces
            else:
                time.sleep(delay)       # Normal typing speed
        
        print()  # New line at the end
    
    def network_activity_visualization(self, packets_per_second, duration=10):
        """Visualize network activity with animated packets"""
        self.clear_screen()
        self.hide_cursor()
        
        try:
            start_time = time.time()
            packet_chars = ["◆", "◇", "●", "○", "▲", "△"]
            
            while time.time() - start_time < duration:
                self.clear_screen()
                
                # Header
                print(f"{Fore.CYAN + Style.BRIGHT}{'═' * 80}")
                print(f"{Fore.CYAN + Style.BRIGHT}{'🌐 NETWORK ACTIVITY MONITOR 🌐'.center(80)}")
                print(f"{Fore.CYAN + Style.BRIGHT}{'═' * 80}")
                print()
                
                # Simulate packet flow
                for line in range(15):
                    flow_line = ""
                    for pos in range(70):
                        if random.random() < (packets_per_second / 1000):
                            packet = random.choice(packet_chars)
                            color = random.choice([Fore.GREEN, Fore.YELLOW, Fore.RED])
                            flow_line += f"{color + Style.BRIGHT}{packet}"
                        else:
                            flow_line += " "
                    
                    print(f"│{flow_line}│")
                
                # Footer with stats
                print(f"{Fore.CYAN + Style.BRIGHT}{'═' * 80}")
                print(f"{Fore.GREEN + Style.BRIGHT}📊 Packets/sec: {packets_per_second} | 🎯 Target Load: {'High' if packets_per_second > 500 else 'Medium' if packets_per_second > 100 else 'Low'}")
                
                time.sleep(0.1)
        finally:
            self.show_cursor()

def demo_all_animations():
    """Demonstrate all available animations"""
    fx = VisualEffects()
    
    print(f"{Fore.MAGENTA + Style.BRIGHT}🎬 ANIMATION SHOWCASE STARTING...\n")
    time.sleep(2)
    
    # Loading animations
    print(f"{Fore.YELLOW}🔄 LOADING ANIMATIONS:")
    fx.loading_animation("Dots Loading", 2, "dots")
    fx.loading_animation("Spinner Loading", 2, "spinner")
    fx.loading_animation("Progress Loading", 2, "progress")
    fx.loading_animation("Matrix Loading", 2, "matrix")
    fx.loading_animation("Pulse Loading", 2, "pulse")
    
    # Progress bar
    print(f"\n{Fore.YELLOW}📊 PROGRESS BAR DEMO:")
    for i in range(101):
        fx.animated_progress_bar(i, 100, prefix="Demo Progress", animate=True)
        time.sleep(0.02)
    
    # Countdown
    print(f"\n{Fore.YELLOW}⏰ COUNTDOWN DEMO:")
    fx.countdown_timer(5, "Demo starting in", "digital")
    
    # Attack animation
    print(f"{Fore.YELLOW}⚡ ATTACK ANIMATIONS:")
    fx.attack_status_animation("HTTP Flood", 1500, 3, "fire")
    
    # Matrix effect
    print(f"{Fore.YELLOW}📱 MATRIX EFFECT:")
    fx.matrix_effect(10, 3, "medium")
    
    # Success celebration
    print(f"{Fore.YELLOW}🎉 SUCCESS ANIMATION:")
    fx.success_celebration("DEMO COMPLETE", "fireworks")
    
    # Glitch effect
    print(f"\n{Fore.YELLOW}👾 GLITCH EFFECT:")
    fx.glitch_effect("DDOS EDUCATIONAL TOOLKIT BY RAJSARASWATI JATAV", 3, "medium")
    
    # Typewriter
    print(f"\n{Fore.YELLOW}⌨️ TYPEWRITER EFFECT:")
    fx.typewriter_effect("Thank you for using Rajsaraswati Jatav's DDOS Educational Toolkit!", 0.05)
    
    print(f"\n{Fore.GREEN + Style.BRIGHT}✅ ALL ANIMATIONS DEMONSTRATED SUCCESSFULLY!")
    print(f"{Fore.CYAN}🎯 Ready for educational testing and ethical hacking practice!")

if __name__ == "__main__":
    demo_all_animations()
