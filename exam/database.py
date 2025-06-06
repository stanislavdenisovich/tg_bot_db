import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
from .data_insertion import insert_data 
from rich import print
from rich.console import Console

console = Console()

load_dotenv()

def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="university_database",
            user="postgres",
            password="565009stas",
            host="127.0.0.1"
        )

        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM students")
            count = cur.fetchone()[0]
            if count == 0:
                console.print("[yellow]Таблица пуста. Вставка начальных данных...[/yellow]")
                insert_data(connection)
            else:
                console.print("[green]Подключение успешно. Данные уже существуют.[/green]")

        return connection
    except OperationalError as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")
        return None

