"""Информация о системе ПК"""
import platform
import socket
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def get_system_info():
    """Получает полную информацию о системе"""
    info_data = {}
    
    # Основная информация об ОС
    info_data["os"] = {
        "name": platform.system(),
        "version": platform.version(),
        "architecture": platform.architecture()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
        "platform": platform.platform()
    }
    
    # Информация о Python
    info_data["python"] = {
        "version": sys.version,
        "version_info": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "executable": sys.executable,
        "path": sys.path[0] if sys.path else "Unknown"
    }
    
    # Информация о сети
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        info_data["network"] = {
            "hostname": hostname,
            "local_ip": local_ip,
            "fqdn": socket.getfqdn()
        }
    except:
        info_data["network"] = {"error": "Не удалось получить информацию о сети"}
    
    # Информация о дисках
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        info_data["disks"] = {
            "total": f"{total // (1024**3)} GB",
            "used": f"{used // (1024**3)} GB", 
            "free": f"{free // (1024**3)} GB",
            "usage_percent": f"{(used / total * 100):.1f}%"
        }
    except:
        info_data["disks"] = {"error": "Не удалось получить информацию о дисках"}
    
    # Информация о памяти (если доступна)
    try:
        import psutil
        memory = psutil.virtual_memory()
        info_data["memory"] = {
            "total": f"{memory.total // (1024**3)} GB",
            "available": f"{memory.available // (1024**3)} GB",
            "used": f"{memory.used // (1024**3)} GB",
            "percent": f"{memory.percent:.1f}%"
        }
    except ImportError:
        info_data["memory"] = {"info": "Требуется модуль psutil для детальной информации"}
    except:
        info_data["memory"] = {"error": "Не удалось получить информацию о памяти"}
    
    # Информация о CPU (если доступна)
    try:
        import psutil
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        info_data["cpu"] = {
            "cores": cpu_count,
            "frequency": f"{cpu_freq.current:.0f} MHz" if cpu_freq else "Unknown",
            "usage": f"{psutil.cpu_percent(interval=1):.1f}%"
        }
    except ImportError:
        info_data["cpu"] = {"info": "Требуется модуль psutil для детальной информации"}
    except:
        info_data["cpu"] = {"error": "Не удалось получить информацию о процессоре"}
    
    return info_data

def show_pc_info():
    """Показывает красивую информацию о ПК"""
    console.print("\n[bold bright_cyan]💻 Собираю информацию о вашем ПК...[/bold bright_cyan]")
    
    # Показываем анимацию загрузки
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[bold green]🔍 Анализирую систему...", total=None)
        info_data = get_system_info()
    
    console.print("\n")
    
    # Создаем заголовок
    header_panel = Panel(
        f"[bold bright_green]💻 Информация о системе[/bold bright_green]\n\n"
        f"[dim]Детальная информация о вашем компьютере[/dim]",
        title="🖥️ Системная информация",
        border_style="bright_blue"
    )
    console.print(header_panel)
    console.print("")
    
    # Информация об ОС
    os_info = info_data.get("os", {})
    os_panel = Panel(
        f"[bold cyan]🖥️ Операционная система:[/bold cyan] [yellow]{os_info.get('name', 'Unknown')}[/yellow]\n"
        f"[bold cyan]📋 Версия:[/bold cyan] [white]{os_info.get('version', 'Unknown')}[/white]\n"
        f"[bold cyan]🏗️ Архитектура:[/bold cyan] [green]{os_info.get('architecture', 'Unknown')}[/green]\n"
        f"[bold cyan]💻 Платформа:[/bold cyan] [dim]{os_info.get('platform', 'Unknown')}[/dim]",
        title="🖥️ Операционная система",
        border_style="cyan"
    )
    console.print(os_panel)
    console.print("")
    
    # Информация о Python
    python_info = info_data.get("python", {})
    python_panel = Panel(
        f"[bold yellow]🐍 Python версия:[/bold yellow] [white]{python_info.get('version_info', 'Unknown')}[/white]\n"
        f"[bold yellow]📍 Исполняемый файл:[/bold yellow] [dim]{python_info.get('executable', 'Unknown')}[/dim]\n"
        f"[bold yellow]📂 Путь:[/bold yellow] [dim]{python_info.get('path', 'Unknown')}[/dim]",
        title="🐍 Python",
        border_style="yellow"
    )
    console.print(python_panel)
    console.print("")
    
    # Создаем таблицу с остальной информацией
    info_table = Table(title="📊 Дополнительная информация", show_header=True)
    info_table.add_column("🔧 Компонент", style="bold magenta", no_wrap=True)
    info_table.add_column("📊 Значение", style="white")
    info_table.add_column("💡 Статус", style="dim")
    
    # Добавляем информацию о сети
    network_info = info_data.get("network", {})
    if "error" in network_info:
        status = "❌"
        value = network_info["error"]
    else:
        status = "✅"
        value = f"Hostname: {network_info.get('hostname', 'Unknown')}\nIP: {network_info.get('local_ip', 'Unknown')}"
    info_table.add_row("🌐 Сеть", value, status)
    
    # Добавляем информацию о дисках
    disk_info = info_data.get("disks", {})
    if "error" in disk_info:
        status = "❌"
        value = disk_info["error"]
    else:
        status = "✅"
        value = f"Общий: {disk_info.get('total', 'Unknown')}\nИспользовано: {disk_info.get('used', 'Unknown')} ({disk_info.get('usage_percent', 'Unknown')})"
    info_table.add_row("💾 Диски", value, status)
    
    # Добавляем информацию о памяти
    memory_info = info_data.get("memory", {})
    if "error" in memory_info:
        status = "❌"
        value = memory_info["error"]
    elif "info" in memory_info:
        status = "ℹ️"
        value = memory_info["info"]
    else:
        status = "✅"
        value = f"Общая: {memory_info.get('total', 'Unknown')}\nИспользуется: {memory_info.get('used', 'Unknown')} ({memory_info.get('percent', 'Unknown')})"
    info_table.add_row("🧠 Память", value, status)
    
    # Добавляем информацию о процессоре
    cpu_info = info_data.get("cpu", {})
    if "error" in cpu_info:
        status = "❌"
        value = cpu_info["error"]
    elif "info" in cpu_info:
        status = "ℹ️"
        value = cpu_info["info"]
    else:
        status = "✅"
        value = f"Ядер: {cpu_info.get('cores', 'Unknown')}\nЧастота: {cpu_info.get('frequency', 'Unknown')}\nЗагрузка: {cpu_info.get('usage', 'Unknown')}"
    info_table.add_row("⚡ Процессор", value, status)
    
    console.print(info_table)
    console.print("")
    
    # Заключительная панель
    summary_panel = Panel(
        "[bold green]✅ Сбор информации завершен![/bold green]\n\n"
        "[dim]💡 Для получения детальной информации о памяти и процессоре установите:[/dim]\n"
        "[cyan]pip install psutil[/cyan]",
        title="🎉 Готово!",
        border_style="green"
    )
    console.print(summary_panel)
    console.print("")