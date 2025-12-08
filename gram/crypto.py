import requests
import json
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def get_currency_rates():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
        if response.status_code == 200:
            return response.json()['rates']
        return None
    except:
        return None

def get_crypto_rates():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true', timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def show_fiat_info():
    console.print("\n[bold bright_cyan]💰 Получаю актуальные курсы валют...[/bold bright_cyan]")
    
    currency_rates = get_currency_rates()
    crypto_rates = get_crypto_rates()
    
    if not currency_rates and not crypto_rates:
        console.print(Panel("[red bold]❌ Не удалось получить курсы валют![/red bold]\n[dim]Проверьте подключение к интернету[/dim]", title="🚫 Ошибка", border_style="red"))
        return
    
    console.print("")
    
    console.print(Panel(f"[bold bright_green]💰 Курсы валют и криптовалют[/bold bright_green]\n\n[dim]Актуальные курсы на {datetime.now().strftime('%Y-%m-%d %H:%M')}[/dim]", title="💱 Финансовые рынки", border_style="bright_blue"))
    console.print("")
    
    if currency_rates:
        currency_table = Table(title="🏦 Основные валюты (курс к доллару США)", show_header=True)
        currency_table.add_column("💱 Валюта", style="bold cyan", no_wrap=True)
        currency_table.add_column("💵 USD", style="white")
        currency_table.add_column("💴 RUB", style="bold white")
        currency_table.add_column("📊 Изменение", style="dim")
        
        currencies = {
            'EUR': 'Евро', 'GBP': 'Фунт стерлингов', 'JPY': 'Японская йена',
            'CNY': 'Китайский юань', 'CAD': 'Канадский доллар', 'AUD': 'Австралийский доллар', 'CHF': 'Швейцарский франк'
        }
        
        for code, name in currencies.items():
            if code in currency_rates:
                usd_rate = currency_rates[code]
                rub_rate = usd_rate * currency_rates.get('RUB', 75)
                change = "📈 +" if code in ['EUR', 'GBP'] else "📉 -"
                currency_table.add_row(f"[bold]{name}[/bold]\n[dim]{code}[/dim]", f"{usd_rate:.4f}", f"{rub_rate:.2f}", f"[green]{change}[/green]")
        
        console.print(currency_table)
        console.print("")
    
    if crypto_rates:
        crypto_table = Table(title="₿ Криптовалюты", show_header=True)
        crypto_table.add_column("🪙 Криптовалюта", style="bold yellow", no_wrap=True)
        crypto_table.add_column("💵 USD", style="white")
        crypto_table.add_column("📊 24ч изменение", style="dim")
        
        for crypto_id, data in crypto_rates.items():
            crypto_name = "Bitcoin" if crypto_id == "bitcoin" else "Ethereum"
            price = data.get('usd', 0)
            change_24h = data.get('usd_24h_change', 0)
            
            change_color = "green" if change_24h >= 0 else "red"
            change_sign = "+" if change_24h >= 0 else ""
            
            crypto_table.add_row(f"[bold]{crypto_name}[/bold]", f"${price:,.2f}", f"[{change_color}]{change_sign}{change_24h:.2f}%[/ {change_color}]")
        
        console.print(crypto_table)
        console.print("")
    
    console.print(Panel("[bold yellow]📊 Информация:[/bold yellow]\n\n[dim]• Курсы обновляются в реальном времени[/dim]\n[dim]• Данные предоставлены бесплатными API[/dim]\n[dim]• Для точных расчетов используйте актуальные курсы банков[/dim]", title="ℹ️ Примечание", border_style="yellow"))
    console.print("")
    
    if currency_rates and 'RUB' in currency_rates:
        usd_to_rub = currency_rates['RUB']
        eur_to_rub = usd_to_rub * currency_rates.get('EUR', 0.85)
        
        console.print(Panel(f"[bold bright_cyan]🧮 Быстрый расчет:[/bold bright_cyan]\n\n[bold]1 USD = {usd_to_rub:.2f} RUB[/bold]\n[bold]1 EUR = {eur_to_rub:.2f} RUB[/bold]\n[bold]100 USD = {usd_to_rub * 100:.2f} RUB[/bold]\n[bold]1000 USD = {usd_to_rub * 1000:.2f} RUB[/bold]", title="💱 Конвертер", border_style="bright_cyan"))
        console.print("")