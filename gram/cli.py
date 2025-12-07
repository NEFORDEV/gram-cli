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
    parser.add_argument('--help-commands', action='store_true', dest='help_commands_flag')
    
    try:
        return parser.parse_args()
    except SystemExit:
        return None

def main():
    """Главная функция CLI"""
    import sys
    
    # Проверяем аргументы командной строки
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
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
    from gram.help import show_detailed_help
    
    # Проверяем флаг справки по командам
    if args.help_commands_flag:
        show_detailed_help()
        return
    
    # Если нет аргументов, показываем красивую справку
    if not any(vars(args).values()):
        from gram.help import show_quick_help
        show_quick_help()
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