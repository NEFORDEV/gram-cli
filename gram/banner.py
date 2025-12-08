"""Баннеры"""
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import datetime

console = Console()

def get_random_quote():
    quotes = ["Код - поэзия логики", "Создай будущее", "Код приближает к совершенству", "Искусство решать проблемы", "Детективная отладка", "Комментарии для людей"]
    import random
    return random.choice(quotes)

def render_banner():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    
    title = Text()
    title.append("🌟 ", style="gold1")
    title.append("G", style="bold red")
    title.append("R", style="bold orange1") 
    title.append("A", style="bold yellow")
    title.append("M", style="bold green")
    title.append(" 🌟", style="gold1")
    
    subtitle = Text("✨ Анализатор и генератор проектов ✨", style="italic cyan")
    
    console.print("\n")
    console.print(title, justify="center")
    console.print(subtitle, justify="center")
    console.print(f"[dim]🔮 Помощник в мире Python 🔮[/dim]", justify="center")
    console.print("")
    
    info_text = f"[bold cyan]🕐 Запуск:[/bold cyan] [yellow]{time_str}[/yellow]"
    
    info_panel = Panel(info_text, title="📊 Сессия", border_style="bright_blue", padding=(1, 2))
    console.print(info_panel)
    console.print("")
    
    quote = get_random_quote()
    quote_panel = Panel(f"[italic bright_cyan]\"{quote}\"[/italic bright_cyan]", title="💡 Цитата", border_style="green", padding=(1, 2))
    console.print(quote_panel)
    console.print("")
    
    final_panel = Panel("[bold bright_green]✨ Готов к работе![/bold bright_green]\n\n[dim]Используйте [cyan]gram --help[/cyan] для команд[/dim]", title="🚀 Статус", border_style="green")
    console.print(final_panel)
    console.print("")