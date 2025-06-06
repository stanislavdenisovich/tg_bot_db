from .database import create_connection
from .ui import main_hello, main_menu

def main():
    connection = create_connection()
    if connection is None:
        print("Завершение работы программы из-за ошибки подключения.")
        return

    try:
        main_hello(connection)
        main_menu(connection)
    finally:
        connection.close()

if __name__ == '__main__':
    main()
