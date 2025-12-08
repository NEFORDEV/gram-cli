"""GPT чат"""
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

def gpt_chat():
    try:
        from g4f.client import Client
    except ImportError:
        console.print("[red bold]❌ Ошибка: g4f не установлен![/red bold]")
        console.print("[dim]Установите: pip install g4f[/dim]")
        return
    
    gpt_title = Text()
    gpt_title.append("🤖", style="gold1")
    gpt_title.append(" G", style="bold red")
    gpt_title.append("P", style="bold orange1")
    gpt_title.append("T", style="bold yellow") 
    gpt_title.append(" Chat", style="bold green")
    gpt_title.append(" 🤖", style="gold1")
    
    console.print("\n")
    console.print(gpt_title, justify="center")
    console.print("[bold cyan]✨ Интерактивный чат с ИИ ✨[/bold cyan]", justify="center")
    console.print("[dim]💡 Напишите 'exit' для возврата[/dim]", justify="center")
    console.print("\n" + "─" * 80 + "\n")
    
    client = Client()
    
    while True:
        try:
            input_panel = Panel("[bold yellow]💬 Введите ваш запрос:[/bold yellow]\n[dim]💡 Нажмите Enter или 'exit' для выхода[/dim]", title="📝 Ввод", border_style="bright_blue", padding=(1, 2))
            console.print(input_panel)
            
            console.print("[bold bright_yellow]➤ [/bold bright_yellow]", end="")
            user_input = input().strip()
            
            if user_input.lower() == 'exit':
                console.print("\n")
                exit_panel = Panel("[bold green]👋 Спасибо за использование![/bold green]\n[dim]Возвращаемся в меню...[/dim]", title="🚪 Выход", border_style="green", padding=(1, 2))
                console.print(exit_panel)
                console.print("\n")
                break
            
            if not user_input:
                console.print("\n")
                warning_panel = Panel("[bold yellow]⚠️ Пустое сообщение![/bold yellow]\n[dim]Пожалуйста, введите вопрос[/dim]", title="⚠️ Предупреждение", border_style="yellow", padding=(1, 2))
                console.print(warning_panel)
                console.print("\n" + "─" * 80 + "\n")
                continue
            
            console.print("\n")
            user_message_panel = Panel(f"[bold white]{user_input}[/bold white]", title="👤 Вы", border_style="bright_blue", padding=(1, 2))
            console.print(user_message_panel)
            
            console.print("\n[bold green]🤖 ИИ обрабатывает запрос...[/bold green]")
            loading_panel = Panel("[bold green]⏳ Генерация ответа...[/bold green]\n[dim]🔄 Подождите[/dim]", title="⏳ Обработка", border_style="green", padding=(1, 2))
            console.print(loading_panel)
            
            try:
                console.print("[dim]📡 Отправляем запрос...[/dim]")
                
                models = ["gpt-4"]
                response = None
                
                for model in models:
                    try:
                        console.print(f"[dim]🔧 Проверяем модель: {model}[/dim]")
                        response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": user_input}], web_search=False, timeout=30)
                        break
                    except Exception as model_error:
                        console.print(f"[dim]❌ Модель {model} недоступна: {str(model_error)}[/dim]")
                        continue
                
                if response is None:
                    console.print("\n")
                    error_panel = Panel("[bold red]❌ Все модели ИИ недоступны![/bold red]\n[dim]Проверьте интернет и попробуйте позже[/dim]", title="🚫 Ошибка подключения", border_style="red", padding=(1, 2))
                    console.print(error_panel)
                    console.print("\n" + "─" * 80 + "\n")
                    continue
                
                assistant_message = response.choices[0].message.content
                
                console.print("\n")
                
                if len(assistant_message) > 500:
                    parts = [assistant_message[i:i+500] for i in range(0, len(assistant_message), 500)]
                    for i, part in enumerate(parts):
                        if i == 0:
                            ai_message_panel = Panel(f"[bold bright_blue]{part}[/bold bright_blue]\n\n[dim]📄 Ответ продолжен...[/dim]", title=f"🤖 ИИ (часть {i+1}/{len(parts)})", border_style="bright_blue", padding=(1, 2))
                        else:
                            ai_message_panel = Panel(f"[bold bright_blue]{part}[/bold bright_blue]", title=f"🤖 ИИ (часть {i+1}/{len(parts)})", border_style="bright_blue", padding=(1, 2))
                        console.print(ai_message_panel)
                        if i < len(parts) - 1:
                            console.print("\n")
                else:
                    ai_message_panel = Panel(f"[bold bright_blue]{assistant_message}[/bold bright_blue]", title="🤖 ИИ", border_style="bright_blue", padding=(1, 2))
                    console.print(ai_message_panel)
                
                success_panel = Panel("[bold green]✅ Ответ получен![/bold green]\n[dim]💭 Следующий вопрос или 'exit'[/dim]", title="✅ Готово", border_style="green", padding=(1, 2))
                console.print("\n")
                console.print(success_panel)
                console.print("\n" + "─" * 80 + "\n")
                
            except Exception as e:
                console.print("\n")
                error_panel = Panel(f"[bold red]❌ Ошибка: {str(e)}[/bold red]\n[dim]🔄 Попробуйте еще раз[/dim]", title="🚫 Ошибка", border_style="red", padding=(1, 2))
                console.print(error_panel)
                console.print("\n" + "─" * 80 + "\n")
                
        except KeyboardInterrupt:
            console.print("\n\n")
            interrupt_panel = Panel("[bold yellow]⚠️ Прервано пользователем[/bold yellow]\n[dim]🔙 Возвращаемся...[/dim]", title="⏹️ Прерывание", border_style="yellow", padding=(1, 2))
            console.print(interrupt_panel)
            console.print("\n")
            break
        except Exception as e:
            console.print("\n")
            unexpected_error_panel = Panel(f"[bold red]❌ Неожиданная ошибка: {str(e)}[/bold red]\n[dim]🔧 Перезапустите программу[/dim]", title="💥 Критическая ошибка", border_style="red", padding=(1, 2))
            console.print(unexpected_error_panel)
            console.print("\n")
            break