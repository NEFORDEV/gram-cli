"""Проверка качества кода"""
import ast
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def lint_file(path_str: str):
    """Проверяет качество Python файла с помощью различных инструментов"""
    path = Path(path_str)
    
    if not path.exists():
        error_panel = Panel(
            f"[red bold]❌ Файл или папка не найдена![/red bold]\n[dim]Путь: {path}[/dim]",
            title="🚫 Ошибка",
            border_style="red"
        )
        console.print(error_panel)
        return

    # Создаем заголовок проверки
    header_panel = Panel(
        "[bold cyan]🔍 Комплексная проверка качества кода[/bold cyan]\n"
        f"[dim]Путь: {path}[/dim]",
        title="🔬 Анализ кода",
        border_style="bright_blue"
    )
    console.print(header_panel)
    console.print("")

    if path.is_file() and path.suffix == ".py":
        # Проверяем один файл
        _check_single_file(path)
    elif path.is_dir():
        # Проверяем папку
        _check_directory(path)
    else:
        warning_panel = Panel(
            f"[yellow bold]⚠️ Указанный путь не является Python-файлом или папкой![/yellow bold]\n[dim]Путь: {path}[/dim]",
            title="⚠️ Предупреждение",
            border_style="yellow"
        )
        console.print(warning_panel)

def _check_single_file(path: Path):
    """Проверяет одиночный файл"""
    console.print(f"[bold cyan]🔍 Анализирую файл: [yellow]{path.name}[/yellow][/bold cyan]\n")
    
    # Проверяем синтаксис
    _check_syntax(path)
    
    # Запускаем flake8
    _run_flake8(path)
    
    # Запускаем pylint
    _run_pylint(path)
    
    # Проверяем безопасность с bandit
    _run_bandit(path)
    
    # Проверяем типизацию с mypy
    _run_mypy(path)
    
    # Проверяем форматирование с black
    _check_black_format(path)
    
    # Запускаем тесты если есть
    _run_pytest(path.parent if path.parent != Path(".") else path)

def _check_directory(path: Path):
    """Проверяет папку с проектом"""
    console.print(f"[bold cyan]📁 Анализирую папку: [yellow]{path.name}[/yellow][/bold cyan]\n")
    
    # Ищем все Python файлы
    python_files = list(path.rglob("*.py"))
    
    if not python_files:
        warning_panel = Panel(
            "[yellow bold]⚠️ В папке не найдено Python файлов![/yellow bold]",
            title="🔍 Поиск файлов",
            border_style="yellow"
        )
        console.print(warning_panel)
        return
    
    console.print(f"[dim]Найдено {len(python_files)} Python файлов[/dim]\n")
    
    # Проверяем синтаксис всех файлов
    syntax_results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("🔍 Проверка синтаксиса...", total=len(python_files))
        
        for py_file in python_files:
            try:
                py_file.read_text(encoding="utf-8")
                ast.parse(py_file.read_text(encoding="utf-8"))
                syntax_results.append((py_file, "✅ OK", "green"))
            except SyntaxError as e:
                syntax_results.append((py_file, f"❌ Синтаксическая ошибка: {e}", "red"))
            except Exception as e:
                syntax_results.append((py_file, f"⚠️ Ошибка: {e}", "yellow"))
            progress.advance(task)
    
    # Показываем результаты проверки синтаксиса
    if syntax_results:
        syntax_table = Table(title="📋 Проверка синтаксиса")
        syntax_table.add_column("Файл", style="cyan")
        syntax_table.add_column("Статус", style="bold")
        syntax_table.add_column("Результат", style="white")
        
        for file_path, status, color in syntax_results:
            syntax_table.add_row(
                str(file_path.relative_to(path)),
                f"[{color}]{status}[/{color}]",
                "Синтаксис корректен" if "OK" in status else "Требует исправления"
            )
        
        console.print(syntax_table)
        console.print("")
    
    # Запускаем flake8 на всю папку
    _run_flake8(path)
    
    # Запускаем pylint на всю папку
    _run_pylint(path)
    
    # Проверяем безопасность
    _run_bandit(path)
    
    # Проверяем типизацию
    _run_mypy(path)
    
    # Проверяем форматирование
    _check_black_format(path)
    
    # Ищем и запускаем тесты
    _run_pytest(path)

