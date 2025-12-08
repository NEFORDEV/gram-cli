
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
    path = Path(path_str)
    
    if not path.exists():
        console.print(Panel(f"[red bold]❌ Файл или папка не найдена![/red bold]\n[dim]Путь: {path}[/dim]", title="🚫 Ошибка", border_style="red"))
        return

    console.print(Panel("[bold cyan]🔍 Комплексная проверка качества кода[/bold cyan]\n[dim]Путь: {path}[/dim]", title="🔬 Анализ кода", border_style="bright_blue"))
    console.print("")
    
    if path.is_file() and path.suffix == ".py":
        _check_single_file(path)
    elif path.is_dir():
        _check_directory(path)
    else:
        console.print(Panel(f"[yellow bold]⚠️ Указанный путь не является Python-файлом![[/yellow bold]\n[dim]Путь: {path}[/dim]", title="⚠️ Предупреждение", border_style="yellow"))

def _check_single_file(path: Path):
    console.print(f"[bold cyan]🔍 Анализирую файл: [yellow]{path.name}[/yellow][/bold cyan]\n")
    _check_syntax(path)
    _run_flake8(path)
    _run_pylint(path)
    _run_bandit(path)
    _run_mypy(path)
    _check_black_format(path)
    _run_pytest(path.parent if path.parent != Path(".") else path)

def _check_directory(path: Path):
    console.print(f"[bold cyan]📁 Анализирую папку: [yellow]{path.name}[/yellow][/bold cyan]\n")
    
    python_files = list(path.rglob("*.py"))
    
    if not python_files:
        console.print(Panel("[yellow bold]⚠️ В папке не найдено Python файлов![/yellow bold]", title="🔍 Поиск файлов", border_style="yellow"))
        return
    
    console.print(f"[dim]Найдено {len(python_files)} Python файлов[/dim]\n")
    
    syntax_results = []
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
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
    
    if syntax_results:
        syntax_table = Table(title="📋 Проверка синтаксиса")
        syntax_table.add_column("Файл", style="cyan")
        syntax_table.add_column("Статус", style="bold")
        syntax_table.add_column("Результат", style="white")
        
        for file_path, status, color in syntax_results:
            syntax_table.add_row(str(file_path.relative_to(path)), f"[{color}]{status}[/{color}]", "Синтаксис корректен" if "OK" in status else "Требует исправления")
        
        console.print(syntax_table)
        console.print("")
    
    _run_flake8(path)
    _run_pylint(path)
    _run_bandit(path)
    _run_mypy(path)
    _check_black_format(path)
    _run_pytest(path)

def _check_syntax(path: Path):
    try:
        code = path.read_text(encoding="utf-8")
        ast.parse(code)
        console.print(Panel("[bold green]✅ Синтаксис корректен![/bold green]\n[dim]Файл успешно парсится Python интерпретатором[/dim]", title="🔤 Синтаксис", border_style="green"))
    except SyntaxError as e:
        console.print(Panel(f"[bold red]❌ Синтаксическая ошибка![/bold red]\n[dim]Строка {e.lineno}: {e.msg}[/dim]", title="🚫 Синтаксис", border_style="red"))
    except Exception as e:
        console.print(Panel(f"[bold yellow]⚠️ Ошибка при проверке синтаксиса: {str(e)}[/bold yellow]", title="⚠️ Синтаксис", border_style="yellow"))
    console.print("")

