
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
import requests
import toml
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

console = Console()

def get_github_version():
    try:
        url = "https://raw.githubusercontent.com/NEFORDEV/gram-cli/main/pyproject.toml"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = toml.loads(response.text)
            return data.get('project', {}).get('version', '0.1.0')
        else:
            return None
    except:
        return None

def compare_versions(current, latest):
    try:
        current_parts = [int(x) for x in current.split('.')]
        latest_parts = [int(x) for x in latest.split('.')]
        
        max_len = max(len(current_parts), len(latest_parts))
        current_parts.extend([0] * (max_len - len(current_parts)))
        latest_parts.extend([0] * (max_len - len(latest_parts)))
        
        for i in range(max_len):
            if latest_parts[i] > current_parts[i]:
                return True
            elif latest_parts[i] < current_parts[i]:
                return False
        
        return False
    except:
        return False

def show_update_info(current_version, latest_version):
    console.print("\n")
    
    comparison_table = Table(title="🔄 Сравнение версий", show_header=True)
    comparison_table.add_column("📦 Версия", style="bold cyan", no_wrap=True)
    comparison_table.add_column("📊 Статус", style="white")
    comparison_table.add_column("📅 Дата", style="dim")
    
    comparison_table.add_row(f"[bold]Текущая[/bold]", f"[yellow]{current_version}[/yellow]", "Установлена")
    comparison_table.add_row(f"[bold]Последняя[/bold]", f"[green]{latest_version}[/green]", "Доступна")
    
    console.print(comparison_table)
    console.print("")

def perform_update():
    console.print("\n[bold bright_green]🚀 Начинаю обновление пакета...[/bold bright_green]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TaskProgressColumn(), console=console) as progress:
        task1 = progress.add_task("📥 Скачиваю последнюю версию...", total=None)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            repo_path = temp_path / "gram-cli"
            
            result = subprocess.run(["git", "clone", "https://github.com/NEFORDEV/gram-cli.git", str(repo_path)], capture_output=True, text=True)
            
            if result.returncode != 0:
                console.print(Panel("[red bold]❌ Ошибка при скачивании репозитория![/red bold]\n[dim]{result.stderr}[/dim]", title="🚫 Ошибка", border_style="red"))
                return False
            
            progress.update(task1, description="✅ Скачивание завершено")
            
            task2 = progress.add_task("🔧 Устанавливаю пакет...", total=None)
            
            old_cwd = Path.cwd()
            try:
                import os
                os.chdir(repo_path)
                
                result = subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "."], capture_output=True, text=True)
                
                if result.returncode == 0:
                    progress.update(task2, description="✅ Установка завершена")
                    return True
                else:
                    console.print(Panel("[red bold]❌ Ошибка при установке![/red bold]\n[dim]{result.stderr}[/dim]", title="🚫 Ошибка установки", border_style="red"))
                    return False
            finally:
                os.chdir(old_cwd)
    
    return False

def show_update_result(success):
    if success:
        console.print(Panel("[bold green]🎉 Обновление успешно завершено![/bold green]\n\n[dim]✅ Последняя версия GRAM CLI установлена[/dim]\n[dim]🔄 Перезапустите терминал для полного обновления[/dim]", title="✅ Успех", border_style="green"))
    else:
        console.print(Panel("[red bold]❌ Обновление не удалось![/red bold]\n\n[yellow]Возможные причины:[/yellow]\n[dim]• Нет подключения к интернету[/dim]\n[dim]• Проблемы с правами доступа[/dim]\n[dim]• Ошибки в репозитории[/dim]\n\n[cyan]Попробуйте обновить вручную:[/cyan]\n[dim]pip install --upgrade git+https://github.com/NEFORDEV/gram-cli.git[/dim]", title="❌ Ошибка", border_style="red"))
    
    console.print("")

def show_update():
    from gram.version import get_current_version
    
    current_version = get_current_version()
    console.print(f"\n[bold bright_cyan]🔍 Проверяю последнюю версию на GitHub...[/bold bright_cyan]")
    
    latest_version = get_github_version()
    
    if not latest_version:
        console.print(Panel("[red bold]❌ Не удалось получить информацию о последней версии![/red bold]\n[dim]Проверьте подключение к интернету[/dim]", title="🚫 Ошибка", border_style="red"))
        return
    
    show_update_info(current_version, latest_version)
    
    if compare_versions(current_version, latest_version):
        console.print("[bold yellow]🔄 Доступна новая версия![/bold yellow]\n")
        
        console.print("[bold cyan]Хотите обновить до последней версии? (y/N):[/bold cyan] ", end="")
        choice = input().strip().lower()
        
        if choice in ['y', 'yes', 'да', 'д']:
            success = perform_update()
            show_update_result(success)
        else:
            console.print("\n[dim]Обновление отменено пользователем[/dim]\n")
    else:
        console.print(Panel("[bold green]✅ У вас установлена последняя версия![/bold green]\n\n[dim]Версия {current_version} - актуальна[/dim]", title="🎉 Актуальная версия", border_style="green"))
        console.print("")