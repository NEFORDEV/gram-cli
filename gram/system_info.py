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
    
    # Создаем компактную сводку
    summary_panel = Panel(
        f"[bold bright_green]💻 {info_data.get('os', {}).get('name', 'Unknown')} {info_data.get('os', {}).get('version', '')}[/bold bright_green]\n"
        f"[bold yellow]🐍 Python {info_data.get('python', {}).get('version_info', 'Unknown')}[/bold yellow]\n"
        f"[bold cyan]🖥️ {info_data.get('cpu', {}).get('cores', 'Unknown')} ядер | {info_data.get('memory', {}).get('total', 'Unknown')} RAM[/bold cyan]",
        title="🎯 Системная сводка",
        border_style="bright_blue"
    )
    console.print(summary_panel)
    console.print("")
    
    # Основная информация в компактном виде
    main_info_table = Table(title="📊 Основная информация", show_header=True)
    main_info_table.add_column("🔧 Параметр", style="bold cyan", no_wrap=True)
    main_info_table.add_column("📊 Значение", style="white")
    main_info_table.add_column("💡 Статус", style="dim")
    
    # ОС и система
    os_info = info_data.get("os", {})
    main_info_table.add_row(
        "🖥️ Операционная система",
        f"{os_info.get('name', 'Unknown')} {os_info.get('version', '')}",
        "✅"
    )
    
    # Python
    python_info = info_data.get("python", {})
    main_info_table.add_row(
        "🐍 Python версия",
        python_info.get('version_info', 'Unknown'),
        "✅"
    )
    
    # Архитектура
    main_info_table.add_row(
        "🏗️ Архитектура",
        os_info.get('architecture', 'Unknown'),
        "✅"
    )
    
    # Сеть
    network_info = info_data.get("network", {})
    if "error" not in network_info:
        main_info_table.add_row(
            "🌐 Хостнейм",
            network_info.get('hostname', 'Unknown'),
            "✅"
        )
        main_info_table.add_row(
            "📡 IP адрес",
            network_info.get('local_ip', 'Unknown'),
            "✅"
        )
    
    console.print(main_info_table)
    console.print("")
    
    # Производительность в компактном виде
    perf_table = Table(title="⚡ Производительность", show_header=True)
    perf_table.add_column("🔧 Компонент", style="bold yellow", no_wrap=True)
    perf_table.add_column("📊 Показатель", style="white")
    perf_table.add_column("💡 Статус", style="dim")
    
    # CPU
    cpu_info = info_data.get("cpu", {})
    if "error" not in cpu_info:
        perf_table.add_row(
            "⚡ Процессор",
            f"{cpu_info.get('cores', 'Unknown')} ядер | {cpu_info.get('frequency', 'Unknown')}",
            f"[green]{cpu_info.get('usage', 'Unknown')}[/green]"
        )
    
    # Память
    memory_info = info_data.get("memory", {})
    if "error" not in memory_info:
        perf_table.add_row(
            "🧠 Оперативная память",
            f"{memory_info.get('total', 'Unknown')} | Используется {memory_info.get('used', 'Unknown')} ({memory_info.get('percent', 'Unknown')})",
            f"[green]{memory_info.get('percent', 'Unknown')}[/green]" if float(memory_info.get('percent', '0').replace('%', '')) < 80 else f"[yellow]{memory_info.get('percent', 'Unknown')}[/yellow]"
        )
    
    # Диски
    disk_info = info_data.get("disks", {})
    if "error" not in disk_info:
        perf_table.add_row(
            "💾 Дисковое пространство",
            f"Общее: {disk_info.get('total', 'Unknown')} | Свободно: {disk_info.get('free', 'Unknown')}",
            f"[green]{disk_info.get('usage_percent', 'Unknown')}[/green]" if float(disk_info.get('usage_percent', '0').replace('%', '')) < 80 else f"[yellow]{disk_info.get('usage_percent', 'Unknown')}[/yellow]"
        )
    
    console.print(perf_table)
    console.print("")
    
    # Дополнительная информация
    details_panel = Panel(
        f"[bold cyan]📋 Детали системы:[/bold cyan]\n\n"
        f"[dim]🖥️ Платформа:[/dim] {os_info.get('platform', 'Unknown')}\n"
        f"[dim]🔧 Процессор:[/dim] {os_info.get('processor', 'Unknown')}\n"
        f"[dim]🐍 Python путь:[/dim] {python_info.get('path', 'Unknown')}\n"
        f"[dim]📍 Исполняемый файл:[/dim] {python_info.get('executable', 'Unknown')}\n\n"
        f"[bold yellow]💡 Для детальной информации установите:[/bold yellow]\n"
        f"[dim]pip install psutil[/dim]",
        title="🔍 Детали",
        border_style="green"
    )
    console.print(details_panel)
    console.print("")
    
    # Заключительная панель
    final_panel = Panel(
        "[bold green]✅ Сбор информации завершен![/bold green]\n\n"
        "[dim]💡 Информация обновлена в реальном времени[/dim]",
        title="🎉 Готово!",
        border_style="green"
    )
    console.print(final_panel)
    console.print("")