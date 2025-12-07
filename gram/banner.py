"""Баннеры и красивый вывод"""
from rich.console import Console
from rich.text import Text
import datetime

console = Console()

def render_banner():
    """Создает красивый баннер"""
    # Создаем красивый заголовок
    title = Text()
    title.append("🌟 ", style="gold1")
    title.append("G", style="bold red")
    title.append("R", style="bold orange1") 
    title.append("A", style="bold yellow")
    title.append("M", style="bold green")
    title.append(" 🌟", style="gold1")
    
    subtitle = Text("✨ Анализатор и генератор проектов нового поколения ✨", style="italic cyan")
    
    # Время запуска с эмодзи
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    console.print("\n")
    console.print(title, justify="center")
    console.print(subtitle, justify="center")
    console.print(f"[dim]🔮 Ваш персональный помощник в мире Python 🔮[/dim]", justify="center")
    console.print(f"[bold cyan]🕐 Запуск: [yellow]{time_str}[/yellow][/bold cyan]", justify="center")
    console.print("\n[dim]✨ Готов к работе! Используйте --help для просмотра команд ✨[/dim]\n")