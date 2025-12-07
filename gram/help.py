"""Справка и документация"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_quick_help():
    """Показывает красивую справку по командам"""
    # Создаем красивый заголовок
    header_panel = Panel(
        "[bold bright_cyan]🌟 GRAM CLI - Ваш помощник в Python разработке[/bold bright_cyan]\n\n"
        "[dim]Мощный инструмент для анализа кода и создания проектов[/dim]",
        title="📋 Справка",
        border_style="bright_blue"
    )
    console.print(header_panel)
    
    # Основные команды
    help_table = Table(title="🚀 Доступные команды", show_header=True)
    help_table.add_column("💻 Команда", style="bold cyan", no_wrap=True)
    help_table.add_column("📖 Описание", style="white")
    help_table.add_column("🎯 Использование", style="dim")
    
    commands = [
        ("--start fastapi", "Создать новый FastAPI проект", "gram --start fastapi"),
        ("--info <file>", "Анализ Python файла или папки", "gram --info main.py"),
        ("--lint <file>", "Проверка качества кода", "gram --lint app.py"),
        ("--gpt", "Интерактивный чат с GPT", "gram --gpt"),
        ("--pc", "Информация о системе ПК", "gram --pc"),
        ("--fiat", "Курсы валют и криптовалют", "gram --fiat"),
        ("--version", "Показать версию пакета", "gram --version"),
        ("--update", "Обновить до последней версии", "gram --update"),
        ("--help-commands", "Подробная документация", "gram --help-commands")
    ]
    
    for cmd, desc, usage in commands:
        help_table.add_row(
            f"[bold]{cmd}[/bold]",
            desc,
            f"[dim]{usage}[/dim]"
        )
    
    console.print(help_table)
    
    # Быстрые ссылки
    links_panel = Panel(
        "[bold yellow]🚀 Быстрый старт:[/bold yellow]\n\n"
        "📁 [bold]Создать проект:[/bold] [cyan]gram --start fastapi[/cyan]\n"
        "🤖 [bold]Запустить GPT:[/bold] [cyan]gram --gpt[/cyan]\n"
        "📊 [bold]Анализ файла:[/bold] [cyan]gram --info ваш_файл.py[/cyan]\n\n"
        "[dim]💡 Используйте --help-commands для подробной документации[/dim]",
        title="⚡ Быстрые ссылки",
        border_style="green"
    )
    console.print("\n")
    console.print(links_panel)


def show_detailed_help():
    """показывает подробную справку по всем командам"""
    console.print("\n")
    
    # Заголовок
    title_panel = Panel(
        "[bold cyan]🌟 Добро пожаловать в GRAM CLI![/bold cyan]\n\n"
        "[dim]Ваш персональный помощник для анализа и генерации Python проектов[/dim]",
        title="📖 Подробная документация",
        border_style="bright_cyan"
    )
    console.print(title_panel)
    console.print("\n")
    
    # Команды
    commands_info = [
        {
            "title": "🚀 Команды создания проектов",
            "color": "green",
            "commands": [
                ("--start fastapi", "Создать FastAPI проект с современной структурой")
            ]
        },
        {
            "title": "🤖 Команды ИИ",
            "color": "blue", 
            "commands": [
                ("--gpt", "Интерактивный чат с GPT (Qwen/Qwen3-14B)")
            ]
        },
        {
            "title": "💻 Команды системы",
            "color": "bright_blue", 
            "commands": [
                ("--pc", "Показать полную информацию о системе ПК"),
                ("--fiat", "Показать курсы валют и криптовалют")
            ]
        },
        {
            "title": "🔍 Команды анализа",
            "color": "cyan", 
            "commands": [
                ("--info <файл>", "Показать детальную статистику Python файла"),
                ("--lint <файл>", "Провести проверку качества кода")
            ]
        },
        {
            "title": "📚 Справка и информация",
            "color": "magenta",
            "commands": [
                ("--help-commands", "Показать эту подробную справку"),
                ("--help", "Показать базовую справку по CLI")
            ]
        }
    ]
    
    for section in commands_info:
        section_panel = Panel(
            "\n".join([
                f"[bold {section['color']}]{cmd}[/bold {section['color']}] - {desc}"
                for cmd, desc in section['commands']
            ]),
            title=section['title'],
            border_style=section['color']
        )
        console.print(section_panel)
        console.print("")
    
    # Примеры использования
    examples_panel = Panel(
        "[bold yellow]📝 Примеры использования:[/bold yellow]\n\n"
        "[bold cyan]1.[/bold cyan] Создание FastAPI проекта:\n"
        "   [dim]gram --start fastapi[/dim]\n\n"
        "[bold cyan]2.[/bold cyan] GPT чат с ИИ:\n"
        "   [dim]gram --gpt[/dim]\n\n"
        "[bold cyan]3.[/bold cyan] Информация о ПК:\n"
        "   [dim]gram --pc[/dim]\n\n"
        "[bold cyan]4.[/bold cyan] Курсы валют:\n"
        "   [dim]gram --fiat[/dim]\n\n"
        "[bold cyan]5.[/bold cyan] Анализ файла:\n"
        "   [dim]gram --info main.py[/dim]\n\n"
        "[bold cyan]6.[/bold cyan] Проверка качества:\n"
        "   [dim]gram --lint app.py[/dim]\n\n",
        title="💡 Примеры использования",
        border_style="yellow"
    )
    console.print(examples_panel)
    console.print("\n")
    
    # Возможности
    features_panel = Panel(
        "[bold bright_green]✨ Возможности GRAM CLI:[/bold bright_green]\n\n"
        "🎯 [bold]Генерация FastAPI проектов:[/bold] Быстрое создание современной структуры\n"
        "📊 [bold]Глубокий анализ кода:[/bold] Детальная статистика и метрики Python файлов\n"
        "🔧 [bold]Проверка качества кода:[/bold] Автоматическое выявление проблем и рекомендации\n"
        "🤖 [bold]Интеграция с GPT:[/bold] Интерактивный чат для помощи в разработке\n"
        "💰 [bold]Курсы валют:[/bold] Актуальные курсы валют и криптовалют\n"
        "🖥️ [bold]Информация о системе:[/bold] Детальная информация о ПК\n"
        "🎨 [bold]Красивый интерфейс:[/bold] Rich-текст, таблицы и информативные панели\n"
        "🌈 [bold]Цветной вывод:[/bold] Удобное восприятие информации в консоли",
        title="🌟 Ключевые возможности",
        border_style="bright_green"
    )
    console.print(features_panel)
    console.print("\n")