def _check_syntax(path: Path):
    """Проверяет синтаксис файла"""
    try:
        code = path.read_text(encoding="utf-8")
        ast.parse(code)
        
        success_panel = Panel(
            "[bold green]✅ Синтаксис корректен![/bold green]\n"
            "[dim]Файл успешно парсится Python интерпретатором[/dim]",
            title="🔤 Синтаксис",
            border_style="green"
        )
        console.print(success_panel)
        
    except SyntaxError as e:
        error_panel = Panel(
            f"[bold red]❌ Синтаксическая ошибка![/bold red]\n"
            f"[dim]Строка {e.lineno}: {e.msg}[/dim]",
            title="🚫 Синтаксис",
            border_style="red"
        )
        console.print(error_panel)
        
    except Exception as e:
        warning_panel = Panel(
            f"[bold yellow]⚠️ Ошибка при проверке синтаксиса: {str(e)}[/bold yellow]",
            title="⚠️ Синтаксис",
            border_style="yellow"
        )
        console.print(warning_panel)
    
    console.print("")

def _run_flake8(target_path: Path):
    """Запускает flake8 для проверки стиля кода"""
    try:
        result = subprocess.run(
            ["flake8", str(target_path), "--max-line-length=120", "--extend-ignore=E203,W503"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            success_panel = Panel(
                "[bold green]✅ Flake8: Проблем не найдено![/bold green]\n"
                "[dim]Код соответствует стандартам PEP 8[/dim]",
                title="📏 Flake8 (стиль кода)",
                border_style="green"
            )
            console.print(success_panel)
        else:
            issues = result.stdout.strip().split('\n') if result.stdout.strip() else []
            error_panel = Panel(
                f"[bold red]❌ Flake8 нашел {len(issues)} проблем![/bold red]\n"
                f"[dim]Нарушения стиля кода и потенциальные ошибки[/dim]",
                title="📏 Flake8",
                border_style="red"
            )
            console.print(error_panel)
            
            # Показываем первые 10 проблем
            for i, issue in enumerate(issues[:10], 1):
                if issue.strip():
                    console.print(f"  {i}. [red]{issue}[/red]")
            
            if len(issues) > 10:
                console.print(f"  [dim]... и еще {len(issues) - 10} проблем[/dim]")
        
    except FileNotFoundError:
        warning_panel = Panel(
            "[bold yellow]⚠️ Flake8 не установлен![/bold yellow]\n"
            "[dim]Установите: pip install flake8[/dim]",
            title="📏 Flake8",
            border_style="yellow"
        )
        console.print(warning_panel)
    except subprocess.TimeoutExpired:
        warning_panel = Panel(
            "[bold yellow]⚠️ Flake8 завис (таймаут)[/bold yellow]",
            title="📏 Flake8",
            border_style="yellow"
        )
        console.print(warning_panel)
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Ошибка при запуске Flake8: {str(e)}[/bold red]",
            title="📏 Flake8",
            border_style="red"
        )
        console.print(error_panel)
    
    console.print("")

def _run_pylint(target_path: Path):
    """Запускает pylint для глубокого анализа кода"""
    try:
        result = subprocess.run(
            ["pylint", str(target_path), "--errors-only"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            success_panel = Panel(
                "[bold green]✅ Pylint: Ошибок не найдено![/bold green]\n"
                "[dim]Код прошел проверку на критические ошибки[/dim]",
                title="🔍 Pylint (глубокий анализ)",
                border_style="green"
            )
            console.print(success_panel)
        else:
            issues = result.stdout.strip().split('\n') if result.stdout.strip() else []
            error_panel = Panel(
                f"[bold red]❌ Pylint нашел проблемы![/bold red]\n"
                f"[dim]Обнаружены потенциальные ошибки и проблемы[/dim]",
                title="🔍 Pylint",
                border_style="red"
            )
            console.print(error_panel)
            
            # Показываем первые 5 критических проблем
            critical_issues = []
            for issue in issues:
                if any(keyword in issue.upper() for keyword in ['ERROR', 'FATAL', 'CRITICAL']):
                    critical_issues.append(issue)
            
            for i, issue in enumerate(critical_issues[:5], 1):
                if issue.strip():
                    console.print(f"  {i}. [red]{issue}[/red]")
            
            if len(critical_issues) > 5:
                console.print(f"  [dim]... и еще {len(critical_issues) - 5} критических проблем[/dim]")
        
    except FileNotFoundError:
        warning_panel = Panel(
            "[bold yellow]⚠️ Pylint не установлен![/bold yellow]\n"
            "[dim]Установите: pip install pylint[/dim]",
            title="🔍 Pylint",
            border_style="yellow"
        )
        console.print(warning_panel)
    except subprocess.TimeoutExpired:
        warning_panel = Panel(
            "[bold yellow]⚠️ Pylint завис (таймаут)[/bold yellow]",
            title="🔍 Pylint",
            border_style="yellow"
        )
        console.print(warning_panel)
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Ошибка при запуске Pylint: {str(e)}[/bold red]",
            title="🔍 Pylint",
            border_style="red"
        )
        console.print(error_panel)
    
    console.print("")

def _run_bandit(target_path: Path):
    """Запускает bandit для проверки безопасности"""
    try:
        result = subprocess.run(
            ["bandit", "-r", str(target_path), "-f", "json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            success_panel = Panel(
                "[bold green]✅ Bandit: Проблем безопасности не найдено![/bold green]\n"
                "[dim]Код прошел базовую проверку безопасности[/dim]",
                title="🔒 Bandit (безопасность)",
                border_style="green"
            )
            console.print(success_panel)
        else:
            try:
                import json
                report = json.loads(result.stdout)
                issues = report.get('results', [])
                
                error_panel = Panel(
                    f"[bold red]❌ Bandit нашел {len(issues)} проблем безопасности![/bold red]\n"
                    f"[dim]Обнаружены потенциальные уязвимости[/dim]",
                    title="🔒 Bandit",
                    border_style="red"
                )
                console.print(error_panel)
                
                # Показываем первые 5 проблем
                for i, issue in enumerate(issues[:5], 1):
                    console.print(f"  {i}. [red]{issue.get('test_id', '')}: {issue.get('issue_text', '')}[/red]")
                
                if len(issues) > 5:
                    console.print(f"  [dim]... и еще {len(issues) - 5} проблем[/dim]")
                    
            except json.JSONDecodeError:
                # Если не удалось распарсить JSON, показываем сырой вывод
                error_panel = Panel(
                    f"[bold red]❌ Bandit обнаружил проблемы безопасности![/bold red]\n"
                    f"[dim]Проверьте вывод bandit вручную[/dim]",
                    title="🔒 Bandit",
                    border_style="red"
                )
                console.print(error_panel)
        
    except FileNotFoundError:
        warning_panel = Panel(
            "[bold yellow]⚠️ Bandit не установлен![/bold yellow]\n"
            "[dim]Установите: pip install bandit[/dim]",
            title="🔒 Bandit",
            border_style="yellow"
        )
        console.print(warning_panel)
    except subprocess.TimeoutExpired:
        warning_panel = Panel(
            "[bold yellow]⚠️ Bandit завис (таймаут)[/bold yellow]",
            title="🔒 Bandit",
            border_style="yellow"
        )
        console.print(warning_panel)
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Ошибка при запуске Bandit: {str(e)}[/bold red]",
            title="🔒 Bandit",
            border_style="red"
        )
        console.print(error_panel)
    
    console.print("")

def _run_mypy(target_path: Path):
    """Запускает mypy для проверки типизации"""
    try:
        result = subprocess.run(
            ["mypy", str(target_path), "--ignore-missing-imports"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            success_panel = Panel(
                "[bold green]✅ MyPy: Проблем типизации не найдено![/bold green]\n"
                "[dim]Код корректно типизирован или не требует типизации[/dim]",
                title="🔤 MyPy (типизация)",
                border_style="green"
            )
            console.print(success_panel)
        else:
            issues = result.stdout.strip().split('\n') if result.stdout.strip() else []
            warning_panel = Panel(
                f"[bold yellow]⚠️ MyPy нашел проблемы типизации![/bold yellow]\n"
                f"[dim]Обнаружены потенциальные проблемы с типами[/dim]",
                title="🔤 MyPy",
                border_style="yellow"
            )
            console.print(warning_panel)
            
            # Показываем первые 5 проблем
            for i, issue in enumerate(issues[:5], 1):
                if issue.strip():
                    console.print(f"  {i}. [yellow]{issue}[/yellow]")
            
            if len(issues) > 5:
                console.print(f"  [dim]... и еще {len(issues) - 5} проблем[/dim]")
        
    except FileNotFoundError:
        warning_panel = Panel(
            "[bold yellow]⚠️ MyPy не установлен![/bold yellow]\n"
            "[dim]Установите: pip install mypy[/dim]",
            title="🔤 MyPy",
            border_style="yellow"
        )
        console.print(warning_panel)
    except subprocess.TimeoutExpired:
        warning_panel = Panel(
            "[bold yellow]⚠️ MyPy завис (таймаут)[/bold yellow]",
            title="🔤 MyPy",
            border_style="yellow"
        )
        console.print(warning_panel)
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Ошибка при запуске MyPy: {str(e)}[/bold red]",
            title="🔤 MyPy",
            border_style="red"
        )
        console.print(error_panel)
    
    console.print("")

def _check_black_format(target_path: Path):
    """Проверяет форматирование с помощью black"""
    try:
        result = subprocess.run(
            ["black", "--check", "--diff", str(target_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            success_panel = Panel(
                "[bold green]✅ Black: Код правильно отформатирован![/bold green]\n"
                "[dim]Код соответствует стандартам форматирования Black[/dim]",
                title="🎨 Black (форматирование)",
                border_style="green"
            )
            console.print(success_panel)
        else:
            warning_panel = Panel(
                "[bold yellow]⚠️ Black: Код нужно отформатировать![/bold yellow]\n"
                "[dim]Запустите 'black <файл>' для автоматического форматирования[/dim]",
                title="🎨 Black",
                border_style="yellow"
            )
            console.print(warning_panel)
            
            # Показываем diff (первые несколько строк)
            if result.stdout:
                diff_lines = result.stdout.split('\n')[:10]
                for line in diff_lines:
                    if line.strip():
                        console.print(f"  [dim]{line}[/dim]")
                
                if len(result.stdout.split('\n')) > 10:
                    console.print("  [dim]... (показаны первые 10 строк diff)[/dim]")
        
    except FileNotFoundError:
        warning_panel = Panel(
            "[bold yellow]⚠️ Black не установлен![/bold yellow]\n"
            "[dim]Установите: pip install black[/dim]",
            title="🎨 Black",
            border_style="yellow"
        )
        console.print(warning_panel)
    except subprocess.TimeoutExpired:
        warning_panel = Panel(
            "[bold yellow]⚠️ Black завис (таймаут)[/bold yellow]",
            title="🎨 Black",
            border_style="yellow"
        )
        console.print(warning_panel)
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Ошибка при запуске Black: {str(e)}[/bold red]",
            title="🎨 Black",
            border_style="red"
        )
        console.print(error_panel)
    
    console.print("")

def _run_pytest(target_path: Path):
    """Запускает pytest для проверки тестов"""
    try:
        # Ищем тесты в директории
        test_files = list(target_path.rglob("test_*.py")) + list(target_path.rglob("*_test.py"))
        
        if not test_files:
            info_panel = Panel(
                "[dim]Тестовые файлы не найдены[/dim]\n"
                "[dim]Создайте файлы test_*.py или *_test.py для автоматической проверки[/dim]",
                title="🧪 PyTest (тестирование)",
                border_style="blue"
            )
            console.print(info_panel)
        else:
            console.print(f"[dim]Найдено {len(test_files)} тестовых файлов[/dim]")
            
            result = subprocess.run(
                ["pytest", str(target_path), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                success_panel = Panel(
                    "[bold green]✅ PyTest: Все тесты прошли успешно![/bold green]\n"
                    "[dim]Ваш код покрыт тестами и работает корректно[/dim]",
                    title="🧪 PyTest",
                    border_style="green"
                )
                console.print(success_panel)
            else:
                # Анализируем результаты тестов
                output_lines = result.stdout.strip().split('\n')
                failed_tests = [line for line in output_lines if 'FAILED' in line]
                passed_tests = [line for line in output_lines if 'PASSED' in line]
                
                error_panel = Panel(
                    f"[bold red]❌ PyTest: {len(failed_tests)} тестов провалено![/bold red]\n"
                    f"[dim]Пройдено: {len(passed_tests)} | Провалено: {len(failed_tests)}[/dim]",
                    title="🧪 PyTest",
                    border_style="red"
                )
                console.print(error_panel)
                
                # Показываем первые 3 проваленных теста
                for i, test in enumerate(failed_tests[:3], 1):
                    console.print(f"  {i}. [red]{test.strip()}[/red]")
                
                if len(failed_tests) > 3:
                    console.print(f"  [dim]... и еще {len(failed_tests) - 3} проваленных тестов[/dim]")
        
    except FileNotFoundError:
        warning_panel = Panel(
            "[bold yellow]⚠️ PyTest не установлен![/bold yellow]\n"
            "[dim]Установите: pip install pytest[/dim]",
            title="🧪 PyTest",
            border_style="yellow"
        )
        console.print(warning_panel)
    except subprocess.TimeoutExpired:
        warning_panel = Panel(
            "[bold yellow]⚠️ PyTest завис (таймаут)[/bold yellow]",
            title="🧪 PyTest",
            border_style="yellow"
        )
        console.print(warning_panel)
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Ошибка при запуске PyTest: {str(e)}[/bold red]",
            title="🧪 PyTest",
            border_style="red"
        )
        console.print(error_panel)
    
    console.print("")
    
    # Итоговая панель
    final_panel = Panel(
        "[bold cyan]🎯 Комплексная проверка завершена![/bold cyan]\n"
        "[dim]Используйте рекомендации выше для улучшения качества кода[/dim]\n"
        "[dim]💡 Установите недостающие инструменты для полной проверки[/dim]",
        title="✅ Проверка завершена",
        border_style="bright_blue"
    )
    console.print(final_panel)