"""Проверка качества кода"""
import ast
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def lint_file(path_str: str):
    """Проверяет качество Python файла"""
    path = Path(path_str)
    
    if not path.exists():
        error_panel = Panel(
            f"[red bold]❌ Файл или папка не найдена![/red bold]\n[dim]Путь: {path}[/dim]",
            title="🚫 Ошибка",
            border_style="red"
        )
        console.print(error_panel)
        return

    if path.is_file() and path.suffix == ".py":
        console.print(f"\n[bold cyan]🔍 Проверяю качество кода: [yellow]{path.name}[/yellow][/bold cyan]\n")
        
        code = path.read_text(encoding="utf-8")
        tree = ast.parse(code)
        issues = []
        warnings = []
        
        # Проверяем на различные проблемы
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                for h in node.handlers:
                    if h.type is None:
                        issues.append({
                            "type": "error",
                            "line": node.lineno,
                            "message": "Голый except блок",
                            "severity": "high",
                            "suggestion": "Используйте конкретные исключения"
                        })
        
        lines = code.splitlines()
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            
            # Проверяем длину строки
            if len(line) > 120:
                issues.append({
                    "type": "warning", 
                    "line": i,
                    "message": f"Строка слишком длинная ({len(line)} символов)",
                    "severity": "medium",
                    "suggestion": "Разбейте на несколько строк"
                })
            
            # Проверяем на неиспользуемые импорты (простая проверка)
            if stripped.startswith("import ") or stripped.startswith("from "):
                import_name = stripped.split()[1] if stripped.startswith("import ") else stripped.split()[1]
                if not any(import_name in other_line for other_line in lines[i:] if not other_line.strip().startswith("#")):
                    warnings.append({
                        "type": "info",
                        "line": i,
                        "message": f"Возможно неиспользуемый импорт: {import_name}",
                        "severity": "low",
                        "suggestion": "Удалите неиспользуемые импорты"
                    })
            
            # Проверяем на TODO/FIXME комментарии
            if "TODO" in stripped.upper() or "FIXME" in stripped.upper():
                warnings.append({
                    "type": "info",
                    "line": i,
                    "message": "Найден TODO/FIXME комментарий",
                    "severity": "low",
                    "suggestion": "Не забудьте выполнить задачу"
                })
            
            # Проверяем на print statements в продакшене
            if "print(" in stripped and not stripped.strip().startswith("#"):
                warnings.append({
                    "type": "warning",
                    "line": i,
                    "message": "Использование print() в коде",
                    "severity": "medium",
                    "suggestion": "Используйте logging вместо print"
                })
        
        # Проверяем на магические числа
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, int):
                if node.value in [0, 1, -1, 2]:
                    continue  # Разрешаем часто используемые числа
                elif node.value > 100:
                    warnings.append({
                        "type": "info",
                        "line": getattr(node, 'lineno', 0),
                        "message": f"Магическое число: {node.value}",
                        "severity": "low",
                        "suggestion": "Вынесите в константу"
                    })
        
        # Подсчитываем общую статистику
        total_lines = len(lines)
        empty_lines = sum(1 for line in lines if not line.strip())
        code_lines = total_lines - empty_lines
        comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
        
        # Создаем красивый отчет
        if not issues and not warnings:
            success_panel = Panel(
                "[bold green]🎉 Поздравляем! Проблем не найдено![/bold green]\n"
                f"[cyan]📊 Статистика проверки:[/cyan]\n"
                f"  • [green]Проблем высокого приоритета: 0[/green]\n"
                f"  • [yellow]Предупреждений: 0[/yellow]\n"
                f"  • [blue]Информационных сообщений: 0[/blue]\n\n"
                f"[dim]Ваш код соответствует базовым стандартам качества![/dim]",
                title="✅ Проверка пройдена",
                border_style="green"
            )
            console.print(success_panel)
        else:
            # Создаем панель с общей информацией
            summary_data = [
                f"📊 [bold cyan]Статистика:[/bold cyan]",
                f"  🔴 [red]Проблем высокого приоритета: {len(issues)}[/red]",
                f"  🟡 [yellow]Предупреждений: {len(warnings)}[/yellow]",
                f"  📝 [dim]Всего строк кода: {code_lines}[/dim]",
                f"  💬 [dim]Строк комментариев: {comment_lines}[/dim]"
            ]
            
            summary_panel = Panel(
                "\n".join(summary_data),
                title="📋 Результаты проверки",
                border_style="red" if issues else "yellow"
            )
            console.print(summary_panel)
            console.print("")
            
            # Показываем проблемы
            if issues:
                console.print("[bold red]🔴 Критические проблемы:[/bold red]")
                for i, issue in enumerate(issues, 1):
                    issue_panel = Panel(
                        f"[bold red]{issue['message']}[/bold red]\n"
                        f"[dim]Строка {issue['line']} | {issue['suggestion']}[/dim]",
                        border_style="red"
                    )
                    console.print(f"  {i}. ", end="")
                    console.print(issue_panel)
                console.print("")
            
            # Показываем предупреждения
            if warnings:
                console.print("[bold yellow]🟡 Предупреждения и рекомендации:[/bold yellow]")
                for i, warning in enumerate(warnings, 1):
                    warning_panel = Panel(
                        f"[bold yellow]{warning['message']}[/bold yellow]\n"
                        f"[dim]Строка {warning['line']} | {warning['suggestion']}[/dim]",
                        border_style="yellow"
                    )
                    console.print(f"  {i}. ", end="")
                    console.print(warning_panel)
                console.print("")
            
            # Даем общие рекомендации
            recommendations = []
            if issues:
                recommendations.append("🔧 Исправьте критические проблемы в первую очередь")
            if len(warnings) > 5:
                recommendations.append("📚 Рассмотрите рефакторинг для улучшения читаемости")
            if comment_lines / code_lines < 0.1 if code_lines > 0 else False:
                recommendations.append("📝 Добавьте больше комментариев для улучшения документирования")
            
            if recommendations:
                rec_panel = Panel(
                    "\n".join([f"[dim]{rec}[/dim]" for rec in recommendations]),
                    title="💡 Рекомендации",
                    border_style="blue"
                )
                console.print(rec_panel)
        
        console.print("\n")
    else:
        warning_panel = Panel(
            f"[yellow bold]⚠️ Указанный путь не является Python-файлом![/yellow bold]\n[dim]Путь: {path}[/dim]",
            title="⚠️ Предупреждение",
            border_style="yellow"
        )
        console.print(warning_panel)