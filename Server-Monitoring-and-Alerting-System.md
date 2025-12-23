# Server Monitoring and Alerting System Documentation

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [Monitoring Components](#monitoring-components)
7. [Alert System](#alert-system)
8. [Maintenance Tasks](#maintenance-tasks)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)
11. [Appendix](#appendix)

---

## Overview

### Purpose
This documentation describes the implementation of a comprehensive server monitoring and alerting system designed to prevent critical incidents such as disk space exhaustion, database crashes, and system failures.

### Key Features
- **Real-time Monitoring**: Track CPU, memory, disk, and database metrics
- **Automated Alerts**: Email notifications when thresholds are exceeded
- **Automated Cleanup**: Regular removal of old logs, backups, and temporary files
- **Dashboard Visualization**: Grafana dashboards for metric visualization
- **Proactive Maintenance**: Scheduled database optimization and system health checks

### Incident Reference
This system was developed in response to the **December 22, 2025 incident** where:
- Database server crashed due to insufficient disk space
- NSE trade file download failed
- All trades were auto-approved without ban list verification
- 3 compliance violations occurred (banned securities traded)

---

## System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Monitoring System                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Frappe     │  │  Prometheus  │  │   Grafana    │     │
│  │  Monitoring  │  │ Node Exporter│  │  Dashboard   │     │
│  │   Module     │  │              │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌──────────────────────────────────────────────────┐      │
│  │           Server Metrics Collection              │      │
│  │  - CPU Usage                                     │      │
│  │  - Memory Usage                                  │      │
│  │  - Disk Usage                                    │      │
│  │  - Database Size                                 │      │
│  │  - Network Traffic                               │      │
│  └──────────────────┬───────────────────────────────┘      │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────────┐      │
│  │         Threshold Checking & Alerts              │      │
│  │  - Compare with configured thresholds            │      │
│  │  - Generate alerts for violations                │      │
│  │  - Send email notifications                      │      │
│  └──────────────────┬───────────────────────────────┘      │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────────┐      │
│  │        Automated Maintenance Tasks               │      │
│  │  - Log cleanup (daily)                           │      │
│  │  - Backup cleanup (weekly)                       │      │
│  │  - Database optimization (weekly)                │      │
│  │  - Temp file removal (daily)                     │      │
│  └──────────────────────────────────────────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### System Requirements
- **Operating System**: Ubuntu 20.04 LTS or later
- **Python**: 3.8 or higher
- **Frappe Framework**: v14 or v15
- **Database**: MariaDB 10.6+ or MySQL 8.0+
- **Disk Space**: Minimum 50GB free space
- **Memory**: Minimum 4GB RAM (8GB recommended)

### Required Packages
```bash
# System packages
sudo apt-get install -y sysstat htop iotop nethogs

# Python packages
pip install psutil --break-system-packages
```

### User Permissions
- Root or sudo access for system monitoring tools
- Database access for metrics collection
- Email/SMTP access for alert notifications

---

## Installation Guide

### Step 1: Create Frappe App Structure
```bash
# Navigate to Frappe bench
cd ~/frappe-bench

# Create new app (if not exists)
bench new-app monitoring_system

# Install app to site
bench --site your-site install-app monitoring_system
```

### Step 2: Create Required DocTypes

#### 2.1 Server Monitoring DocType

Create file: `monitoring_system/monitoring_system/doctype/server_monitoring/server_monitoring.json`
```json
{
 "actions": [],
 "creation": "2025-12-23 12:00:00",
 "doctype": "DocType",
 "engine": "InnoDB",
 "field_order": [
  "timestamp",
  "section_break_2",
  "cpu_percent",
  "cpu_count",
  "column_break_4",
  "memory_total_gb",
  "memory_used_gb",
  "memory_percent",
  "section_break_8",
  "disk_total_gb",
  "disk_used_gb",
  "disk_free_gb",
  "disk_percent",
  "column_break_13",
  "database_size_mb",
  "network_sent_mb",
  "network_recv_mb"
 ],
 "fields": [
  {
   "fieldname": "timestamp",
   "fieldtype": "Datetime",
   "label": "Timestamp",
   "reqd": 1
  },
  {
   "fieldname": "section_break_2",
   "fieldtype": "Section Break",
   "label": "CPU Metrics"
  },
  {
   "fieldname": "cpu_percent",
   "fieldtype": "Float",
   "label": "CPU Usage (%)",
   "precision": "2"
  },
  {
   "fieldname": "cpu_count",
   "fieldtype": "Int",
   "label": "CPU Count"
  },
  {
   "fieldname": "column_break_4",
   "fieldtype": "Column Break"
  },
  {
   "fieldname": "memory_total_gb",
   "fieldtype": "Float",
   "label": "Total Memory (GB)",
   "precision": "2"
  },
  {
   "fieldname": "memory_used_gb",
   "fieldtype": "Float",
   "label": "Used Memory (GB)",
   "precision": "2"
  },
  {
   "fieldname": "memory_percent",
   "fieldtype": "Float",
   "label": "Memory Usage (%)",
   "precision": "2"
  },
  {
   "fieldname": "section_break_8",
   "fieldtype": "Section Break",
   "label": "Disk & Database Metrics"
  },
  {
   "fieldname": "disk_total_gb",
   "fieldtype": "Float",
   "label": "Total Disk (GB)",
   "precision": "2"
  },
  {
   "fieldname": "disk_used_gb",
   "fieldtype": "Float",
   "label": "Used Disk (GB)",
   "precision": "2"
  },
  {
   "fieldname": "disk_free_gb",
   "fieldtype": "Float",
   "label": "Free Disk (GB)",
   "precision": "2"
  },
  {
   "fieldname": "disk_percent",
   "fieldtype": "Float",
   "label": "Disk Usage (%)",
   "precision": "2"
  },
  {
   "fieldname": "column_break_13",
   "fieldtype": "Column Break"
  },
  {
   "fieldname": "database_size_mb",
   "fieldtype": "Float",
   "label": "Database Size (MB)",
   "precision": "2"
  },
  {
   "fieldname": "network_sent_mb",
   "fieldtype": "Float",
   "label": "Network Sent (MB)",
   "precision": "2"
  },
  {
   "fieldname": "network_recv_mb",
   "fieldtype": "Float",
   "label": "Network Received (MB)",
   "precision": "2"
  }
 ],
 "modified": "2025-12-23 12:00:00",
 "modified_by": "Administrator",
 "module": "Monitoring System",
 "name": "Server Monitoring",
 "naming_rule": "Autoincrement",
 "owner": "Administrator",
 "permissions": [
  {
   "create": 1,
   "delete": 1,
   "email": 1,
   "export": 1,
   "print": 1,
   "read": 1,
   "report": 1,
   "role": "System Manager",
   "share": 1,
   "write": 1
  }
 ],
 "sort_field": "modified",
 "sort_order": "DESC",
 "track_changes": 1
}
```

#### 2.2 Server Monitoring Settings DocType

Create file: `monitoring_system/monitoring_system/doctype/server_monitoring_settings/server_monitoring_settings.json`
```json
{
 "actions": [],
 "creation": "2025-12-23 12:00:00",
 "doctype": "DocType",
 "engine": "InnoDB",
 "field_order": [
  "monitoring_enabled",
  "collection_interval",
  "retention_days",
  "section_break_3",
  "cpu_threshold",
  "memory_threshold",
  "disk_threshold",
  "disk_free_gb_threshold",
  "database_size_threshold_gb",
  "section_break_8",
  "alert_email_addresses",
  "cc_email_addresses",
  "sender_email",
  "section_break_12",
  "smtp_server",
  "smtp_port",
  "section_break_15",
  "enable_log_cleanup",
  "log_retention_days",
  "enable_backup_cleanup",
  "backup_retention_days",
  "enable_temp_cleanup"
 ],
 "fields": [
  {
   "default": "1",
   "fieldname": "monitoring_enabled",
   "fieldtype": "Check",
   "label": "Monitoring Enabled"
  },
  {
   "default": "5",
   "depends_on": "monitoring_enabled",
   "fieldname": "collection_interval",
   "fieldtype": "Int",
   "label": "Collection Interval (Minutes)"
  },
  {
   "default": "30",
   "fieldname": "retention_days",
   "fieldtype": "Int",
   "label": "Metrics Retention (Days)"
  },
  {
   "fieldname": "section_break_3",
   "fieldtype": "Section Break",
   "label": "Threshold Settings"
  },
  {
   "default": "80",
   "fieldname": "cpu_threshold",
   "fieldtype": "Float",
   "label": "CPU Threshold (%)",
   "precision": "2"
  },
  {
   "default": "85",
   "fieldname": "memory_threshold",
   "fieldtype": "Float",
   "label": "Memory Threshold (%)",
   "precision": "2"
  },
  {
   "default": "90",
   "fieldname": "disk_threshold",
   "fieldtype": "Float",
   "label": "Disk Threshold (%)",
   "precision": "2"
  },
  {
   "default": "10",
   "fieldname": "disk_free_gb_threshold",
   "fieldtype": "Float",
   "label": "Disk Free Space Threshold (GB)",
   "precision": "2"
  },
  {
   "default": "50",
   "fieldname": "database_size_threshold_gb",
   "fieldtype": "Float",
   "label": "Database Size Threshold (GB)",
   "precision": "2"
  },
  {
   "fieldname": "section_break_8",
   "fieldtype": "Section Break",
   "label": "Email Configuration"
  },
  {
   "fieldname": "alert_email_addresses",
   "fieldtype": "Small Text",
   "label": "Alert Email Addresses",
   "description": "Comma-separated list of email addresses"
  },
  {
   "fieldname": "cc_email_addresses",
   "fieldtype": "Small Text",
   "label": "CC Email Addresses",
   "description": "Comma-separated list of CC email addresses"
  },
  {
   "fieldname": "sender_email",
   "fieldtype": "Data",
   "label": "Sender Email"
  },
  {
   "fieldname": "section_break_12",
   "fieldtype": "Section Break",
   "label": "SMTP Configuration"
  },
  {
   "fieldname": "smtp_server",
   "fieldtype": "Data",
   "label": "SMTP Server"
  },
  {
   "default": "25",
   "fieldname": "smtp_port",
   "fieldtype": "Int",
   "label": "SMTP Port"
  },
  {
   "fieldname": "section_break_15",
   "fieldtype": "Section Break",
   "label": "Automated Cleanup Settings"
  },
  {
   "default": "1",
   "fieldname": "enable_log_cleanup",
   "fieldtype": "Check",
   "label": "Enable Log Cleanup"
  },
  {
   "default": "30",
   "depends_on": "enable_log_cleanup",
   "fieldname": "log_retention_days",
   "fieldtype": "Int",
   "label": "Log Retention (Days)"
  },
  {
   "default": "1",
   "fieldname": "enable_backup_cleanup",
   "fieldtype": "Check",
   "label": "Enable Backup Cleanup"
  },
  {
   "default": "7",
   "depends_on": "enable_backup_cleanup",
   "fieldname": "backup_retention_days",
   "fieldtype": "Int",
   "label": "Backup Retention (Days)"
  },
  {
   "default": "1",
   "fieldname": "enable_temp_cleanup",
   "fieldtype": "Check",
   "label": "Enable Temporary Files Cleanup"
  }
 ],
 "issingle": 1,
 "modified": "2025-12-23 12:00:00",
 "modified_by": "Administrator",
 "module": "Monitoring System",
 "name": "Server Monitoring Settings",
 "owner": "Administrator",
 "permissions": [
  {
   "create": 1,
   "read": 1,
   "role": "System Manager",
   "write": 1
  }
 ],
 "sort_field": "modified",
 "sort_order": "DESC"
}
```

### Step 3: Create Monitoring Module

Create file: `monitoring_system/monitoring_system/doctype/server_monitoring/server_monitoring.py`
```python
# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import psutil
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime
from datetime import datetime, timedelta

class ServerMonitoring(Document):
    pass

def collect_server_metrics():
    """
    Collect server metrics and store in database.
    This function is called by scheduler every N minutes.
    """
    
    try:
        settings = frappe.get_single('Server Monitoring Settings')
        
        if not settings.monitoring_enabled:
            return
        
        # CPU Metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory Metrics
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024**3), 2)  # GB
        memory_used = round(memory.used / (1024**3), 2)
        memory_percent = round(memory.percent, 2)
        
        # Disk Metrics
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024**3), 2)  # GB
        disk_used = round(disk.used / (1024**3), 2)
        disk_free = round(disk.free / (1024**3), 2)
        disk_percent = round(disk.percent, 2)
        
        # Network Metrics
        network = psutil.net_io_counters()
        bytes_sent = round(network.bytes_sent / (1024**2), 2)  # MB
        bytes_recv = round(network.bytes_recv / (1024**2), 2)
        
        # Database Size
        db_size = get_database_size()
        
        # Create monitoring record
        doc = frappe.get_doc({
            'doctype': 'Server Monitoring',
            'timestamp': now_datetime(),
            'cpu_percent': cpu_percent,
            'cpu_count': cpu_count,
            'memory_total_gb': memory_total,
            'memory_used_gb': memory_used,
            'memory_percent': memory_percent,
            'disk_total_gb': disk_total,
            'disk_used_gb': disk_used,
            'disk_free_gb': disk_free,
            'disk_percent': disk_percent,
            'database_size_mb': db_size,
            'network_sent_mb': bytes_sent,
            'network_recv_mb': bytes_recv
        })
        
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Check thresholds and send alerts if needed
        check_thresholds({
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'disk_free_gb': disk_free,
            'database_size_mb': db_size
        })
        
        # Cleanup old monitoring records
        cleanup_old_monitoring_records()
        
    except Exception as e:
        frappe.log_error(f"Server monitoring collection failed: {str(e)}", "Server Monitoring Error")

def get_database_size():
    """Get current database size in MB"""
    try:
        result = frappe.db.sql("""
            SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
            FROM information_schema.TABLES
            WHERE table_schema = %s
        """, (frappe.conf.db_name,), as_dict=True)
        
        return result[0].size_mb if result else 0
    except:
        return 0

def check_thresholds(metrics):
    """Check if metrics exceed thresholds and trigger alerts"""
    
    try:
        settings = frappe.get_single('Server Monitoring Settings')
        alerts = []
        
        # CPU Alert
        if metrics['cpu_percent'] > settings.cpu_threshold:
            alerts.append({
                'parameter': 'CPU Usage',
                'current_value': f"{metrics['cpu_percent']}%",
                'threshold': f"{settings.cpu_threshold}%",
                'severity': 'High' if metrics['cpu_percent'] > 90 else 'Medium'
            })
        
        # Memory Alert
        if metrics['memory_percent'] > settings.memory_threshold:
            alerts.append({
                'parameter': 'Memory Usage',
                'current_value': f"{metrics['memory_percent']}%",
                'threshold': f"{settings.memory_threshold}%",
                'severity': 'High' if metrics['memory_percent'] > 90 else 'Medium'
            })
        
        # Disk Alert
        if metrics['disk_percent'] > settings.disk_threshold or metrics['disk_free_gb'] < settings.disk_free_gb_threshold:
            alerts.append({
                'parameter': 'Disk Usage',
                'current_value': f"{metrics['disk_percent']}% ({metrics['disk_free_gb']} GB free)",
                'threshold': f"{settings.disk_threshold}% or {settings.disk_free_gb_threshold} GB free",
                'severity': 'Critical' if metrics['disk_free_gb'] < 5 else 'High'
            })
        
        # Database Size Alert
        db_size_gb = metrics['database_size_mb'] / 1024
        if db_size_gb > settings.database_size_threshold_gb:
            alerts.append({
                'parameter': 'Database Size',
                'current_value': f"{db_size_gb:.2f} GB",
                'threshold': f"{settings.database_size_threshold_gb} GB",
                'severity': 'Medium'
            })
        
        if alerts:
            from monitoring_system.utils.alert_system import send_alert_email
            send_alert_email(alerts)
        
    except Exception as e:
        frappe.log_error(f"Threshold checking failed: {str(e)}", "Threshold Check Error")

def cleanup_old_monitoring_records():
    """Delete monitoring records older than retention period"""
    try:
        settings = frappe.get_single('Server Monitoring Settings')
        cutoff_date = get_datetime() - timedelta(days=settings.retention_days)
        
        frappe.db.sql("""
            DELETE FROM `tabServer Monitoring`
            WHERE timestamp < %s
            LIMIT 1000
        """, (cutoff_date,))
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Cleanup of old monitoring records failed: {str(e)}")
```

### Step 4: Create Alert System

Create file: `monitoring_system/monitoring_system/utils/alert_system.py`
```python
# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import smtplib
import frappe
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_alert_email(alerts, alert_type="Server Monitoring"):
    """Send alert email to stakeholders"""
    
    try:
        settings = frappe.get_single('Server Monitoring Settings')
        
        if not settings.alert_email_addresses:
            frappe.log_error("No alert email addresses configured", "Alert System")
            return
        
        # Prepare email
        msg = MIMEMultipart()
        msg['From'] = settings.sender_email or "noreply@company.com"
        msg['To'] = settings.alert_email_addresses
        if settings.cc_email_addresses:
            msg['Cc'] = settings.cc_email_addresses
        
        # Determine maximum severity
        severity_map = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
        max_severity = max([alert.get('severity', 'Low') for alert in alerts],
                          key=lambda x: severity_map.get(x, 0))
        
        msg['Subject'] = f"🚨 {max_severity} ALERT: {alert_type} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Create email body
        email_body = create_alert_email_body(alerts, alert_type)
        msg.attach(MIMEText(email_body, 'html'))
        
        # Send email
        recipients = [email.strip() for email in settings.alert_email_addresses.split(',')]
        if settings.cc_email_addresses:
            recipients.extend([email.strip() for email in settings.cc_email_addresses.split(',')])
        
        with smtplib.SMTP(settings.smtp_server or 'localhost', settings.smtp_port or 25) as server:
            server.sendmail(settings.sender_email, recipients, msg.as_string())
        
        frappe.log_error(f"Alert email sent successfully to {len(recipients)} recipients", "Alert System Success")
        
    except Exception as e:
        frappe.log_error(f"Failed to send alert email: {str(e)}", "Alert System Error")

def create_alert_email_body(alerts, alert_type):
    """Create HTML email body for alerts"""
    
    email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #f44336;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #fff;
            padding: 20px;
            border: 1px solid #ddd;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .critical {{ background-color: #ffebee; }}
        .high {{ background-color: #fff3e0; }}
        .medium {{ background-color: #fff9c4; }}
        .low {{ background-color: #e8f5e9; }}
        .footer {{
            margin-top: 30px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
            font-size: 12px;
            color: #666;
        }}
        .actions {{
            margin-top: 20px;
            padding: 15px;
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }}
        .actions ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🚨 Server Monitoring Alert</h2>
        </div>
        <div class="content">
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Server:</strong> {frappe.local.site}</p>
            <p><strong>Alert Type:</strong> {alert_type}</p>
            
            <h3>Alert Details:</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Current Value</th>
                    <th>Threshold</th>
                    <th>Severity</th>
                </tr>
"""
    
    for alert in alerts:
        severity_class = alert.get('severity', 'Low').lower()
        email_body += f"""
                <tr class="{severity_class}">
                    <td><strong>{alert.get('parameter', 'N/A')}</strong></td>
                    <td>{alert.get('current_value', 'N/A')}</td>
                    <td>{alert.get('threshold', 'N/A')}</td>
                    <td><strong>{alert.get('severity', 'N/A')}</strong></td>
                </tr>
"""
    
    email_body += """
            </table>
            
            <div class="actions">
                <h3>🔧 Recommended Actions:</h3>
                <ul>
                    <li>Check server logs for any errors or warnings</li>
                    <li>Review running processes and resource usage</li>
                    <li>Clean up unnecessary files if disk space is low</li>
                    <li>Investigate any unusual database growth</li>
                    <li>Contact IT team if issue persists or escalates</li>
                    <li>Review application logs for potential memory leaks</li>
                </ul>
            </div>
        </div>
        <div class="footer">
            <p>This is an automated alert from the Server Monitoring System.</p>
            <p>Please do not reply to this email. For support, contact your IT team.</p>
        </div>
    </div>
</body>
</html>
"""
    
    return email_body

def send_recovery_email():
    """Send email when system recovers from alert state"""
    
    try:
        settings = frappe.get_single('Server Monitoring Settings')
        
        if not settings.alert_email_addresses:
            return
        
        msg = MIMEMultipart()
        msg['From'] = settings.sender_email
        msg['To'] = settings.alert_email_addresses
        msg['Subject'] = f"✅ RECOVERY: Server Monitoring - All Systems Normal"
        
        email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4caf50;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #fff;
            padding: 20px;
            border: 1px solid #ddd;
        }}
        .footer {{
            margin-top: 30px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>✅ System Recovery Notification</h2>
        </div>
        <div class="content">
            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Server:</strong> {frappe.local.site}</p>
            
            <p>All monitored parameters have returned to normal levels.</p>
            <p>The system is operating within acceptable thresholds.</p>
        </div>
        <div class="footer">
            <p>This is an automated notification from the Server Monitoring System.</p>
        </div>
    </div>
</body>
</html>
"""
        
        msg.attach(MIMEText(email_body, 'html'))
        
        recipients = [email.strip() for email in settings.alert_email_addresses.split(',')]
        
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.sendmail(settings.sender_email, recipients, msg.as_string())
        
    except Exception as e:
        frappe.log_error(f"Failed to send recovery email: {str(e)}", "Recovery Email Error")
```

### Step 5: Create Cleanup Tasks

Create file: `monitoring_system/monitoring_system/tasks/disk_cleanup.py`
```python
# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import os
import glob
import frappe
from datetime import datetime, timedelta
from frappe.utils import get_bench_path, get_site_path

def cleanup_old_files():
    """Main cleanup function - coordinates all cleanup tasks"""
    
    try:
        settings = frappe.get_single('Server Monitoring Settings')
        
        bench_path = get_bench_path()
        site_path = get_site_path()
        
        results = {}
        
        # Cleanup logs
        if settings.enable_log_cleanup:
            results['logs'] = cleanup_old_logs(bench_path, site_path, settings.log_retention_days)
        
        # Cleanup backups
        if settings.enable_backup_cleanup:
            results['backups'] = cleanup_old_backups(site_path, settings.backup_retention_days)
        
        # Cleanup temp files
        if settings.enable_temp_cleanup:
            results['temp_files'] = cleanup_temp_files(bench_path, site_path)
        
        # Cleanup error snapshots
        results['snapshots'] = cleanup_error_snapshots(site_path, 30)
        
        # Log results
        frappe.log_error(f"Cleanup completed successfully: {results}", "Disk Cleanup Success")
        
        return results
        
    except Exception as e:
        frappe.log_error(f"Disk cleanup failed: {str(e)}", "Disk Cleanup Error")
        return {}

def cleanup_old_logs(bench_path, site_path, days=30):
    """Remove log files older than specified days"""
    
    deleted_count = 0
    deleted_size = 0
    
    log_patterns = [
        f"{bench_path}/logs/*.log*",
        f"{site_path}/logs/*.log*",
        f"{site_path}/private/logs/*.log*"
    ]
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for pattern in log_patterns:
        for log_file in glob.glob(pattern):
            try:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                if file_mtime < cutoff_date:
                    file_size = os.path.getsize(log_file)
                    os.remove(log_file)
                    deleted_count += 1
                    deleted_size += file_size
            except Exception as e:
                frappe.log_error(f"Error deleting log file {log_file}: {str(e)}")
    
    return {
        'deleted_count': deleted_count,
        'deleted_size_mb': round(deleted_size / (1024 * 1024), 2)
    }

def cleanup_old_backups(site_path, days=7):
    """Remove backup files older than specified days"""
    
    deleted_count = 0
    deleted_size = 0
    
    backup_path = f"{site_path}/private/backups"
    cutoff_date = datetime.now() - timedelta(days=days)
    
    if os.path.exists(backup_path):
        for backup_file in glob.glob(f"{backup_path}/*"):
            try:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(backup_file))
                if file_mtime < cutoff_date:
                    file_size = os.path.getsize(backup_file)
                    os.remove(backup_file)
                    deleted_count += 1
                    deleted_size += file_size
            except Exception as e:
                frappe.log_error(f"Error deleting backup {backup_file}: {str(e)}")
    
    return {
        'deleted_count': deleted_count,
        'deleted_size_mb': round(deleted_size / (1024 * 1024), 2)
    }

def cleanup_temp_files(bench_path, site_path):
    """Remove temporary files"""
    
    deleted_count = 0
    deleted_size = 0
    
    temp_patterns = [
        f"{site_path}/private/temp/*",
        f"{site_path}/public/files/.tmb/*",
        "/tmp/frappe-*"
    ]
    
    for pattern in temp_patterns:
        for temp_file in glob.glob(pattern):
            try:
                if os.path.isfile(temp_file):
                    file_size = os.path.getsize(temp_file)
                    os.remove(temp_file)
                    deleted_count += 1
                    deleted_size += file_size
            except Exception as e:
                frappe.log_error(f"Error deleting temp file {temp_file}: {str(e)}")
    
    return {
        'deleted_count': deleted_count,
        'deleted_size_mb': round(deleted_size / (1024 * 1024), 2)
    }

def cleanup_error_snapshots(site_path, days=30):
    """Remove old error snapshots"""
    
    deleted_count = 0
    deleted_size = 0
    
    snapshot_path = f"{site_path}/private/error-snapshots"
    cutoff_date = datetime.now() - timedelta(days=days)
    
    if os.path.exists(snapshot_path):
        for snapshot in glob.glob(f"{snapshot_path}/*"):
            try:
                file_mtime = datetime.fromtimestamp(os.path.getmtime(snapshot))
                if file_mtime < cutoff_date:
                    file_size = os.path.getsize(snapshot)
                    os.remove(snapshot)
                    deleted_count += 1
                    deleted_size += file_size
            except Exception as e:
                frappe.log_error(f"Error deleting snapshot {snapshot}: {str(e)}")
    
    return {
        'deleted_count': deleted_count,
        'deleted_size_mb': round(deleted_size / (1024 * 1024), 2)
    }

def get_disk_usage_report():
    """Generate disk usage report for top directories"""
    
    try:
        site_path = get_site_path()
        
        directories = [
            f"{site_path}/private/backups",
            f"{site_path}/private/files",
            f"{site_path}/public/files",
            f"{site_path}/logs",
            f"{site_path}/private/logs"
        ]
        
        report = []
        
        for directory in directories:
            if os.path.exists(directory):
                total_size = 0
                file_count = 0
                
                for dirpath, dirnames, filenames in os.walk(directory):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            total_size += os.path.getsize(filepath)
                            file_count += 1
                        except:
                            pass
                
                report.append({
                    'directory': directory,
                    'size_mb': round(total_size / (1024 * 1024), 2),
                    'file_count': file_count
                })
        
        return report
        
    except Exception as e:
        frappe.log_error(f"Error generating disk usage report: {str(e)}")
        return []
```

### Step 6: Create Database Maintenance Tasks

Create file: `monitoring_system/monitoring_system/tasks/database_maintenance.py`
```python
# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta

def optimize_database():
    """Optimize database tables weekly"""
    
    try:
        tables = frappe.db.sql("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s 
            AND table_type = 'BASE TABLE'
        """, (frappe.conf.db_name,), as_dict=True)
        
        optimized_count = 0
        failed_count = 0
        
        for table in tables:
            try:
                frappe.db.sql(f"OPTIMIZE TABLE `{table.table_name}`")
                optimized_count += 1
            except Exception as e:
                failed_count += 1
                frappe.log_error(f"Error optimizing table {table.table_name}: {str(e)}")
        
        frappe.db.commit()
        
        result = f"Database optimization completed: {optimized_count} tables optimized, {failed_count} failed"
        frappe.log_error(result, "Database Maintenance Success")
        
        return {
            'optimized_count': optimized_count,
            'failed_count': failed_count
        }
        
    except Exception as e:
        frappe.log_error(f"Database optimization failed: {str(e)}", "Database Maintenance Error")
        return {}

def analyze_database_tables():
    """Analyze database tables for query optimization"""
    
    try:
        tables = frappe.db.sql("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s 
            AND table_type = 'BASE TABLE'
        """, (frappe.conf.db_name,), as_dict=True)
        
        analyzed_count = 0
        
        for table in tables:
            try:
                frappe.db.sql(f"ANALYZE TABLE `{table.table_name}`")
                analyzed_count += 1
            except Exception as e:
                frappe.log_error(f"Error analyzing table {table.table_name}: {str(e)}")
        
        frappe.db.commit()
        
        result = f"Database analysis completed: {analyzed_count} tables analyzed"
        frappe.log_error(result, "Database Analysis Success")
        
        return {'analyzed_count': analyzed_count}
        
    except Exception as e:
        frappe.log_error(f"Database analysis failed: {str(e)}", "Database Analysis Error")
        return {}

def cleanup_old_error_logs():
    """Clean up old error logs from database"""
    
    try:
        cutoff_date = datetime.now() - timedelta(days=90)
        
        frappe.db.sql("""
            DELETE FROM `tabError Log`
            WHERE creation < %s
            LIMIT 1000
        """, (cutoff_date,))
        
        frappe.db.commit()
        
        frappe.log_error("Old error logs cleaned up successfully", "Error Log Cleanup")
        
    except Exception as e:
        frappe.log_error(f"Error log cleanup failed: {str(e)}", "Error Log Cleanup Error")

def get_database_statistics():
    """Get comprehensive database statistics"""
    
    try:
        # Table sizes
        table_stats = frappe.db.sql("""
            SELECT 
                table_name,
                ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb,
                table_rows
            FROM information_schema.TABLES
            WHERE table_schema = %s
            AND table_type = 'BASE TABLE'
            ORDER BY (data_length + index_length) DESC
            LIMIT 20
        """, (frappe.conf.db_name,), as_dict=True)
        
        # Total database size
        total_size = frappe.db.sql("""
            SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as total_mb
            FROM information_schema.TABLES
            WHERE table_schema = %s
        """, (frappe.conf.db_name,), as_dict=True)
        
        return {
            'table_stats': table_stats,
            'total_size_mb': total_size[0].total_mb if total_size else 0
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting database statistics: {str(e)}")
        return {}
```

### Step 7: Configure Scheduler

Edit file: `monitoring_system/hooks.py`
```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "monitoring_system"
app_title = "Monitoring System"
app_publisher = "Your Company"
app_description = "Server Monitoring and Alerting System"
app_icon = "octicon octicon-pulse"
app_color = "blue"
app_email = "support@company.com"
app_license = "MIT"

# Scheduled Tasks
# ---------------

scheduler_events = {
    # Server monitoring every 5 minutes
    "cron": {
        "*/5 * * * *": [
            "monitoring_system.monitoring_system.doctype.server_monitoring.server_monitoring.collect_server_metrics"
        ]
    },
    
    # Daily tasks at 2 AM
    "daily": [
        "monitoring_system.monitoring_system.tasks.disk_cleanup.cleanup_old_files",
        "monitoring_system.monitoring_system.tasks.database_maintenance.cleanup_old_error_logs"
    ],
    
    # Weekly tasks on Sunday at 3 AM
    "weekly": [
        "monitoring_system.monitoring_system.tasks.database_maintenance.optimize_database",
        "monitoring_system.monitoring_system.tasks.database_maintenance.analyze_database_tables"
    ]
}

# Document Events
# ---------------

# doc_events = {
#     "*": {
#         "on_update": "method",
#         "on_cancel": "method",
#         "on_trash": "method"
#     }
# }
```

### Step 8: Install Prometheus & Grafana (Optional)

#### Install Node Exporter
```bash
# Download Node Exporter
cd /tmp
wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
tar xvfz node_exporter-1.7.0.linux-amd64.tar.gz

# Install
sudo cp node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter

# Create systemd service
sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOF
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter

# Verify
curl http://localhost:9100/metrics
```

#### Install MySQL Exporter
```bash
# Download MySQL Exporter
cd /tmp
wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.15.1/mysqld_exporter-0.15.1.linux-amd64.tar.gz
tar xvfz mysqld_exporter-0.15.1.linux-amd64.tar.gz

# Install
sudo cp mysqld_exporter-0.15.1.linux-amd64/mysqld_exporter /usr/local/bin/
sudo useradd -rs /bin/false mysqld_exporter

# Create MySQL user for exporter
mysql -u root -p <<EOF
CREATE USER 'exporter'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'localhost';
FLUSH PRIVILEGES;
EOF

# Create config file
sudo mkdir /etc/mysqld_exporter
sudo tee /etc/mysqld_exporter/.my.cnf > /dev/null <<EOF
[client]
user=exporter
password=StrongPassword123!
EOF

sudo chown mysqld_exporter:mysqld_exporter /etc/mysqld_exporter/.my.cnf
sudo chmod 600 /etc/mysqld_exporter/.my.cnf

# Create systemd service
sudo tee /etc/systemd/system/mysqld_exporter.service > /dev/null <<EOF
[Unit]
Description=MySQL Exporter
After=network.target

[Service]
User=mysqld_exporter
Group=mysqld_exporter
Type=simple
ExecStart=/usr/local/bin/mysqld_exporter \
  --config.my-cnf=/etc/mysqld_exporter/.my.cnf \
  --collect.global_status \
  --collect.info_schema.innodb_metrics \
  --collect.auto_increment.columns \
  --collect.info_schema.processlist \
  --collect.binlog_size \
  --collect.info_schema.tablestats \
  --collect.global_variables \
  --collect.info_schema.query_response_time \
  --collect.info_schema.userstats \
  --collect.perf_schema.tableiowaits \
  --collect.perf_schema.indexiowaits \
  --collect.perf_schema.tablelocks

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl start mysqld_exporter
sudo systemctl enable mysqld_exporter

# Verify
curl http://localhost:9104/metrics
```

#### Install Prometheus
```bash
# Download Prometheus
cd /tmp
wget https://github.com/prometheus/prometheus/releases/download/v2.48.0/prometheus-2.48.0.linux-amd64.tar.gz
tar xvfz prometheus-2.48.0.linux-amd64.tar.gz

# Install
sudo cp -r prometheus-2.48.0.linux-amd64 /usr/local/prometheus
sudo useradd -rs /bin/false prometheus

# Create config
sudo tee /usr/local/prometheus/prometheus.yml > /dev/null <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']
  
  - job_name: 'mysql'
    static_configs:
      - targets: ['localhost:9104']
EOF

# Create systemd service
sudo tee /etc/systemd/system/prometheus.service > /dev/null <<EOF
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/prometheus/prometheus \
  --config.file=/usr/local/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/ \
  --web.console.templates=/usr/local/prometheus/consoles \
  --web.console.libraries=/usr/local/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
EOF

# Create data directory
sudo mkdir -p /var/lib/prometheus
sudo chown prometheus:prometheus /var/lib/prometheus

# Start service
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus

# Access at http://your-server-ip:9090
```

#### Install Grafana
```bash
# Add Grafana repository
sudo apt-get install -y software-properties-common
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"

# Install Grafana
sudo apt-get update
sudo apt-get install -y grafana

# Start Grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

# Access at http://your-server-ip:3000
# Default login: admin/admin
```

#### Configure Grafana

1. **Add Prometheus Data Source:**
   - Login to Grafana (http://your-server-ip:3000)
   - Go to: Configuration → Data Sources → Add data source
   - Select: Prometheus
   - URL: `http://localhost:9090`
   - Click: Save & Test

2. **Import Dashboards:**
   
   **Node Exporter Dashboard:**
   - Go to: Create → Import
   - Dashboard ID: `1860`
   - Select Prometheus data source
   - Click: Import

   **MySQL Dashboard:**
   - Go to: Create → Import
   - Dashboard ID: `7362`
   - Select Prometheus data source
   - Click: Import

---

## Configuration

### Initial Setup

1. **Access Settings:**
```
   Navigate to: Desk → Monitoring System → Server Monitoring Settings
```

2. **Enable Monitoring:**
   - Check: "Monitoring Enabled"
   - Set collection interval: `5` minutes (recommended)
   - Set retention days: `30` days

3. **Configure Thresholds:**
   - CPU Threshold: `80%`
   - Memory Threshold: `85%`
   - Disk Threshold: `90%`
   - Disk Free Space: `10 GB`
   - Database Size: `50 GB`

4. **Email Configuration:**
   - Alert Email Addresses: `devops@company.com, admin@company.com`
   - CC Emails: `manager@company.com`
   - Sender Email: `monitoring@company.com`
   - SMTP Server: `smtp.company.com` or `localhost`
   - SMTP Port: `25` or `587`

5. **Cleanup Settings:**
   - Enable Log Cleanup: ✓
   - Log Retention: `30` days
   - Enable Backup Cleanup: ✓
   - Backup Retention: `7` days
   - Enable Temp Cleanup: ✓

6. **Save Settings**

### Testing the System
```bash
# Test monitoring collection manually
cd ~/frappe-bench
bench --site your-site execute monitoring_system.monitoring_system.doctype.server_monitoring.server_monitoring.collect_server_metrics

# Test cleanup tasks
bench --site your-site execute monitoring_system.monitoring_system.tasks.disk_cleanup.cleanup_old_files

# Check logs
tail -f ~/frappe-bench/sites/your-site/logs/schedule.log
```

---

## Monitoring Components

### 1. CPU Monitoring

**Metrics Collected:**
- CPU Usage Percentage
- CPU Core Count

**Thresholds:**
- Medium Alert: 80-90%
- High Alert: 90%+

**Common Causes of High CPU:**
- Heavy database queries
- Background jobs running
- Infinite loops in code
- External API calls timing out
- Too many concurrent users

### 2. Memory Monitoring

**Metrics Collected:**
- Total Memory (GB)
- Used Memory (GB)
- Memory Usage Percentage

**Thresholds:**
- Medium Alert: 85-90%
- High Alert: 90%+

**Common Causes of High Memory:**
- Memory leaks in application code
- Large result sets loaded into memory
- Too many cached objects
- Insufficient memory for workload

### 3. Disk Monitoring

**Metrics Collected:**
- Total Disk Space (GB)
- Used Disk Space (GB)
- Free Disk Space (GB)
- Disk Usage Percentage

**Thresholds:**
- High Alert: 90%+ usage
- Critical Alert: <5 GB free

**Common Causes of Low Disk Space:**
- Log files accumulation
- Database growth
- Backup files not cleaned
- Uploaded files accumulation
- Temp files not removed

### 4. Database Monitoring

**Metrics Collected:**
- Database Size (MB)
- Table Sizes
- Row Counts

**Thresholds:**
- Medium Alert: Exceeds configured threshold

**Common Causes of Database Growth:**
- Lack of data retention policy
- Missing archival process
- Large transaction logs
- Inefficient indexes

### 5. Network Monitoring

**Metrics Collected:**
- Bytes Sent (MB)
- Bytes Received (MB)

**Purpose:**
- Track network usage patterns
- Identify unusual traffic spikes
- Monitor bandwidth consumption

---

## Alert System

### Alert Severity Levels

| Severity | Description | Response Time | Example |
|----------|-------------|---------------|---------|
| **Low** | Minor issues, no immediate action needed | 24 hours | Database size approaching threshold |
| **Medium** | Moderate issues, needs attention | 4 hours | CPU usage 80-90% |
| **High** | Serious issues, needs prompt action | 1 hour | Memory usage >90% |
| **Critical** | System failure imminent | Immediate | Disk space <5GB |

### Alert Email Format
```
Subject: 🚨 [SEVERITY] ALERT: Server Monitoring - [DATE TIME]

Body:
- Timestamp
- Server name
- Alert details table
- Recommended actions
- Contact information
```

### Alert Flow
```
Metric Collection → Threshold Check → Alert Triggered
                                    ↓
                          Send Email to Recipients
                                    ↓
                          Log Alert to Database
                                    ↓
                          Monitor for Recovery
                                    ↓
                          Send Recovery Email (if recovered)
```

### Customizing Alerts

You can customize alert behavior by modifying:
```python
# monitoring_system/monitoring_system/doctype/server_monitoring/server_monitoring.py

def check_thresholds(metrics):
    """Modify this function to customize alert logic"""
    
    # Example: Add custom alert for specific condition
    if metrics['disk_free_gb'] < 2:
        # Trigger emergency shutdown procedures
        emergency_disk_cleanup()
        send_critical_alert()
```

---

## Maintenance Tasks

### Daily Tasks (2:00 AM)

1. **Log Cleanup**
   - Removes logs older than configured retention period
   - Patterns: `*.log`, `*.log.*`
   - Locations: bench/logs, site/logs, site/private/logs

2. **Temporary Files Cleanup**
   - Removes temporary files
   - Locations: site/private/temp, /tmp/frappe-*

3. **Error Log Cleanup**
   - Removes database error logs older than 90 days

### Weekly Tasks (Sunday 3:00 AM)

1. **Database Optimization**
   - Runs `OPTIMIZE TABLE` on all tables
   - Reclaims unused space
   - Rebuilds indexes

2. **Database Analysis**
   - Runs `ANALYZE TABLE` on all tables
   - Updates table statistics
   - Improves query performance

3. **Backup Cleanup**
   - Removes backups older than configured retention period
   - Keeps latest backups only

### Manual Maintenance Commands
```bash
# Force cleanup now
bench --site your-site execute monitoring_system.monitoring_system.tasks.disk_cleanup.cleanup_old_files

# Force database optimization
bench --site your-site execute monitoring_system.monitoring_system.tasks.database_maintenance.optimize_database

# Get disk usage report
bench --site your-site execute monitoring_system.monitoring_system.tasks.disk_cleanup.get_disk_usage_report

# Get database statistics
bench --site your-site execute monitoring_system.monitoring_system.tasks.database_maintenance.get_database_statistics
```

---

## Troubleshooting

### Issue: Metrics Not Being Collected

**Symptoms:**
- No new records in Server Monitoring
- Email alerts not received

**Solutions:**
1. Check if monitoring is enabled:
```bash
   bench --site your-site console
   >>> frappe.get_single('Server Monitoring Settings').monitoring_enabled
```

2. Check scheduler status:
```bash
   bench --site your-site doctor
```

3. Check scheduler logs:
```bash
   tail -f ~/frappe-bench/sites/your-site/logs/schedule.log
```

4. Manually run collection:
```bash
   bench --site your-site execute monitoring_system.monitoring_system.doctype.server_monitoring.server_monitoring.collect_server_metrics
```

### Issue: Email Alerts Not Sending

**Symptoms:**
- Metrics collected but no emails received

**Solutions:**
1. Verify email configuration:
```bash
   bench --site your-site console
   >>> settings = frappe.get_single('Server Monitoring Settings')
   >>> print(settings.alert_email_addresses)
   >>> print(settings.smtp_server)
```

2. Test SMTP connection:
```bash
   telnet smtp-server 25
```

3. Check error logs:
```bash
   tail -f ~/frappe-bench/sites/your-site/logs/frappe.log | grep -i "alert"
```

4. Manually trigger alert:
```bash
   bench --site your-site execute monitoring_system.monitoring_system.utils.alert_system.send_alert_email --args '[{"parameter":"Test","current_value":"100%","threshold":"80%","severity":"High"}]'
```

### Issue: High False Positive Alerts

**Symptoms:**
- Too many alerts for normal operations

**Solutions:**
1. Adjust thresholds in Settings
2. Increase collection interval
3. Add alert cooldown period (code modification required)

### Issue: Cleanup Not Working

**Symptoms:**
- Old files not being deleted
- Disk space still high

**Solutions:**
1. Check cleanup settings are enabled
2. Verify file permissions
3. Manually run cleanup:
```bash
   bench --site your-site execute monitoring_system.monitoring_system.tasks.disk_cleanup.cleanup_old_files
```

4. Check specific directories:
```bash
   du -sh ~/frappe-bench/sites/your-site/private/backups/*
   du -sh ~/frappe-bench/sites/your-site/logs/*
```

### Issue: Prometheus Not Collecting Metrics

**Symptoms:**
- Grafana shows "No Data"

**Solutions:**
1. Check exporters are running:
```bash
   sudo systemctl status node_exporter
   sudo systemctl status mysqld_exporter
   sudo systemctl status prometheus
```

2. Test exporter endpoints:
```bash
   curl http://localhost:9100/metrics
   curl http://localhost:9104/metrics
```

3. Check Prometheus targets:
   - Open: http://your-server-ip:9090/targets
   - All targets should show "UP" status

4. Check Prometheus logs:
```bash
   sudo journalctl -u prometheus -f
```

### Issue: Database Connection Errors

**Symptoms:**
- "Lost connection to MySQL server" errors

**Solutions:**
1. Increase MySQL timeouts:
```bash
   sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
   
   # Add:
   wait_timeout = 28800
   interactive_timeout = 28800
```

2. Restart MySQL:
```bash
   sudo systemctl restart mysql
```

3. Check connection pooling in Frappe

---

## Best Practices

### 1. Threshold Configuration

- **Start Conservative:** Begin with higher thresholds and gradually lower them
- **Know Your Baseline:** Monitor for 1 week to understand normal patterns
- **Business Hours vs Off-Hours:** Consider different thresholds for different times
- **Seasonal Variations:** Adjust for known busy periods

### 2. Alert Fatigue Prevention

- **Meaningful Alerts Only:** Don't alert on every minor issue
- **Alert Consolidation:** Group related alerts
- **Recovery Notifications:** Send "all clear" emails
- **Alert Cooldown:** Don't send same alert repeatedly

### 3. Disk Space Management

- **Proactive Cleanup:** Don't wait for alerts
- **Regular Reviews:** Monthly check of large directories
- **Data Archival:** Move old data to archive storage
- **Backup Strategy:** Keep only necessary backups

### 4. Database Optimization

- **Regular Maintenance:** Weekly optimization minimum
- **Index Management:** Review and optimize indexes quarterly
- **Query Analysis:** Identify and optimize slow queries
- **Data Retention:** Implement retention policies for all tables

### 5. Monitoring Best Practices

- **Documentation:** Document all threshold changes
- **Runbooks:** Create response procedures for each alert type
- **Regular Testing:** Test alert system monthly
- **Review Metrics:** Weekly review of trends
- **Capacity Planning:** Use metrics for future planning

### 6. Security Considerations

- **Email Security:** Use TLS for SMTP
- **Access Control:** Restrict monitoring dashboard access
- **Sensitive Data:** Don't log passwords or sensitive data
- **Alert Content:** Be careful about PII in alerts

### 7. Team Coordination

- **On-Call Rotation:** Establish clear responsibility
- **Escalation Path:** Define when to escalate
- **Communication:** Keep team informed of changes
- **Post-Mortems:** Review incidents and improve

---

## Appendix

### A. Useful Commands
```bash
# System monitoring
htop                    # Interactive process viewer
iotop                   # Disk I/O monitoring
nethogs                 # Network bandwidth per process
df -h                   # Disk usage
free -h                 # Memory usage
uptime                  # System uptime and load

# Frappe specific
bench --site site1 doctor                          # System health check
bench --site site1 migrate                         # Run migrations
bench --site site1 clear-cache                     # Clear cache
bench --site site1 console                         # Python console
bench restart                                      # Restart all services
bench --site site1 backup                          # Create backup
bench --site site1 restore /path/to/backup.sql    # Restore backup

# Service management
sudo systemctl status frappe-bench-frappe          # Check Frappe service
sudo systemctl restart frappe-bench-frappe         # Restart Frappe
sudo systemctl status mysql                        # Check MySQL
sudo systemctl restart mysql                       # Restart MySQL
sudo systemctl status nginx                        # Check Nginx
sudo systemctl restart nginx                       # Restart Nginx

# Log viewing
tail -f ~/frappe-bench/sites/site1/logs/web.log       # Web logs
tail -f ~/frappe-bench/sites/site1/logs/worker.log    # Worker logs
tail -f ~/frappe-bench/sites/site1/logs/schedule.log  # Scheduler logs
tail -f /var/log/nginx/error.log                      # Nginx errors
tail -f /var/log/mysql/error.log                      # MySQL errors

# Database operations
mysql -u root -p                                   # MySQL shell
mysql -u root -p dbname < backup.sql              # Restore database
mysqldump -u root -p dbname > backup.sql          # Backup database
mysqlcheck -u root -p --optimize --all-databases  # Optimize all databases

# Disk cleanup
du -sh ~/frappe-bench/sites/*/private/backups/*   # Check backup sizes
du -sh ~/frappe-bench/sites/*/logs/*              # Check log sizes
find ~/frappe-bench -name "*.log" -mtime +30      # Find old logs
find /tmp -name "frappe-*" -type f -delete        # Clean temp files
```

### B. Configuration Files Reference

**Location of Key Files:**
```
~/frappe-bench/
├── sites/
│   └── your-site/
│       ├── site_config.json                    # Site configuration
│       ├── private/
│       │   ├── backups/                        # Database backups
│       │   ├── files/                          # Private uploads
│       │   └── logs/                           # Custom logs
│       ├── public/
│       │   └── files/                          # Public uploads
│       └── logs/
│           ├── web.log                         # Web requests
│           ├── worker.log                      # Background jobs
│           └── schedule.log                    # Scheduled tasks
├── apps/
│   └── monitoring_system/                      # Your app
└── config/
    └── supervisor.conf                         # Supervisor config
```

### C. Database Schema

**Server Monitoring Table:**
```sql
CREATE TABLE `tabServer Monitoring` (
  `name` varchar(140) NOT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `timestamp` datetime(6) DEFAULT NULL,
  `cpu_percent` decimal(18,2) DEFAULT NULL,
  `cpu_count` int(11) DEFAULT NULL,
  `memory_total_gb` decimal(18,2) DEFAULT NULL,
  `memory_used_gb` decimal(18,2) DEFAULT NULL,
  `memory_percent` decimal(18,2) DEFAULT NULL,
  `disk_total_gb` decimal(18,2) DEFAULT NULL,
  `disk_used_gb` decimal(18,2) DEFAULT NULL,
  `disk_free_gb` decimal(18,2) DEFAULT NULL,
  `disk_percent` decimal(18,2) DEFAULT NULL,
  `database_size_mb` decimal(18,2) DEFAULT NULL,
  `network_sent_mb` decimal(18,2) DEFAULT NULL,
  `network_recv_mb` decimal(18,2) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `timestamp` (`timestamp`)
);
```

### D. Grafana Dashboard JSON

Save this as a JSON file and import into Grafana for custom Frappe monitoring:
```json
{
  "dashboard": {
    "title": "Frappe Server Monitoring",
    "tags": ["frappe", "monitoring"],
    "timezone": "browser",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100"
          }
        ]
      },
      {
        "title": "Disk Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "(node_filesystem_size_bytes{fstype!=\"tmpfs\"} - node_filesystem_avail_bytes{fstype!=\"tmpfs\"}) / node_filesystem_size_bytes{fstype!=\"tmpfs\"} * 100"
          }
        ]
      },
      {
        "title": "MySQL Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "mysql_global_status_threads_connected"
          }
        ]
      }
    ]
  }
}
```

### E. Cron Job Syntax Reference
```bash
# Format: minute hour day month weekday command
# * = any value
# */n = every n units
# n-m = range from n to m
# n,m = list of values

# Examples:
0 2 * * *          # Daily at 2:00 AM
0 3 * * 0          # Weekly on Sunday at 3:00 AM
*/5 * * * *        # Every 5 minutes
0 0 1 * *          # Monthly on 1st at midnight
0 9-17 * * 1-5     # Every hour from 9 AM to 5 PM, Monday to Friday
```

### F. Support and Resources

**Documentation:**
- Frappe Framework: https://frappeframework.com/docs
- Prometheus: https://prometheus.io/docs
- Grafana: https://grafana.com/docs

**Community:**
- Frappe Forum: https://discuss.frappe.io
- GitHub Issues: Report bugs and request features

**Professional Support:**
- Email: support@company.com
- Phone: +91-XXX-XXXX-XXXX
- Hours: Monday-Friday, 9 AM - 6 PM IST

---

## Changelog

### Version 1.0.0 (2025-12-23)
- Initial release
- Server monitoring with CPU, memory, disk metrics
- Database size monitoring
- Email alert system
- Automated cleanup tasks
- Grafana dashboard integration
- Documentation

### Version 1.1.0 (Planned)
- Alert cooldown periods
- SMS notifications
- Slack integration
- Custom metric collection
- Advanced analytics
- Mobile app

---

## License

MIT License

Copyright (c) 2025 Your Company

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**Document Version:** 1.0  
**Last Updated:** December 23, 2025  
**Prepared By:** Sant Agarwal, Software Developer  
**Organization:** Batlivala & Karani Securities India Pvt. Ltd.

---

*End of Documentation*