def _run_tool(tool_name: str, args: list, success_msg: str, error_msg: str, target_path: Path, timeout: int = 30):
    try:
        result = subprocess.run([tool_name] + args + [str(target_path)], capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            console.print(Panel(f"[bold green]✅ {success_msg}[/bold green]", title=f"📏 {tool_name}", border_style="green"))
        else:
            issues = result.stdout.strip().split('\n') if result.stdout.strip() else []
            console.print(Panel(f"[bold red]❌ {error_msg}![/bold red]\n[dim]Найдено {len(issues)} проблем[/dim]", title=f"📏 {tool_name}", border_style="red"))
            
            for i, issue in enumerate(issues[:5], 1):
                if issue.strip():
                    console.print(f"  {i}. [red]{issue}[/red]")
            
            if len(issues) > 5:
                console.print(f"  [dim]... и еще {len(issues) - 5} проблем[/dim]")
        
    except FileNotFoundError:
        console.print(Panel(f"[bold yellow]⚠️ {tool_name} не установлен![/bold yellow]\n[dim]Установите: pip install {tool_name}[/dim]", title=f"📏 {tool_name}", border_style="yellow"))
    except subprocess.TimeoutExpired:
        console.print(Panel(f"[bold yellow]⚠️ {tool_name} завис (таймаут)[/bold yellow]", title=f"📏 {tool_name}", border_style="yellow"))
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Ошибка при запуске {tool_name}: {str(e)}[/bold red]", title=f"📏 {tool_name}", border_style="red"))
    
    console.print("")

def _run_flake8(target_path: Path):
    _run_tool("flake8", ["--max-line-length=120", "--extend-ignore=E203,W503"], "Flake8: Проблем не найдено!", "Flake8 нашел проблемы", target_path)

def _run_pylint(target_path: Path):
    _run_tool("pylint", ["--errors-only"], "Pylint: Ошибок не найдено!", "Pylint нашел проблемы", target_path, 60)

def _run_bandit(target_path: Path):
    _run_tool("bandit", ["-r", "-f", "json"], "Bandit: Проблем безопасности не найдено!", "Bandit нашел проблемы безопасности", target_path)

def _run_mypy(target_path: Path):
    _run_tool("mypy", ["--ignore-missing-imports"], "MyPy: Проблем типизации не найдено!", "MyPy нашел проблемы типизации", target_path)

def _check_black_format(target_path: Path):
    try:
        result = subprocess.run(["black", "--check", "--diff", str(target_path)], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            console.print(Panel("[bold green]✅ Black: Код правильно отформатирован![/bold green]", title="🎨 Black", border_style="green"))
        else:
            console.print(Panel("[bold yellow]⚠️ Black: Код нужно отформатировать![/bold yellow]\n[dim]Запустите 'black <файл>' для автоматического форматирования[/dim]", title="🎨 Black", border_style="yellow"))
        
    except FileNotFoundError:
        console.print(Panel("[bold yellow]⚠️ Black не установлен![/bold yellow]\n[dim]Установите: pip install black[/dim]", title="🎨 Black", border_style="yellow"))
    except subprocess.TimeoutExpired:
        console.print(Panel("[bold yellow]⚠️ Black завис (таймаут)[/bold yellow]", title="🎨 Black", border_style="yellow"))
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Ошибка при запуске Black: {str(e)}[/bold red]", title="🎨 Black", border_style="red"))
    
    console.print("")

def _run_pytest(target_path: Path):
    try:
        test_files = list(target_path.rglob("test_*.py")) + list(target_path.rglob("*_test.py"))
        
        if not test_files:
            console.print(Panel("[dim]Тестовые файлы не найдены[/dim]", title="🧪 PyTest", border_style="blue"))
        else:
            console.print(f"[dim]Найдено {len(test_files)} тестовых файлов[/dim]")
            
            result = subprocess.run(["pytest", str(target_path), "-v", "--tb=short"], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                console.print(Panel("[bold green]✅ PyTest: Все тесты прошли успешно![/bold green]", title="🧪 PyTest", border_style="green"))
            else:
                output_lines = result.stdout.strip().split('\n')
                failed_tests = [line for line in output_lines if 'FAILED' in line]
                passed_tests = [line for line in output_lines if 'PASSED' in line]
                
                console.print(Panel(f"[bold red]❌ PyTest: {len(failed_tests)} тестов провалено![/bold red]\n[dim]Пройдено: {len(passed_tests)} | Провалено: {len(failed_tests)}[/dim]", title="🧪 PyTest", border_style="red"))
                
                for i, test in enumerate(failed_tests[:3], 1):
                    console.print(f"  {i}. [red]{test.strip()}[/red]")
                
                if len(failed_tests) > 3:
                    console.print(f"  [dim]... и еще {len(failed_tests) - 3} проваленных тестов[/dim]")
        
    except FileNotFoundError:
        console.print(Panel("[bold yellow]⚠️ PyTest не установлен![/bold yellow]\n[dim]Установите: pip install pytest[/dim]", title="🧪 PyTest", border_style="yellow"))
    except subprocess.TimeoutExpired:
        console.print(Panel("[bold yellow]⚠️ PyTest завис (таймаут)[/bold yellow]", title="🧪 PyTest", border_style="yellow"))
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Ошибка при запуске PyTest: {str(e)}[/bold red]", title="🧪 PyTest", border_style="red"))
    
    console.print("")
    console.print(Panel("[bold cyan]🎯 Комплексная проверка завершена![/bold cyan]\n[dim]Используйте рекомендации выше для улучшения качества кода[/dim]", title="✅ Проверка завершена", border_style="bright_blue"))