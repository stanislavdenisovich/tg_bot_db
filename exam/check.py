from rich.console import Console
import questionary
from rich.panel import Panel
from rich.prompt import Prompt
import re

console = Console()

def get_valid_username():
    while True:
        console.print(Panel("Введите имя пользователя (только буквы и цифры, от 3 до 20 символов):", border_style="cyan", width=50))
        username = Prompt.ask("[bold cyan]Имя пользователя[/bold cyan]").strip()

        if not re.match(r"^[a-zA-Z0-9]{3,20}$", username):
            console.print("[red]Ошибка: Имя пользователя должно содержать только буквы и цифры, длина от 3 до 20 символов.[/red]")
        else:
            return username

def get_valid_password():
    while True:
        console.print(Panel("Введите пароль (не менее 6 символов):", border_style="cyan", width=50))
        password = Prompt.ask("[bold cyan]Пароль[/bold cyan]", password=True).strip()

        if len(password) < 6:
            console.print("[red]Ошибка: Пароль должен быть не менее 6 символов.[/red]")
        else:
            return password