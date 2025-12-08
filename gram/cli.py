"""Основная логика CLI"""
import argparse
from pathlib import Path

def parse_args():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(prog='gram', add_help=False)
    parser.add_argument('--start', dest='start_flag')
    parser.add_argument('--info', dest='info_flag')
    parser.add_argument('--lint', dest='lint_flag')
    parser.add_argument('--gpt', action='store_true', dest='gpt_flag')
    parser.add_argument('--pc', action='store_true', dest='pc_flag')
    parser.add_argument('--fiat', action='store_true', dest='fiat_flag')
    parser.add_argument('--version', action='store_true', dest='version_flag')
    parser.add_argument('--update', action='store_true', dest='update_flag')
    parser.add_argument('--help-commands', action='store_true', dest='help_commands_flag')
    
    try:
        return parser.parse_args()
    except SystemExit:
        return None

def show_interactive_menu():
    """Показывает интерактивное меню"""
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    
    console = Console()
    
    while True:
        console.clear()
        
        # Создаем красивый заголовок меню
        header_panel = Panel(
            "[bold bright_cyan]🌟 GRAM CLI - Интерактивное меню[/bold bright_cyan]\n\n"
            "[dim]Выберите действие или введите команду[/dim]",
            title="🎮 Интерактивный режим",
            border_style="bright_blue"
        )
        console.print(header_panel)
        console.print("")
        
        # Создаем таблицу с опциями
        menu_table = Table(title="📋 Доступные опции", show_header=True)
        menu_table.add_column("🔢 №", style="bold yellow", no_wrap=True)
        menu_table.add_column("📝 Опция", style="bold cyan")
        menu_table.add_column("📖 Описание", style="white")
        menu_table.add_column("💻 Команда", style="dim")
        
        menu_options = [
            ("1", "🚀 Создать проект", "Создать новый FastAPI проект", "--start fastapi"),
            ("2", "🔍 Анализ кода", "Проанализировать Python файл или папку", "--info <файл>"),
            ("3", "🔧 Проверка кода", "Провести линтинг и проверку качества", "--lint <файл>"),
            ("4", "🤖 GPT чат", "Интерактивный чат с ИИ", "--gpt"),
            ("5", "💻 Системная информация", "Показать информацию о ПК", "--pc"),
            ("6", "💰 Курсы валют", "Показать курсы валют и криптовалют", "--fiat"),
            ("7", "📦 Версия", "Показать версию пакета", "--version"),
            ("8", "🔄 Обновление", "Обновить до последней версии", "--update"),
            ("9", "📚 Справка", "Показать подробную справку", "--help-commands"),
            ("0", "❌ Выход", "Выйти из интерактивного режима", "exit")
        ]
        
        for number, option, description, command in menu_options:
            menu_table.add_row(
                f"[bold]{number}[/bold]",
                f"[bold]{option}[/bold]",
                description,
                f"[dim]{command}[/dim]"
            )
        
        console.print(menu_table)
        console.print("")
        
        # Дополнительная информация
        info_panel = Panel(
            "[bold yellow]💡 Подсказки:[/bold yellow]\n\n"
            "[dim]• Введите номер опции (1-9) для быстрого выбора[/dim]\n"
            "[dim]• Или введите команду напрямую (например: --start fastapi)[/dim]\n"
            "[dim]• Или введите 'exit' для выхода[/dim]",
            title="ℹ️ Как использовать",
            border_style="green"
        )
        console.print(info_panel)
        console.print("")
        
        # Получаем ввод пользователя
        user_input = Prompt.ask("\n[bold cyan]Выберите опцию или введите команду[/bold cyan]").strip().lower()
        
        # Обрабатываем пустой ввод
        if not user_input:
            console.print("\n[dim]⚠️ Вы не ввели команду. Попробуйте еще раз.[/dim]")
            input("[dim]Нажмите Enter для продолжения...[/dim]")
            continue
        
        # Обрабатываем ввод
        if user_input in ['exit', '0', 'quit', 'выход', 'q']:
            console.print("\n[bold green]👋 До свидания! Возвращаемся к командной строке...[/bold green]")
            console.print("")
            break
        
        elif user_input in ['1', 'создать проект', 'start', 'создать']:
            console.print("\n[bold yellow]🚀 Запуск создания FastAPI проекта...[/bold yellow]")
            console.print("")
            from gram.project import create_project
            create_project("fastapi")
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        elif user_input in ['2', 'анализ', 'info', 'анализировать']:
            console.print("\n[bold yellow]🔍 Запуск анализа кода...[/bold yellow]")
            console.print("")
            from gram.analysis import show_info
            file_path = Prompt.ask("[bold cyan]Введите путь к файлу или папке[/bold cyan]")
            show_info(file_path)
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        elif user_input in ['3', 'линт', 'lint', 'проверка']:
            console.print("\n[bold yellow]🔧 Запуск проверки кода...[/bold yellow]")
            console.print("")
            from gram.lint import lint_file
            file_path = Prompt.ask("[bold cyan]Введите путь к файлу или папке[/bold cyan]")
            lint_file(file_path)
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        elif user_input in ['4', 'gpt', 'чат', 'chat', 'ии']:
            console.print("\n[bold yellow]🤖 Запуск GPT чата...[/bold yellow]")
            console.print("")
            from gram.gpt import gpt_chat
            gpt_chat()
            
        elif user_input in ['5', 'система', 'pc', 'системная информация']:
            console.print("\n[bold yellow]💻 Показ системной информации...[/bold yellow]")
            console.print("")
            from gram.system_info import show_pc_info
            show_pc_info()
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        elif user_input in ['6', 'валюты', 'fiat', 'криптовалюта', 'курсы']:
            console.print("\n[bold yellow]💰 Показ курсов валют...[/bold yellow]")
            console.print("")
            from gram.crypto import show_fiat_info
            show_fiat_info()
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        elif user_input in ['7', 'версия', 'version']:
            console.print("\n[bold yellow]📦 Показ версии...[/bold yellow]")
            console.print("")
            from gram.version import show_version
            show_version()
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        elif user_input in ['8', 'обновление', 'update']:
            console.print("\n[bold yellow]🔄 Проверка обновлений...[/bold yellow]")
            console.print("")
            from gram.updater import show_update
            show_update()
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        elif user_input in ['9', 'справка', 'help', 'помощь']:
            console.print("\n[bold yellow]📚 Показ справки...[/bold yellow]")
            console.print("")
            from gram.help import show_detailed_help
            show_detailed_help()
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        # Если введена команда с --
        elif user_input.startswith('--'):
            console.print(f"\n[bold cyan]🔧 Выполняю команду: {user_input}[/bold cyan]")
            console.print("")
            
            # Временно подменяем sys.argv для выполнения команды
            import sys
            old_argv = sys.argv.copy()
            sys.argv = ['gram'] + user_input.split()
            
            try:
                # Выполняем команду как обычно
                if '--start' in user_input:
                    from gram.project import create_project
                    project_name = user_input.split('--start')[1].strip()
                    create_project(project_name)
                elif '--info' in user_input:
                    from gram.analysis import show_info
                    file_path = user_input.split('--info')[1].strip()
                    show_info(file_path)
                elif '--lint' in user_input:
                    from gram.lint import lint_file
                    file_path = user_input.split('--lint')[1].strip()
                    lint_file(file_path)
                elif '--gpt' in user_input:
                    from gram.gpt import gpt_chat
                    gpt_chat()
                elif '--pc' in user_input:
                    from gram.system_info import show_pc_info
                    show_pc_info()
                elif '--fiat' in user_input:
                    from gram.crypto import show_fiat_info
                    show_fiat_info()
                elif '--version' in user_input:
                    from gram.version import show_version
                    show_version()
                elif '--update' in user_input:
                    from gram.updater import show_update
                    show_update()
                elif '--help-commands' in user_input:
                    from gram.help import show_detailed_help
                    show_detailed_help()
                else:
                    console.print(f"[red]❌ Неизвестная команда: {user_input}[/red]")
                    
            finally:
                sys.argv = old_argv
            
            input("\n[dim]Нажмите Enter для возврата в меню...[/dim]")
            
        else:
            console.print(f"\n[red]❌ Неизвестная команда: {user_input}[/red]")
            console.print("[dim]Попробуйте ввести номер опции (1-9) или команду (например: --start fastapi)[/dim]")
            input("\n[dim]Нажмите Enter для продолжения...[/dim]")

