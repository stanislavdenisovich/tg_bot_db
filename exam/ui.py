import sys
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import time
import questionary
from .auth import register_user, login_user
from .data_input import manual_data_entry
from .queries import (
    find_students_above_85,
    average_grade,
    faculties_students,
    teachers_students,
    courses_students,
    students_by_teacher,
    students_any_course,
    scourse_max_students,
    students_same_grade,
    faculty_total_credits
)
from .texts import menu_text, welcome_text

console = Console()

def show_success_progress(message: str):
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn(f"[progress.description]{message}"),
        transient=True,
    ) as progress:
        task = progress.add_task(message, total=100)
        for _ in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)

def main_hello(connection):
    while True:
        console.print(
            Panel(
                welcome_text, 
                title="[bold green]Добро Пожаловать[/bold green]", 
                border_style="bright_blue", 
                width=50, 
                padding=(1, 2)
            )
        )
        
        auth_choice = questionary.select(
            "Выберите пункт:",
            choices=[
                "1. Вход",
                "2. Регистрация",
                "0. Выход"
            ]
        ).ask()

        if auth_choice.startswith('1'):
            is_teacher = login_user(connection)
            if is_teacher is not None:
                main_menu(connection, is_teacher)
            else:
                console.print("[bold red]Ошибка входа. Попробуйте снова.[/bold red]")


        elif auth_choice.startswith('2'):
            if register_user(connection):
                show_success_progress("Регистрация прошла успешно. Пожалуйста, войдите...")
            else:
                console.print("[bold red]Ошибка при регистрации. Попробуйте снова.[/bold red]")

        elif auth_choice.startswith('0'):
            with console.status("[bold red]Выход из программы...[/bold red]", spinner="runner"):
                time.sleep(1.5)
            sys.exit()

        else:
            console.print("[bold red]Неверный выбор, попробуйте снова.[/bold red]")


def main_menu(connection, is_teacher):
    while True:
        console.print(Panel(menu_text, title="Главное меню", title_align="center", border_style="magenta"))

        choice = input("Введите номер функции: ").strip()

        if choice == '0':
            with console.status("[bold yellow]Выход на авторизацию...[/bold yellow]", spinner="dots"):
                time.sleep(1.5)
            main_hello(connection)
            return  


        elif choice == '1':
            find_students_above_85(connection)
        elif choice == '2':
            average_grade(connection)
        elif choice == '3':
            faculties_students(connection)
        elif choice == '4':
            teachers_students(connection)
        elif choice == '5':
            courses_students(connection)
        elif choice == '6':
            students_by_teacher(connection)
        elif choice == '7':
            students_any_course(connection)
        elif choice == '8':
            scourse_max_students(connection)
        elif choice == '9':
            students_same_grade(connection)
        elif choice == '10':
            faculty_total_credits(connection)
        elif choice == '11':
            if is_teacher:
                manual_data_entry(connection)
            else:
                console.print(Panel("[bold red]Доступ к этой функции разрешён только преподавателям.[/bold red]", border_style="red", width=50))
        else:
            console.print(Panel("[bold red]Неверный выбор, попробуйте снова.[/bold red]", border_style="red", width=50))
