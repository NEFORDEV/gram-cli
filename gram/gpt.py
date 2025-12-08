"""GPT чат - максимальный минимализм"""
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import time

console = Console()

def gpt_chat():
    """Интерактивный GPT чат - минимальный интерфейс"""
    try:
        from g4f.client import Client
    except ImportError:
        console.print("[red bold]❌ Ошибка: g4f не установлен![/red bold]")
        console.print("[dim]Установите: pip install g4f[/dim]")
        return
    
    # Создаем красивый заголовок для GPT
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
    console.print("[dim]💡 Напишите 'exit' для возврата в главное меню[/dim]", justify="center")
    console.print("\n" + "─" * 80 + "\n")
    
    # Создаем клиент
    client = Client()
    
    while True:
        try:
            # Красивое поле ввода с индикатором
            input_panel = Panel(
                "[bold yellow]💬 Введите ваш запрос:[/bold yellow]\n"
                "[dim]💡 Нажмите Enter для отправки или 'exit' для выхода[/dim]",
                title="📝 Ввод сообщения",
                border_style="bright_blue",
                padding=(1, 2)
            )
            console.print(input_panel)
            
            # Показываем курсор ввода
            console.print("[bold bright_yellow]➤ [/bold bright_yellow]", end="")
            user_input = input().strip()
            
            # Проверяем команду выхода
            if user_input.lower() == 'exit':
                console.print("\n")
                exit_panel = Panel(
                    "[bold green]👋 Спасибо за использование GPT чата![/bold green]\n"
                    "[dim]Возвращаемся в главное меню Gram...[/dim]",
                    title="🚪 Выход",
                    border_style="green",
                    padding=(1, 2)
                )
                console.print(exit_panel)
                console.print("\n")
                break
            
            # Проверяем пустой ввод
            if not user_input:
                console.print("\n")
                warning_panel = Panel(
                    "[bold yellow]⚠️ Пустое сообщение![/bold yellow]\n"
                    "[dim]Пожалуйста, введите ваш вопрос или запрос[/dim]",
                    title="⚠️ Предупреждение",
                    border_style="yellow",
                    padding=(1, 2)
                )
                console.print(warning_panel)
                console.print("\n" + "─" * 80 + "\n")
                continue
            
            # Красивое отображение введенного сообщения
            console.print("\n")
            user_message_panel = Panel(
                f"[bold white]{user_input}[/bold white]",
                title="👤 Вы",
                border_style="bright_blue",
                padding=(1, 2)
            )
            console.print(user_message_panel)
            
            # Красивый индикатор генерации
            console.print("\n[bold green]🤖 ИИ обрабатывает ваш запрос...[/bold green]")
            
            loading_panel = Panel(
                "[bold green]⏳ Генерация ответа...[/bold green]\n"
                "[dim]🔄 Пожалуйста, подождите[/dim]",
                title="⏳ Обработка",
                border_style="green",
                padding=(1, 2)
            )
            console.print(loading_panel)
            
            # Получаем ответ от GPT - с более надежной моделью
            try:
                console.print("[dim]📡 Отправляем запрос на сервер...[/dim]")
                
                # Пробуем разные модели по очереди
                models = ["gpt-4"]
                response = None
                
                for model in models:
                    try:
                        console.print(f"[dim]🔧 Проверяем модель: {model}[/dim]")
                        response = client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": user_input}],
                            web_search=False,
                            timeout=30  # 30 секунд таймаут
                        )
                        break  # Если успешно, выходим из цикла
                    except Exception as model_error:
                        console.print(f"[dim]❌ Модель {model} недоступна: {str(model_error)}[/dim]")
                        continue
                
                if response is None:
                    console.print("\n")
                    error_panel = Panel(
                        "[bold red]❌ Все модели ИИ недоступны![/bold red]\n"
                        "[dim]Проверьте подключение к интернету и попробуйте позже[/dim]",
                        title="🚫 Ошибка подключения",
                        border_style="red",
                        padding=(1, 2)
                    )
                    console.print(error_panel)
                    console.print("\n" + "─" * 80 + "\n")
                    continue
                
                assistant_message = response.choices[0].message.content
                
                # Красивое отображение ответа ИИ
                console.print("\n")
                
                # Разбиваем длинные ответы на части для лучшего отображения
                if len(assistant_message) > 500:
                    # Для длинных ответов показываем по частям
                    parts = [assistant_message[i:i+500] for i in range(0, len(assistant_message), 500)]
                    for i, part in enumerate(parts):
                        if i == 0:
                            ai_message_panel = Panel(
                                f"[bold bright_blue]{part}[/bold bright_blue]\n\n"
                                "[dim]📄 Ответ продолжен ниже...[/dim]",
                                title=f"🤖 ИИ (часть {i+1}/{len(parts)})",
                                border_style="bright_blue",
                                padding=(1, 2)
                            )
                        else:
                            ai_message_panel = Panel(
                                f"[bold bright_blue]{part}[/bold bright_blue]",
                                title=f"🤖 ИИ (часть {i+1}/{len(parts)})",
                                border_style="bright_blue",
                                padding=(1, 2)
                            )
                        console.print(ai_message_panel)
                        if i < len(parts) - 1:
                            console.print("\n")
                else:
                    # Для коротких ответов показываем целиком
                    ai_message_panel = Panel(
                        f"[bold bright_blue]{assistant_message}[/bold bright_blue]",
                        title="🤖 ИИ",
                        border_style="bright_blue",
                        padding=(1, 2)
                    )
                    console.print(ai_message_panel)
                
                # Панель успешного завершения
                success_panel = Panel(
                    "[bold green]✅ Ответ получен успешно![/bold green]\n"
                    "[dim]💭 Задайте следующий вопрос или введите 'exit' для выхода[/dim]",
                    title="✅ Готово",
                    border_style="green",
                    padding=(1, 2)
                )
                console.print("\n")
                console.print(success_panel)
                console.print("\n" + "─" * 80 + "\n")
                
            except Exception as e:
                console.print("\n")
                error_panel = Panel(
                    f"[bold red]❌ Ошибка при получении ответа: {str(e)}[/bold red]\n"
                    "[dim]🔄 Попробуйте еще раз или проверьте подключение к интернету[/dim]",
                    title="🚫 Ошибка",
                    border_style="red",
                    padding=(1, 2)
                )
                console.print(error_panel)
                console.print("\n" + "─" * 80 + "\n")
                
        except KeyboardInterrupt:
            console.print("\n\n")
            interrupt_panel = Panel(
                "[bold yellow]⚠️ Прервано пользователем[/bold yellow]\n"
                "[dim]🔙 Возвращаемся в главное меню...[/dim]",
                title="⏹️ Прерывание",
                border_style="yellow",
                padding=(1, 2)
            )
            console.print(interrupt_panel)
            console.print("\n")
            break
        except Exception as e:
            console.print("\n")
            unexpected_error_panel = Panel(
                f"[bold red]❌ Неожиданная ошибка: {str(e)}[/bold red]\n"
                "[dim]🔧 Перезапустите программу или обратитесь к разработчику[/dim]",
                title="💥 Критическая ошибка",
                border_style="red",
                padding=(1, 2)
            )
            console.print(unexpected_error_panel)
            console.print("\n")
            break