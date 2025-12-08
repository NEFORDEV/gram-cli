import ast
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_info(path_str: str):
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
        analyze_single_file(path)
    elif path.is_dir():
        analyze_directory(path)
    else:
        warning_panel = Panel(
            f"[yellow bold]⚠️ Указанный путь не является Python-файлом или папкой![/yellow bold]\n[dim]Путь: {path}[/dim]",
            title="⚠️ Предупреждение",
            border_style="yellow"
        )
        console.print(warning_panel)

def analyze_single_file(path):
    console.print(f"\n[bold cyan]🔍 Анализирую файл: [yellow]{path.name}[/yellow][/bold cyan]\n")
    
    code = path.read_text(encoding="utf-8")
    tree = ast.parse(code)
    
    funcs = sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))
    classes = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
    lines = len(code.splitlines())
    imports = sum(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree))
    comments = code.count("#")
    
    docstrings = sum(isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module)) and 
                    (ast.get_docstring(n) is not None) for n in ast.walk(tree))
    async_funcs = sum(isinstance(n, ast.AsyncFunctionDef) for n in ast.walk(tree))
    
    info_table = Table(title=f"📊 Статистика файла {path.name}", show_header=True)
    info_table.add_column("📈 Метрика", style="bold cyan", no_wrap=True)
    info_table.add_column("📊 Значение", style="bold white")
    info_table.add_column("💡 Оценка", style="dim")
    
    def get_evaluation(metric, value):
        if metric == "Строк кода":
            if value < 50: return "[green]🟢 Отлично[/green]"
            elif value < 200: return "[yellow]🟡 Хорошо[/yellow]"
            else: return "[red]🔴 Много[/red]"
        elif metric == "Функций":
            if value == 0: return "[red]🔴 Нет функций[/red]"
            elif value <= 5: return "[green]🟢 Оптимально[/green]"
            elif value <= 15: return "[yellow]🟡 Нормально[/yellow]"
            else: return "[red]🔴 Слишком много[/red]"
        elif metric == "Классов":
            if value == 0: return "[dim]⚪ Нет классов[/dim]"
            elif value <= 3: return "[green]🟢 Хорошо[/green]"
            elif value <= 8: return "[yellow]🟡 Нормально[/yellow]"
            else: return "[red]🔴 Слишком много[/red]"
        elif metric == "Импортов":
            if value <= 5: return "[green]🟢 Мало[/green]"
            elif value <= 15: return "[yellow]🟡 Нормально[/yellow]"
            else: return "[red]🔴 Много[/red]"
        elif metric == "Комментариев":
            ratio = comments/lines if lines > 0 else 0
            if ratio < 0.1: return "[red]🔴 Мало комментариев[/red]"
            elif ratio < 0.3: return "[yellow]🟡 Нормально[/yellow]"
            else: return "[green]🟢 Хорошо документирован[/green]"
        elif metric == "Docstrings":
            if value == 0: return "[red]🔴 Нет документации[/red]"
            elif value <= max(1, (funcs + classes) // 2): return "[yellow]🟡 Частично[/yellow]"
            else: return "[green]🟢 Хорошо документирован[/green]"
        elif metric == "Async функций":
            if value == 0: return "[dim]⚪ Синхронный код[/dim]"
            elif value <= funcs // 2: return "[green]🟢 Сбалансированно[/green]"
            else: return "[blue]🔵 Много async[/blue]"
        return "[dim]—[/dim]"
    
    metrics = [
        ("Строк кода", lines),
        ("Функций", funcs),
        ("Классов", classes),
        ("Импортов", imports),
        ("Комментариев", comments),
        ("Docstrings", docstrings),
        ("Async функций", async_funcs)
    ]
    
    for metric, value in metrics:
        evaluation = get_evaluation(metric, value)
        info_table.add_row(f"[bold]{metric}[/bold]", f"[bold white]{value:,}[/bold white]" if isinstance(value, int) else str(value), evaluation)
    
    console.print(info_table)
    
    if lines > 0:
        comment_ratio = (comments / lines) * 100
        info_panel = Panel(
            f"[cyan]📏 Размер файла:[/cyan] [yellow]{path.stat().st_size / 1024:.1f} KB[/yellow]\n"
            f"[cyan]📝 Плотность комментариев:[/cyan] [green]{comment_ratio:.1f}%[/green]\n"
            f"[cyan]🎯 Соотношение функций/классов:[/cyan] [yellow]{funcs}:{classes}[/yellow]",
            title="📋 Дополнительная информация",
            border_style="blue"
        )
        console.print("\n")
        console.print(info_panel)
        
        score = 0
        if lines < 200: score += 1
        if funcs <= 15 and funcs > 0: score += 1
        if classes <= 8: score += 1
        if imports <= 15: score += 1
        if comment_ratio >= 10: score += 1
        if docstrings > 0: score += 1
        
        score_emojis = {0: "🔴", 1: "🔴", 2: "🟡", 3: "🟡", 4: "🟢", 5: "🟢", 6: "🌟"}
        score_text = {0: "Требует улучшения", 1: "Нужны изменения", 2: "Удовлетворительно", 
                     3: "Хорошо", 4: "Очень хорошо", 5: "Отлично", 6: "Превосходно"}
        
        score_panel = Panel(
            f"[bold {score // 2 and 'green' or 'yellow' if score >= 3 else 'red'}]"
            f"{score_emojis[score]} Общая оценка: {score}/6 - {score_text[score]}[/bold {score // 2 and 'green' or 'yellow' if score >= 3 else 'red'}]",
            title="🎯 Итоговая оценка",
            border_style="green" if score >= 4 else "yellow" if score >= 2 else "red"
        )
        console.print("\n")
        console.print(score_panel)
    
    console.print("\n")

def analyze_directory(path):
    console.print(f"\n[bold cyan]🔍 Анализирую папку: [yellow]{path.name}[/yellow][/bold cyan]\n")
    
    python_files = list(path.rglob("*.py"))
    
    if not python_files:
        warning_panel = Panel(
            "[yellow bold]⚠️ В папке не найдено Python файлов![/yellow bold]",
            title="⚠️ Предупреждение",
            border_style="yellow"
        )
        console.print(warning_panel)
        return
    
    console.print(f"[dim]Найдено Python файлов: {len(python_files)}[/dim]\n")
    
    total_stats = {"files": 0, "total_lines": 0, "total_funcs": 0, "total_classes": 0, "total_imports": 0, "total_comments": 0, "total_docstrings": 0, "total_async": 0, "total_size": 0}
    
    file_details = []
    
    for py_file in python_files:
        try:
            code = py_file.read_text(encoding="utf-8")
            tree = ast.parse(code)
            
            lines = len(code.splitlines())
            funcs = sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))
            classes = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
            imports = sum(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree))
            comments = code.count("#")
            docstrings = sum(isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module)) and (ast.get_docstring(n) is not None) for n in ast.walk(tree))
            async_funcs = sum(isinstance(n, ast.AsyncFunctionDef) for n in ast.walk(tree))
            
            total_stats["files"] += 1
            total_stats["total_lines"] += lines
            total_stats["total_funcs"] += funcs
            total_stats["total_classes"] += classes
            total_stats["total_imports"] += imports
            total_stats["total_comments"] += comments
            total_stats["total_docstrings"] += docstrings
            total_stats["total_async"] += async_funcs
            total_stats["total_size"] += py_file.stat().st_size
            
            file_details.append({"name": py_file.name, "path": str(py_file.relative_to(path)), "lines": lines, "funcs": funcs, "classes": classes, "imports": imports, "comments": comments, "size": py_file.stat().st_size / 1024})
            
        except Exception as e:
            console.print(f"[red]Ошибка при анализе {py_file.name}: {str(e)}[/red]")
    
    summary_table = Table(title=f"📊 Сводка по папке {path.name}", show_header=True)
    summary_table.add_column("📈 Показатель", style="bold cyan", no_wrap=True)
    summary_table.add_column("📊 Значение", style="bold white")
    summary_table.add_column("💡 Примечание", style="dim")
    
    summary_table.add_row("📁 Файлов", f"[bold white]{total_stats['files']}[/bold white]", "Python файлов найдено")
    summary_table.add_row("📝 Всего строк", f"[bold white]{total_stats['total_lines']:,}[/bold white]", "Строк кода")
    summary_table.add_row("⚡ Функций", f"[bold white]{total_stats['total_funcs']:,}[/bold white]", "Всего функций")
    summary_table.add_row("🏗️ Классов", f"[bold white]{total_stats['total_classes']:,}[/bold white]", "Всего классов")
    summary_table.add_row("📦 Импортов", f"[bold white]{total_stats['total_imports']:,}[/bold white]", "Всего импортов")
    summary_table.add_row("💬 Комментариев", f"[bold white]{total_stats['total_comments']:,}[/bold white]", "Строк комментариев")
    summary_table.add_row("📖 Docstrings", f"[bold white]{total_stats['total_docstrings']:,}[/bold white]", "Документированных элементов")
    summary_table.add_row("⚡ Async функций", f"[bold white]{total_stats['total_async']:,}[/bold white]", "Асинхронных функций")
    summary_table.add_row("💾 Размер", f"[bold white]{total_stats['total_size'] / 1024:.1f} MB[/bold white]", "Общий размер файлов")
    
    console.print(summary_table)
    console.print("")
    
    if file_details:
        top_files_table = Table(title="📋 Топ файлов по размеру", show_header=True)
        top_files_table.add_column("📄 Файл", style="bold white")
        top_files_table.add_column("📝 Строк", style="cyan")
        top_files_table.add_column("⚡ Функций", style="yellow")
        top_files_table.add_column("💾 Размер", style="dim")
        
        sorted_files = sorted(file_details, key=lambda x: x["size"], reverse=True)[:10]
        
        for file_info in sorted_files:
            top_files_table.add_row(f"[bold]{file_info['name']}[/bold]", f"{file_info['lines']:,}", f"{file_info['funcs']}", f"{file_info['size']:.1f} KB")
        
        console.print(top_files_table)
        console.print("")
    
    if total_stats["total_lines"] > 0:
        comment_ratio = (total_stats["total_comments"] / total_stats["total_lines"]) * 100
        
        score = 0
        if total_stats["total_lines"] < 1000: score += 1
        if total_stats["total_funcs"] / max(total_stats["files"], 1) < 10: score += 1
        if total_stats["total_classes"] / max(total_stats["files"], 1) < 5: score += 1
        if total_stats["total_imports"] / max(total_stats["files"], 1) < 20: score += 1
        if comment_ratio >= 10: score += 1
        if total_stats["total_docstrings"] > 0: score += 1
        
        score_emojis = {0: "🔴", 1: "🔴", 2: "🟡", 3: "🟡", 4: "🟢", 5: "🟢", 6: "🌟"}
        score_text = {0: "Требует улучшения", 1: "Нужны изменения", 2: "Удовлетворительно", 3: "Хорошо", 4: "Очень хорошо", 5: "Отлично", 6: "Превосходно"}
        
        score_panel = Panel(
            f"[bold {score // 2 and 'green' or 'yellow' if score >= 3 else 'red'}]"
            f"{score_emojis[score]} Общая оценка проекта: {score}/6 - {score_text[score]}[/bold {score // 2 and 'green' or 'yellow' if score >= 3 else 'red'}]",
            title="🎯 Итоговая оценка проекта",
            border_style="green" if score >= 4 else "yellow" if score >= 2 else "red"
        )
        console.print(score_panel)
    
    console.print("")