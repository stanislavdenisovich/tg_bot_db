from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import time
import questionary
from mysql.connector import Error
from .check import get_valid_password, get_valid_username
from .texts import reg_text, log_text, enter_text

console = Console()

from rich.prompt import Prompt
from rich.panel import Panel

def register_user(connection):
    console.print(Panel(reg_text, title="Регистрация", title_align="left", border_style="magenta", width=50))
    
    username = get_valid_username()
    password = get_valid_password()

    role = Prompt.ask(
        "[bold cyan]Выберите роль[/bold cyan]", 
        choices=["учитель", "студент"], 
        default="студент"
    )
    is_teacher = True if role == "учитель" else False

    try:
        with connection.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                console.print(Panel("[bold red]Пользователь с таким именем уже существует.[/bold red]", border_style="red", width=50))
                return False

            cur.execute(
                "INSERT INTO users (username, password, is_teacher) VALUES (%s, %s, %s)",
                (username, password, is_teacher)
            )
            connection.commit()

            console.print(Panel("[bold green]Регистрация успешна![/bold green]", border_style="green", width=50))
            return True

    except Exception as e:
        console.print(Panel(f"[bold red]Ошибка регистрации:[/bold red] {e}", border_style="red", width=50))
        connection.rollback()
        return False


def login_user(connection):
    console.print(Panel(log_text, title="Авторизация", title_align="left", border_style="magenta", width=50))
    
    console.print(Panel("Введите имя пользователя:", border_style="cyan", width=50))
    username = input("> ").strip()

    console.print(Panel("Введите пароль:", border_style="cyan", width=50))
    password = input("> ").strip()

    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT id, is_teacher FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            result = cur.fetchone()

            if result:
                user_id, is_teacher = result

                if is_teacher:
                    role_text = "[bold green]Добро пожаловать, преподаватель![/bold green]"
                else:
                    role_text = "[bold green]Добро пожаловать, студент![/bold green]"

                console.print(Panel(role_text, title="Успешный Вход", title_align="left", border_style="magenta", width=50))
                return is_teacher
            else:
                console.print(Panel("Неверное имя пользователя или пароль.", title="Ошибка", title_align="left", border_style="red", width=50))
                return None

    except Exception as e:
        console.print(Panel(f"Ошибка входа: {e}", title="Ошибка", title_align="left", border_style="red", width=50))
        return None
