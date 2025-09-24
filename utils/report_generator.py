#!/usr/bin/env python3
"""
DDOS Attack Educational Toolkit - Report Generator
Author: Rajsaraswati Jatav
Purpose: Generate comprehensive analysis reports
"""

import json
import csv
import os
from datetime import datetime
from utils.statistics import Statistics
from utils.logger import Logger

class ReportGenerator:
    def __init__(self):
        self.logger = Logger()
        self.stats = Statistics()
        
    def generate_html_report(self, attack_id=None, filename=None):
        """Generate professional HTML report"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"attack_report_{timestamp}.html"
        
        try:
            if attack_id:
                stats = self.stats.get_attack_stats(attack_id)
                html_content = self._create_attack_html_report(attack_id, stats)
            else:
                global_stats = self.stats.get_global_stats()
                html_content = self._create_global_html_report(global_stats)
            
            # Create reports directory if it doesn't exist
            os.makedirs('reports', exist_ok=True)
            filepath = os.path.join('reports', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML report generated: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
            return None
    
    def _create_attack_html_report(self, attack_id, stats):
        """Create detailed HTML report for specific attack"""
        if not stats:
            return "<html><body><h1>Attack Statistics Not Available</h1></body></html>"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DDOS Attack Report - {attack_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            animation: grain 20s linear infinite;
            pointer-events: none;
        }}
        
        @keyframes grain {{
            0%, 100% {{ transform: translate(0, 0); }}
            10% {{ transform: translate(-5%, -5%); }}
            20% {{ transform: translate(-10%, 5%); }}
            30% {{ transform: translate(5%, -10%); }}
            40% {{ transform: translate(-5%, 15%); }}
            50% {{ transform: translate(-10%, 5%); }}
            60% {{ transform: translate(15%, 0%); }}
            70% {{ transform: translate(0%, 15%); }}
            80% {{ transform: translate(-15%, 10%); }}
            90% {{ transform: translate(10%, 5%); }}
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }}
        
        .header h2 {{
            font-size: 1.5em;
            margin-bottom: 15px;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }}
        
        .header p {{
            opacity: 0.8;
            position: relative;
            z-index: 1;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }}
        
        .metric-card {{
            background: #ffffff;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .metric-title {{
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 600;
        }}
        
        .metric-value {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .metric-change {{
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 12px;
            font-weight: 500;
        }}
        
        .success {{ 
            color: #38a169; 
            background: #f0fff4;
        }}
        .warning {{ 
            color: #d69e2e; 
            background: #fffbf0;
        }}
        .error {{ 
            color: #e53e3e; 
            background: #fff5f5;
        }}
        
        .section {{
            background: #ffffff;
            margin: 25px 0;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            font-weight: 600;
            text-align: left;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        tr:nth-child(even) {{
            background-color: #f7fafc;
        }}
        
        .progress-container {{
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            height: 8px;
            margin: 8px 0;
        }}
        
        .progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, #38a169, #68d391);
            border-radius: 10px;
            transition: width 0.3s ease;
        }}
        
        .error-list {{
            background: #fff5f5;
            border: 1px solid #fed7d7;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: #f7fafc;
            color: #666;
            border-top: 1px solid #e2e8f0;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .status-running {{ background: #bee3f8; color: #2c5282; }}
        .status-completed {{ background: #c6f6d5; color: #22543d; }}
        .status-failed {{ background: #fed7d7; color: #742a2a; }}
        
        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 2em;
            }}
            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 DDOS Attack Analysis Report</h1>
            <h2>Attack ID: {attack_id}</h2>
            <p>Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M:%S IST')}</p>
            <p><strong>Created by: Rajsaraswati Jatav</strong> | Educational Testing Only</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Performance Overview</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">Total Requests</div>
                        <div class="metric-value">{stats['requests_sent']:,}</div>
                        <div class="metric-change success">
                            📈 {stats['requests_sent']} sent
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">Success Rate</div>
                        <div class="metric-value {'success' if stats['success_rate'] > 80 else 'warning' if stats['success_rate'] > 50 else 'error'}">{stats['success_rate']:.1f}%</div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {stats['success_rate']}%;"></div>
                        </div>
                        <div class="metric-change {'success' if stats['success_rate'] > 80 else 'warning'}">
                            {'🎉 Excellent' if stats['success_rate'] > 80 else '⚠️ Needs improvement' if stats['success_rate'] > 50 else '❌ Poor performance'}
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">Average RPS</div>
                        <div class="metric-value">{stats['requests_per_second_avg']:.1f}</div>
                        <div class="metric-change {'success' if stats['requests_per_second_avg'] > 50 else 'warning'}">
                            {'🚀 High speed' if stats['requests_per_second_avg'] > 50 else '💡 Can optimize'}
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">Duration</div>
                        <div class="metric-value">{stats['duration']:.1f}s</div>
                        <div class="metric-change success">
                            ⏱️ {self._format_duration(stats['duration'])}
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">Data Transmitted</div>
                        <div class="metric-value">{self._format_bytes(stats['bytes_sent'])}</div>
                        <div class="metric-change success">
                            📡 Total bandwidth used
                        </div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-title">Average Response Time</div>
                        <div class="metric-value">{stats['avg_response_time']:.3f}s</div>
                        <div class="metric-change {'success' if stats['avg_response_time'] < 1 else 'warning'}">
                            {'⚡ Fast' if stats['avg_response_time'] < 1 else '🐌 Slow'}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 Attack Configuration Details</h2>
                <table>
                    <tr><th>Parameter</th><th>Value</th><th>Status</th></tr>
                    <tr>
                        <td>Target</td>
                        <td>{stats.get('target', 'Unknown')}</td>
                        <td><span class="badge status-completed">Configured</span></td>
                    </tr>
                    <tr>
                        <td>Attack Type</td>
                        <td>{stats.get('attack_type', 'Unknown')}</td>
                        <td><span class="badge status-completed">Active</span></td>
                    </tr>
                    <tr>
                        <td>Status</td>
                        <td>{stats['status'].title()}</td>
                        <td><span class="badge status-{'completed' if stats['status'] == 'completed' else 'running'}">{stats['status'].title()}</span></td>
                    </tr>
                    <tr>
                        <td>Start Time</td>
                        <td>{datetime.fromtimestamp(stats['start_time']).strftime('%Y-%m-%d %H:%M:%S')}</td>
                        <td><span class="badge status-completed">Recorded</span></td>
                    </tr>
                    <tr>
                        <td>End Time</td>
                        <td>{datetime.fromtimestamp(stats['end_time']).strftime('%Y-%m-%d %H:%M:%S') if stats.get('end_time') else 'Still Running'}</td>
                        <td><span class="badge status-{'completed' if stats.get('end_time') else 'running'}">{'Completed' if stats.get('end_time') else 'Active'}</span></td>
                    </tr>
                    <tr>
                        <td>Thread Count</td>
                        <td>{stats.get('thread_count', 'Auto')}</td>
                        <td><span class="badge status-completed">Optimized</span></td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>📈 Performance Analysis</h2>
                <table>
                    <tr><th>Metric</th><th>Value</th><th>Rating</th></tr>
                    <tr>
                        <td>🎯 Successful Requests</td>
                        <td>{stats['successful_requests']:,}</td>
                        <td><span class="success">✅ Excellent</span></td>
                    </tr>
                    <tr>
                        <td>❌ Failed Requests</td>
                        <td>{stats['failed_requests']:,}</td>
                        <td><span class="{'success' if stats['failed_requests'] == 0 else 'warning' if stats['failed_requests'] < stats['successful_requests'] * 0.1 else 'error'}">
                            {'✅ Perfect' if stats['failed_requests'] == 0 else '⚠️ Acceptable' if stats['failed_requests'] < stats['successful_requests'] * 0.1 else '❌ High failure rate'}
                        </span></td>
                    </tr>
                    <tr>
                        <td>⚡ Current RPS</td>
                        <td>{stats.get('current_rps', 0)}</td>
                        <td><span class="{'success' if stats.get('current_rps', 0) > 10 else 'warning'}">
                            {'🚀 High performance' if stats.get('current_rps', 0) > 10 else '💡 Can improve'}
                        </span></td>
                    </tr>
                    <tr>
                        <td>📊 Min Response Time</td>
                        <td>{stats['min_response_time']:.3f}s</td>
                        <td><span class="success">⚡ Optimal</span></td>
                    </tr>
                    <tr>
                        <td>📊 Max Response Time</td>
                        <td>{stats['max_response_time']:.3f}s</td>
                        <td><span class="{'success' if stats['max_response_time'] < 2 else 'warning' if stats['max_response_time'] < 5 else 'error'}">
                            {'✅ Fast' if stats['max_response_time'] < 2 else '⚠️ Moderate' if stats['max_response_time'] < 5 else '🐌 Slow'}
                        </span></td>
                    </tr>
                    <tr>
                        <td>💾 Data Sent</td>
                        <td>{self._format_bytes(stats['bytes_sent'])}</td>
                        <td><span class="success">📡 Transmitted</span></td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>🔍 Educational Analysis</h2>
                <div style="background: #f7fafc; padding: 25px; border-radius: 10px; border-left: 4px solid #4299e1;">
                    <h3 style="color: #2d3748; margin-bottom: 15px;">📚 Learning Outcomes:</h3>
"""
        
        # Educational analysis based on results
        if stats['success_rate'] > 90:
            html += "<p><strong>🎉 Excellent Results:</strong> High success rate indicates effective attack simulation. This demonstrates how unprotected systems can be overwhelmed.</p>"
        elif stats['success_rate'] > 70:
            html += "<p><strong>⚠️ Good Results:</strong> Moderate success rate shows some defensive measures may be in place. This is educational for understanding mitigation strategies.</p>"
        else:
            html += "<p><strong>🛡️ Low Success Rate:</strong> Target appears well-protected or network issues exist. This demonstrates the importance of proper security measures.</p>"
            
        if stats['requests_per_second_avg'] > 100:
            html += "<p><strong>⚡ High Performance:</strong> Tool demonstrated capability to generate significant load, useful for capacity planning studies.</p>"
        else:
            html += "<p><strong>💡 Performance Note:</strong> Lower RPS may indicate network limitations or target throttling - important considerations for real-world scenarios.</p>"
            
        html += f"""
                    <h3 style="color: #2d3748; margin: 20px 0 15px 0;">🎯 Security Insights:</h3>
                    <ul style="margin-left: 20px; line-height: 1.6;">
                        <li><strong>Attack Effectiveness:</strong> {'High impact potential' if stats['success_rate'] > 80 else 'Moderate impact' if stats['success_rate'] > 50 else 'Low impact - good defenses'}</li>
                        <li><strong>Resource Usage:</strong> {self._format_bytes(stats['bytes_sent'])} transmitted - shows bandwidth requirements</li>
                        <li><strong>Detection Likelihood:</strong> {'High' if stats['requests_per_second_avg'] > 1000 else 'Medium' if stats['requests_per_second_avg'] > 100 else 'Low'} - based on traffic volume</li>
                        <li><strong>Defense Recommendations:</strong> Rate limiting, traffic filtering, load balancing, DDoS protection services</li>
                    </ul>
                    
                    <div style="margin-top: 20px; padding: 15px; background: #fff5f5; border-radius: 8px; border: 1px solid #fed7d7;">
                        <p><strong>⚠️ Ethical Reminder:</strong> This analysis is for educational purposes. In real penetration testing, these findings would be reported to system owners with recommendations for improvement.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>📊 Professional Report Generated by Rajsaraswati Jatav's DDOS Educational Toolkit</strong></p>
            <p>🎓 Designed for cybersecurity education and authorized ethical testing</p>
            <p>⚖️ Always ensure proper authorization and follow applicable laws</p>
            <p style="margin-top: 10px; font-size: 12px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def generate_csv_report(self, filename=None):
        """Generate CSV report with all attack data"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"attack_data_{timestamp}.csv"
        
        try:
            os.makedirs('reports', exist_ok=True)
            filepath = os.path.join('reports', filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Headers
                writer.writerow([
                    'Attack_ID', 'Status', 'Start_Time', 'End_Time', 'Duration_Seconds',
                    'Target', 'Attack_Type', 'Thread_Count', 'Total_Requests',
                    'Successful_Requests', 'Failed_Requests', 'Success_Rate_Percent',
                    'Average_RPS', 'Current_RPS', 'Bytes_Sent', 'Avg_Response_Time_Seconds',
                    'Min_Response_Time', 'Max_Response_Time', 'Top_Error_Type'
                ])
                
                # Data rows
                for attack_id in self.stats.attack_stats:
                    stats = self.stats.get_attack_stats(attack_id)
                    if stats:
                        # Get top error
                        errors = stats.get('errors', {})
                        top_error = max(errors.keys(), key=lambda k: errors[k]) if errors else 'None'
                        
                        writer.writerow([
                            attack_id,
                            stats['status'],
                            datetime.fromtimestamp(stats['start_time']).strftime('%Y-%m-%d %H:%M:%S'),
                            datetime.fromtimestamp(stats['end_time']).strftime('%Y-%m-%d %H:%M:%S') if stats.get('end_time') else 'N/A',
                            f"{stats['duration']:.2f}",
                            stats.get('target', 'Unknown'),
                            stats.get('attack_type', 'Unknown'),
                            stats.get('thread_count', 0),
                            stats['requests_sent'],
                            stats['successful_requests'],
                            stats['failed_requests'],
                            f"{stats['success_rate']:.2f}",
                            f"{stats['requests_per_second_avg']:.2f}",
                            stats.get('current_rps', 0),
                            stats['bytes_sent'],
                            f"{stats['avg_response_time']:.3f}",
                            f"{stats['min_response_time']:.3f}",
                            f"{stats['max_response_time']:.3f}",
                            top_error
                        ])
            
            self.logger.info(f"CSV report generated: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to generate CSV report: {e}")
            return None
    
    def generate_json_report(self, attack_id=None, filename=None):
        """Generate comprehensive JSON report"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            suffix = f"_{attack_id}" if attack_id else "_global"
            filename = f"attack_report{suffix}_{timestamp}.json"
        
        try:
            os.makedirs('reports', exist_ok=True)
            filepath = os.path.join('reports', filename)
            
            if attack_id:
                data = {
                    'report_metadata': {
                        'report_type': 'attack_specific',
                        'attack_id': attack_id,
                        'generated_at': datetime.now().isoformat(),
                        'generated_by': 'Rajsaraswati Jatav DDOS Educational Toolkit',
                        'version': '2.0',
                        'purpose': 'Educational and Ethical Testing Only'
                    },
                    'attack_statistics': self.stats.get_attack_stats(attack_id),
                    'error_analysis': dict(self.stats.attack_stats[attack_id]['errors']) if attack_id in self.stats.attack_stats else {},
                    'performance_insights': {
                        'efficiency_rating': self._calculate_efficiency_rating(attack_id),
                        'performance_grade': self._calculate_performance_grade(attack_id),
                        'recommendations': self._generate_recommendations(attack_id)
                    }
                }
            else:
                # Global report
                data = {
                    'report_metadata': {
                        'report_type': 'global_summary',
                        'generated_at': datetime.now().isoformat(),
                        'generated_by': 'Rajsaraswati Jatav DDOS Educational Toolkit',
                        'version': '2.0',
                        'purpose': 'Educational and Ethical Testing Only'
                    },
                    'global_statistics': self.stats.get_global_stats(),
                    'all_attacks': {aid: self.stats.get_attack_stats(aid) for aid in self.stats.attack_stats},
                    'summary_analysis': {
                        'total_attacks_conducted': len(self.stats.attack_stats),
                        'overall_success_rate': self._calculate_overall_success_rate(),
                        'peak_performance_attack': self._find_best_performing_attack(),
                        'educational_insights': self._generate_educational_insights()
                    }
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            
            self.logger.info(f"JSON report generated: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {e}")
            return None
    
    def generate_summary_text_report(self, attack_ids=None):
        """Generate text-based summary report"""
        if attack_ids is None:
            attack_ids = list(self.stats.attack_stats.keys())
        
        if not attack_ids:
            return "No attack data available for report generation."
        
        report = f"""
🎯 DDOS EDUCATIONAL TOOLKIT - SUMMARY REPORT
============================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
Created by: Rajsaraswati Jatav
Purpose: Educational Analysis Only

📊 GLOBAL STATISTICS
===================
Total Attacks Conducted: {len(attack_ids)}
Global Success Rate: {self._calculate_overall_success_rate():.1f}%
Total Requests Sent: {sum(self.stats.get_attack_stats(aid)['requests_sent'] for aid in attack_ids if self.stats.get_attack_stats(aid)):,}
Peak Performance Attack: {self._find_best_performing_attack()}

🎯 INDIVIDUAL ATTACK SUMMARY
===========================
"""
        
        for attack_id in attack_ids:
            stats = self.stats.get_attack_stats(attack_id)
            if stats:
                report += f"""
Attack ID: {attack_id}
├─ Status: {stats['status'].title()}
├─ Duration: {stats['duration']:.1f}s
├─ Requests: {stats['requests_sent']:,} (Success: {stats['success_rate']:.1f}%)
├─ Average RPS: {stats['requests_per_second_avg']:.1f}
├─ Response Time: {stats['avg_response_time']:.3f}s
└─ Rating: {self._calculate_performance_grade(attack_id)}

"""
        
        report += f"""
🎓 EDUCATIONAL INSIGHTS
======================
1. High success rates indicate vulnerable systems
2. Low RPS may suggest good rate limiting
3. Fast response times show server efficiency
4. Error patterns reveal defense mechanisms

⚖️ ETHICAL REMINDER
==================
This analysis is for educational purposes only.
Always ensure proper authorization before testing.
Follow responsible disclosure practices.

📞 SUPPORT
==========
GitHub: github.com/RAJSARASWATI-JATAV/DDOS-ATTACK-EDUCATIONAL
Email: rajsaraswati.jatav@gmail.com
YouTube: @rajsaraswatijatav

Generated by Rajsaraswati Jatav's DDOS Educational Toolkit v2.0
"""
        
        return report
    
    def _format_bytes(self, bytes_count):
        """Format bytes in human readable format"""
        if bytes_count == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.2f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.2f} PB"
    
    def _format_duration(self, seconds):
        """Format duration in readable format"""
        if seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.0f} minutes {seconds%60:.0f} seconds"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"
    
    def _calculate_efficiency_rating(self, attack_id):
        """Calculate efficiency rating for attack"""
        stats = self.stats.get_attack_stats(attack_id)
        if not stats:
            return 0
        
        # Weighted score based on success rate and performance
        success_score = stats['success_rate'] / 100 * 50
        speed_score = min(stats['requests_per_second_avg'] / 100, 1) * 30
        response_score = max(0, (2 - stats['avg_response_time']) / 2) * 20
        
        return min(100, success_score + speed_score + response_score)
    
    def _calculate_performance_grade(self, attack_id):
        """Calculate letter grade for attack performance"""
        rating = self._calculate_efficiency_rating(attack_id)
        
        if rating >= 90:
            return "A+ (Excellent)"
        elif rating >= 80:
            return "A (Very Good)"
        elif rating >= 70:
            return "B (Good)"
        elif rating >= 60:
            return "C (Average)"
        elif rating >= 50:
            return "D (Below Average)"
        else:
            return "F (Poor)"
    
    def _calculate_overall_success_rate(self):
        """Calculate overall success rate across all attacks"""
        total_requests = 0
        total_successful = 0
        
        for attack_id in self.stats.attack_stats:
            stats = self.stats.get_attack_stats(attack_id)
            if stats:
                total_requests += stats['requests_sent']
                total_successful += stats['successful_requests']
        
        return (total_successful / total_requests * 100) if total_requests > 0 else 0
    
    def _find_best_performing_attack(self):
        """Find the best performing attack based on efficiency"""
        best_attack = None
        best_rating = 0
        
        for attack_id in self.stats.attack_stats:
            rating = self._calculate_efficiency_rating(attack_id)
            if rating > best_rating:
                best_rating = rating
                best_attack = attack_id
        
        return best_attack if best_attack else "No attacks found"
    
    def _generate_recommendations(self, attack_id):
        """Generate recommendations based on attack results"""
        stats = self.stats.get_attack_stats(attack_id)
        if not stats:
            return []
        
        recommendations = []
        
        # Success rate based recommendations
        if stats['success_rate'] < 50:
            recommendations.append("Consider checking target accessibility and network connectivity")
            recommendations.append("Verify that target system is not over-protected for educational testing")
        elif stats['success_rate'] > 95:
            recommendations.append("High success rate indicates vulnerable target - good for educational demonstration")
            recommendations.append("Consider implementing rate limiting and DDoS protection as learning exercise")
        
        # Performance based recommendations
        if stats['requests_per_second_avg'] < 10:
            recommendations.append("Low RPS detected - consider increasing thread count or checking network bandwidth")
            recommendations.append("System resources may be limiting - monitor CPU and memory usage")
        elif stats['requests_per_second_avg'] > 1000:
            recommendations.append("Very high RPS achieved - excellent for demonstrating attack capabilities")
            recommendations.append("This level of traffic would be easily detected by monitoring systems")
        
        # Response time recommendations
        if stats['avg_response_time'] > 5:
            recommendations.append("High response times may indicate target system stress or network latency")
            recommendations.append("Consider adjusting attack parameters or testing with different targets")
        
        # Educational recommendations
        recommendations.extend([
            "Document these results for educational analysis and discussion",
            "Compare with different attack types to understand various impact patterns",
            "Use results to design and test defensive countermeasures",
            "Consider the ethical implications and legal requirements of such testing"
        ])
        
        return recommendations
    
    def _generate_educational_insights(self):
        """Generate educational insights from all attacks"""
        insights = []
        
        if len(self.stats.attack_stats) > 1:
            insights.append("Multiple attack types tested - comprehensive security assessment approach")
        
        overall_success = self._calculate_overall_success_rate()
        if overall_success > 80:
            insights.append("High overall success rate indicates need for improved DDoS defenses")
        elif overall_success < 30:
            insights.append("Low success rate suggests effective security measures in place")
        
        insights.extend([
            "This toolkit demonstrates various attack vectors for educational understanding",
            "Results show importance of multi-layered security approach",
            "Performance data useful for capacity planning and defense strategy",
            "Always conduct such testing only with proper authorization and ethical guidelines"
        ])
        
        return insights
    
    def export_all_reports(self, attack_id=None):
        """Generate all report formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        reports = {}
        
        # HTML Report
        html_file = self.generate_html_report(attack_id)
        if html_file:
            reports['html'] = html_file
        
        # CSV Report (only for global)
        if not attack_id:
            csv_file = self.generate_csv_report()
            if csv_file:
                reports['csv'] = csv_file
        
        # JSON Report
        json_file = self.generate_json_report(attack_id)
        if json_file:
            reports['json'] = json_file
        
        # Text Summary
        try:
            summary_filename = f"reports/summary_{timestamp}.txt"
            summary_content = self.generate_summary_text_report([attack_id] if attack_id else None)
            
            with open(summary_filename, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            reports['summary'] = summary_filename
            self.logger.info(f"Text summary generated: {summary_filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate text summary: {e}")
        
        return reports
