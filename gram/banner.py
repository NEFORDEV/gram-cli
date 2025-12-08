"""Баннеры и красивый вывод"""
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
import datetime
import os
import platform

console = Console()

def get_random_quote():
    """Получает случайную мотивационную цитату для разработчиков"""
    quotes = [
        "Код - это поэзия, написанная на языке логики",
        "Лучший способ предсказать будущее - создать его",
        "Каждая строка кода приближает к совершенству",
        "Программирование - это искусство решать проблемы",
        "Код, который вы пишете сегодня, работает завтра",
        "Сложность - враг качества и ясности",
        "Лучший код - это тот, который работает",
        "Отладка - это как быть детективом в детективном романе",
        "Комментарии пишите не для компьютера, а для людей",
        "Идеальный код - это не когда нечего добавить, а когда нечего убрать"
    ]
    import random
    return random.choice(quotes)

def get_system_status():
    """Получает статус системы"""
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        return {
            'cpu': cpu_percent,
            'memory': memory.percent,
            'available': True
        }
    except:
        return {'available': False}

def render_banner():
    """Создает красивый и информативный баннер"""
    # Время запуска
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    
    # Создаем основной заголовок
    title = Text()
    title.append("🌟 ", style="gold1")
    title.append("G", style="bold red")
    title.append("R", style="bold orange1") 
    title.append("A", style="bold yellow")
    title.append("M", style="bold green")
    title.append(" 🌟", style="gold1")
    
    subtitle = Text("✨ Анализатор и генератор проектов нового поколения ✨", style="italic cyan")
    
    console.print("\n")
    console.print(title, justify="center")
    console.print(subtitle, justify="center")
    console.print(f"[dim]🔮 Ваш персональный помощник в мире Python 🔮[/dim]", justify="center")
    console.print("")
    
    # Создаем информационную панель
    info_data = []
    info_data.append(f"[bold cyan]🕐 Запуск:[/bold cyan] [yellow]{time_str}[/yellow]")
    info_data.append(f"[bold cyan]📅 Дата:[/bold cyan] [white]{date_str}[/white]")
    info_data.append(f"[bold cyan]💻 Платформа:[/bold cyan] [green]{platform.system()}[/green]")
    
    # Добавляем статус системы если psutil доступен
    system_status = get_system_status()
    if system_status['available']:
        info_data.append(f"[bold cyan]⚡ CPU:[/bold cyan] [yellow]{system_status['cpu']:.1f}%[/yellow]")
        info_data.append(f"[bold cyan]🧠 RAM:[/bold cyan] [yellow]{system_status['memory']:.1f}%[/yellow]")
    
    info_panel = Panel(
        "\n".join(info_data),
        title="📊 Информация о сессии",
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(info_panel)
    console.print("")
    
    # Показываем мотивационную цитату
    quote = get_random_quote()
    quote_panel = Panel(
        f"[italic bright_cyan]\"{quote}\"[/italic bright_cyan]",
        title="💡 Цитата дня",
        border_style="green",
        padding=(1, 2)
    )
    console.print(quote_panel)
    console.print("")
    
    # Создаем панель быстрого доступа
    quick_access_table = Table(title="⚡ Быстрый доступ", show_header=True)
    quick_access_table.add_column("🚀 Действие", style="bold yellow")
    quick_access_table.add_column("💻 Команда", style="cyan")
    quick_access_table.add_column("📖 Описание", style="white")
    
    quick_access_table.add_row(
        "[bold]Создать проект[/bold]",
        "[cyan]gram --start fastapi[/cyan]",
        "Новый FastAPI проект"
    )
    quick_access_table.add_row(
        "[bold]GPT чат[/bold]",
        "[cyan]gram --gpt[/cyan]",
        "Интерактивный ИИ помощник"
    )
    quick_access_table.add_row(
        "[bold]Анализ кода[/bold]",
        "[cyan]gram --info файл.py[/cyan]",
        "Анализ Python файла"
    )
    quick_access_table.add_row(
        "[bold]Система[/bold]",
        "[cyan]gram --pc[/cyan]",
        "Информация о ПК"
    )
    
    console.print(quick_access_table)
    console.print("")
    
    # Показываем совет дня
    tips = [
        "Используйте gram --lint для проверки качества кода",
        "Запустите gram без аргументов для интерактивного меню",
        "Команда gram --help-commands покажет подробную справку",
        "Используйте gram --update для обновления до последней версии",
        "Для анализа папок используйте gram --info путь/к/папке"
    ]
    
    import random
    tip = random.choice(tips)
    
    tip_panel = Panel(
        f"[bold yellow]💡 Совет дня:[/bold yellow]\n\n"
        f"[bright_cyan]{tip}[/bright_cyan]\n\n"
        f"[dim]Для полного списка команд используйте:[/dim]\n"
        f"[cyan]gram --help-commands[/cyan]",
        title="🎯 Подсказка",
        border_style="magenta",
        padding=(1, 2)
    )
    console.print(tip_panel)
    console.print("")
    
    # Финальная панель
    final_panel = Panel(
        "[bold bright_green]✨ Готов к работе![/bold bright_green]\n\n"
        "[dim]🎮 Интерактивный режим:[/dim] [cyan]gram[/cyan]\n"
        "[dim]📚 Справка:[/dim] [cyan]gram --help[/cyan]\n"
        "[dim]⚡ Все команды:[/dim] [cyan]gram --help-commands[/cyan]",
        title="🚀 Статус",
        border_style="green"
    )
    console.print(final_panel)
    console.print("")