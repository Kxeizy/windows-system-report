# 🖥️ Windows System Report

A Python tool that generates a detailed diagnostic report of a Windows system.

## 📋 Features
- System info (OS, CPU, RAM)
- Disk usage for all drives
- Temp files size
- Startup programs
- Top 10 processes by memory usage
- Active network connections
- Auto-saves report as .txt on the Desktop

## ▶️ Usage
```bash
pip install psutil
python system_report.py
```

## 🛠️ Built With
- Python
- psutil
- winreg (built-in)
