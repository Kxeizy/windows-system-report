import platform
import psutil
import os
import winreg
import socket
from datetime import datetime

SEPARATOR = "=" * 60

def save_report(content):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(desktop, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ Report saved to: {path}")

def get_system_info():
    lines = []
    lines.append(SEPARATOR)
    lines.append(f"  WINDOWS SYSTEM REPORT — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(SEPARATOR)

    # System info
    lines.append("\n[💻 SYSTEM]")
    lines.append(f"  OS:       {platform.system()} {platform.release()} ({platform.version()})")
    lines.append(f"  CPU:      {platform.processor()}")
    lines.append(f"  RAM:      {round(psutil.virtual_memory().total / (1024**3), 2)} GB total")
    lines.append(f"  RAM used: {round(psutil.virtual_memory().used / (1024**3), 2)} GB ({psutil.virtual_memory().percent}%)")
    lines.append(f"  Hostname: {socket.gethostname()}")

    # Disk usage
    lines.append("\n[💾 DISK]")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            lines.append(f"  {part.device} — Total: {round(usage.total/(1024**3),1)} GB | "
                         f"Free: {round(usage.free/(1024**3),1)} GB | "
                         f"Used: {usage.percent}%")
        except:
            pass

    # Temp files
    lines.append("\n[🗑️ TEMP FILES]")
    temp_path = os.environ.get("TEMP", "")
    try:
        temp_size = sum(
            os.path.getsize(os.path.join(temp_path, f))
            for f in os.listdir(temp_path)
            if os.path.isfile(os.path.join(temp_path, f))
        )
        lines.append(f"  TEMP folder: {round(temp_size / (1024**2), 2)} MB used")
    except:
        lines.append("  Unable to read TEMP folder")

    # Startup programs
    lines.append("\n[🚀 STARTUP PROGRAMS]")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run")
        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                lines.append(f"  {name}: {value}")
                i += 1
            except OSError:
                break
    except:
        lines.append("  Unable to read registry")

    # Top processes by memory
    lines.append("\n[📊 TOP 10 PROCESSES BY MEMORY]")
    procs = sorted(psutil.process_iter(['name', 'memory_info']),
                   key=lambda p: p.info['memory_info'].rss, reverse=True)[:10]
    for p in procs:
        lines.append(f"  {p.info['name']:<35} {round(p.info['memory_info'].rss / (1024**2), 1)} MB")

   # Active network connections
    lines.append("\n[🌐 ACTIVE NETWORK CONNECTIONS]")
    try:
        connections = psutil.net_connections(kind='inet')
        active = [c for c in connections if c.status == 'ESTABLISHED'][:10]
        if active:
            for c in active:
                laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
                raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "N/A"
                lines.append(f"  {laddr} → {raddr}")
        else:
            lines.append("  No active connections found")
    except Exception as e:
        lines.append(f"  Unable to read network connections: {e}")

    lines.append("\n" + SEPARATOR)
    lines.append("  Report complete!")
    lines.append(SEPARATOR)

    return "\n".join(lines)

if __name__ == "__main__":
    report = get_system_info()
    print(report)
    save_report(report)