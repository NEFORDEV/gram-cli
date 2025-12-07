"""GPT чат - максимальный минимализм"""
from rich.console import Console
from rich.text import Text
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
            # Простой ввод с указанием стрелки
            console.print("[bold yellow]➤ Введите ваш запрос:[/bold yellow]")
            user_input = input().strip()
            
            # Проверяем команду выхода
            if user_input.lower() == 'exit':
                console.print("\n[bold green]👋 До свидания![/bold green]\n")
                break
            
            # Проверяем пустой ввод
            if not user_input:
                console.print("[dim]⚠️ Пожалуйста, введите запрос[/dim]\n")
                continue
            
            # Показываем введенный текст
            console.print(f"\n[bold white]Вы: {user_input}[/bold white]")
            
            # Показываем генерацию
            console.print("\n[bold green]🤖 ИИ думает...[/bold green]")
            
            # Получаем ответ от GPT - с более надежной моделью
            try:
                console.print("[dim]Отправляю запрос...[/dim]")
                
                # Пробуем разные модели по очереди
                models = ["gpt-4"]
                response = None
                
                for model in models:
                    try:
                        console.print(f"[dim]Пробую модель: {model}[/dim]")
                        response = client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": user_input}],
                            web_search=False,
                            timeout=30  # 30 секунд таймаут
                        )
                        break  # Если успешно, выходим из цикла
                    except Exception as model_error:
                        console.print(f"[dim]Модель {model} не работает: {str(model_error)}[/dim]")
                        continue
                
                if response is None:
                    console.print("\n[red bold]❌ Ни одна модель не отвечает![/red bold]")
                    continue
                
                assistant_message = response.choices[0].message.content
                
                # Показываем ответ
                console.print(f"\n[bold bright_blue]ИИ: {assistant_message}[/bold bright_blue]")
                console.print("\n" + "─" * 50 + "\n")
                
            except Exception as e:
                console.print(f"\n[red bold]❌ Ошибка: {str(e)}[/red bold]")
                console.print("[dim]Попробуйте еще раз или проверьте подключение к интернету[/dim]\n")
                
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]⚠️ Прервано пользователем[/bold yellow]")
            break
        except Exception as e:
            console.print(f"\n[red bold]❌ Неожиданная ошибка: {str(e)}[/red bold]")
            break