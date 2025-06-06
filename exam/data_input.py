from rich.console import Console
from rich.table import Table
import questionary
from rich.status import Status
import time

console = Console()

def show_existing_data(connection):
    """Отображает текущие данные в таблицах базы данных."""
    with connection.cursor() as cur:
        cur.execute("SELECT id, name, enrollment_year FROM students")
        students = cur.fetchall()

        cur.execute("SELECT id, name, department FROM teachers")
        teachers = cur.fetchall()

        cur.execute("SELECT id, name, teacher_id FROM courses")
        courses = cur.fetchall()

        cur.execute("SELECT id, name FROM faculties")
        faculties = cur.fetchall()

    def display_table(title, headers, rows):
        table = Table(title=title, show_header=True, header_style="bold magenta")
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*map(str, row))
        console.print(table)

    display_table("Студенты", ["ID", "Имя", "Год поступления"], students)
    display_table("Преподаватели", ["ID", "Имя", "Кафедра"], teachers)
    display_table("Курсы", ["ID", "Название", "ID преподавателя"], courses)
    display_table("Факультеты", ["ID", "Название"], faculties)

def add_student(connection):
    """Добавляет нового студента в базу данных."""
    name = questionary.text("Введите имя студента:").ask()
    faculty_id = questionary.text("Введите ID факультета:").ask()
    enrollment_year = questionary.text("Введите год поступления:").ask()

    with connection.cursor() as cur:
        cur.execute(
            "INSERT INTO students (name, faculty_id, enrollment_year) VALUES (%s, %s, %s)",
            (name, faculty_id, enrollment_year)
        )
        connection.commit()
    console.print(f"[bold green]Студент {name} успешно добавлен![/bold green]")

def add_teacher(connection):
    """Добавляет нового преподавателя в базу данных."""
    name = questionary.text("Введите имя преподавателя:").ask()
    department = questionary.text("Введите кафедру:").ask()
    salary = questionary.text("Введите зарплату:").ask()

    with connection.cursor() as cur:
        cur.execute(
            "INSERT INTO teachers (name, department, salary) VALUES (%s, %s, %s)",
            (name, department, salary)
        )
        connection.commit()
    console.print(f"[bold green]Преподаватель {name} успешно добавлен![/bold green]")

def add_course(connection):
    """Добавляет новый курс в базу данных."""
    name = questionary.text("Введите название курса:").ask()
    teacher_id = questionary.text("Введите ID преподавателя:").ask()
    credits = questionary.text("Введите количество кредитов:").ask()

    with connection.cursor() as cur:
        cur.execute(
            "INSERT INTO courses (name, teacher_id, credits) VALUES (%s, %s, %s)",
            (name, teacher_id, credits)
        )
        connection.commit()
    console.print(f"[bold green]Курс {name} успешно добавлен![/bold green]")

def add_faculty(connection):
    """Добавляет новый факультет в базу данных."""
    name = questionary.text("Введите название факультета:").ask()

    with connection.cursor() as cur:
        cur.execute(
            "INSERT INTO faculties (name) VALUES (%s)",
            (name,)
        )
        connection.commit()
    console.print(f"[bold green]Факультет {name} успешно добавлен![/bold green]")

def manual_data_entry(connection):
    """Основное меню для ввода данных пользователем."""
    while True:
        action = questionary.select(
            "Выберите действие:",
            choices=[
                "Показать текущие данные",
                "Добавить студента",
                "Добавить преподавателя",
                "Добавить курс",
                "Добавить факультет",
                "Выход"
            ]
        ).ask()

        if action == "Показать текущие данные":
            show_existing_data(connection)
        elif action == "Добавить студента":
            add_student(connection)
        elif action == "Добавить преподавателя":
            add_teacher(connection)
        elif action == "Добавить курс":
            add_course(connection)
        elif action == "Добавить факультет":
            add_faculty(connection)
        elif action == "Выход":
            with console.status("[bold yellow]Выход в главное меню...[/bold yellow]", spinner="dots"):
                time.sleep(1.5)           
                break