def main():
    """Главная функция CLI"""
    import sys
    
    # Проверяем только на явный запрос справки
    if '--help' in sys.argv or '-h' in sys.argv:
        from gram.help import show_quick_help
        show_quick_help()
        return
    
    args = parse_args()
    if args is None:
        from gram.help import show_quick_help
        show_quick_help()
        return
    
    # Импорты для избежания циклических зависимостей
    from gram.banner import render_banner
    from gram.project import create_project
    from gram.analysis import show_info
    from gram.lint import lint_file
    from gram.gpt import gpt_chat
    from gram.system_info import show_pc_info
    from gram.crypto import show_fiat_info
    from gram.version import show_version
    from gram.updater import show_update
    from gram.help import show_detailed_help
    
    # Проверяем флаг справки по командам
    if args.help_commands_flag:
        show_detailed_help()
        return
    
    # Проверяем специальные команды (без баннера)
    if args.version_flag:
        show_version()
        return
    
    if args.update_flag:
        show_update()
        return
    
    # Если нет аргументов, показываем интерактивное меню
    if not any(vars(args).values()):
        show_interactive_menu()
        return
    
    render_banner()
    
    if args.start_flag:
        create_project(args.start_flag)
    elif args.info_flag:
        show_info(args.info_flag)
    elif args.lint_flag:
        lint_file(args.lint_flag)
    elif args.gpt_flag:
        gpt_chat()
    elif args.pc_flag:
        show_pc_info()
    elif args.fiat_flag:
        show_fiat_info()