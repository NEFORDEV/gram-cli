"""Работа с версиями пакета"""
import pkg_resources
from pathlib import Path
import toml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def get_current_version():
    """Получает текущую версию пакета"""
    try:
        # Пытаемся получить версию из установленного пакета
        version = pkg_resources.get_distribution("gram-cli").version
        return version
    except:
        try:
            # Если не получилось, читаем из pyproject.toml
            pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, 'r') as f:
                    data = toml.load(f)
                    return data.get('project', {}).get('version', '0.1.0')
        except:
            return "0.1.0"

def show_version():
    """Показывает информацию о версии"""
    current_version = get_current_version()
    
    console.print("\n")
    
    # Создаем красивую панель с информацией о версии
    version_panel = Panel(
        f"[bold bright_cyan]📦 Текущая версия:[/bold bright_cyan] [bold white]{current_version}[/bold white]\n\n"
        f"[dim]🔧 GRAM CLI - Ваш помощник в Python разработке[/dim]\n"
        f"[dim]📚 Автор: NEFOR[/dim]\n"
        f"[dim]🐙 GitHub: github.com/NEFORDEV/gram-cli[/dim]",
        title="ℹ️ Информация о версии",
        border_style="bright_blue"
    )
    console.print(version_panel)
    
    # Таблица с дополнительной информацией
    info_table = Table(title="📋 Детали установки", show_header=False)
    info_table.add_column("🔧 Параметр", style="bold cyan")
    info_table.add_column("📊 Значение", style="white")
    
    info_table.add_row("📦 Пакет", "gram-cli")
    info_table.add_row("🐍 Python", ">=3.10")
    info_table.add_row("📋 Лицензия", "MIT")
    info_table.add_row("🔧 Состояние", "[green]Активен[/green]")
    
    console.print("\n")
    console.print(info_table)
    console.print("")
    
    # Панель с командой обновления
    update_panel = Panel(
        "[bold yellow]💡 Для обновления до последней версии:[/bold yellow]\n\n"
        "[cyan]gram --update[/cyan]\n\n"
        "[dim]Эта команда автоматически скачает и установит последнюю версию[/dim]",
        title="🚀 Обновление",
        border_style="green"
    )
    console.print(update_panel)
    console.print("")