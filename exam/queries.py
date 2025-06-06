from rich.console import Console
from rich.table import Table
from mysql.connector import Error

console = Console()

def find_students_above_85(connection):
    query = """
    SELECT students.id, students.name
    FROM students
    JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.grade > 85
    GROUP BY students.id, students.name
    HAVING COUNT(student_courses.course_id) > 3;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        if not results:
            console.print("[yellow]Таких студентов нет.[/yellow]")
            return
        table = Table(title="Студенты, сдавшие более 3 курсов с оценкой выше 85")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Имя", style="magenta")
        for student_id, student_name in results:
            table.add_row(str(student_id), student_name)
        console.print(table)
    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")

def average_grade(connection):
    if connection is None:
        console.print("[red]Нет подключения к базе данных.[/red]")
        return
    query = """
    SELECT students.id, students.name, AVG(student_courses.grade) AS average_grade
    FROM students
    JOIN student_courses ON students.id = student_courses.student_id
    JOIN courses ON student_courses.course_id = courses.id
    JOIN teachers ON courses.teacher_id = teachers.id
    WHERE teachers.department = 'Математика'
    GROUP BY students.id, students.name;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        if not results:
            console.print("[yellow]Не найдено студентов на кафедре 'Математика'.[/yellow]")
            return
        
        table = Table(title="Средняя оценка студентов по курсам кафедры 'Математика'")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Имя", style="magenta")
        table.add_column("Средняя оценка", justify="center", style="green")

        for student_id, student_name, average_grade in results:
            table.add_row(str(student_id), student_name, f"{average_grade:.2f}")

        console.print(table)

    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")

def faculties_students(connection):
    if connection is None:
        console.print("[red]Нет подключения к базе данных.[/red]")
        return
    query = """
    SELECT faculties.id, faculties.name, COUNT(DISTINCT students.id) AS students_with_low_grades
    FROM faculties
    JOIN students ON students.faculty_id = faculties.id
    JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.grade < 50
    GROUP BY faculties.id, faculties.name
    HAVING COUNT(DISTINCT students.id) > 5;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        if not results:
            console.print("[yellow]Таких факультетов нет.[/yellow]")
            return
        
        table = Table(title="Факультеты с более чем 5 студентами, имеющими оценки ниже 50")
        table.add_column("ID факультета", justify="center", style="cyan", no_wrap=True)
        table.add_column("Факультет", style="magenta")
        table.add_column("Студентов с низкими оценками", justify="center", style="red")

        for faculty_id, faculty_name, count_students in results:
            table.add_row(str(faculty_id), faculty_name, str(count_students))

        console.print(table)

    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")


def teachers_students(connection):
    if connection is None:
        console.print("[red]Нет подключения к базе данных.[/red]")
        return
    query = """
    SELECT teachers.id, teachers.name
    FROM teachers
    JOIN courses ON teachers.id = courses.teacher_id
    JOIN student_courses ON courses.id = student_courses.course_id
    GROUP BY teachers.id, teachers.name
    HAVING AVG(student_courses.grade) > 70;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        if not results:
            console.print("[yellow]Нет преподавателей, чьи студенты сдают их курсы на оценку выше 70.[/yellow]")
            return
        
        table = Table(title="Преподаватели, чьи студенты в среднем сдают их курсы на оценку выше 70")
        table.add_column("ID преподавателя", justify="center", style="cyan", no_wrap=True)
        table.add_column("Преподаватель", style="magenta")

        for teacher_id, teacher_name in results:
            table.add_row(str(teacher_id), teacher_name)

        console.print(table)

    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")

def courses_students(connection):
    if connection is None:
        console.print("[red]Нет подключения к базе данных.[/red]")
        return
    query = """
    SELECT courses.id, courses.name
    FROM courses
    JOIN student_courses ON courses.id = student_courses.course_id
    JOIN students ON student_courses.student_id = students.id
    GROUP BY courses.id, courses.name
    HAVING COUNT(DISTINCT students.faculty_id) > 1;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        if not results:
            console.print("[yellow]Таких курсов нет.[/yellow]")
            return
        
        table = Table(title="Курсы, на которые записаны студенты из разных факультетов")
        table.add_column("ID курса", justify="center", style="cyan", no_wrap=True)
        table.add_column("Курс", style="magenta")

        for course_id, course_name in results:
            table.add_row(str(course_id), course_name)

        console.print(table)

    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")


def students_by_teacher(connection, teacher_name='Dr. Ivanov'):
    if connection is None:
        console.print("[red]Нет подключения к базе данных.[/red]")
        return
    query = """
    SELECT students.id, students.name
    FROM students
    WHERE NOT EXISTS (
        SELECT 1
        FROM courses
        JOIN teachers ON courses.teacher_id = teachers.id
        WHERE teachers.name = %s
          AND courses.id NOT IN (
              SELECT student_courses.course_id
              FROM student_courses
              WHERE student_courses.student_id = students.id
          )
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (teacher_name,))
            results = cursor.fetchall()

        if not results:
            console.print(f"[yellow]Нет студентов, записанных на все курсы преподавателя '{teacher_name}'.[/yellow]")
            return
        
        table = Table(title=f"Студенты, записанные на все курсы преподавателя '{teacher_name}'")
        table.add_column("ID студента", justify="center", style="cyan", no_wrap=True)
        table.add_column("Имя студента", style="magenta")

        for student_id, student_name in results:
            table.add_row(str(student_id), student_name)

        console.print(table)

    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")


def students_any_course(connection):
    if connection is None:
        console.print("[red]Нет подключения к базе данных.[/red]")
        return
    query = """
    SELECT students.id, students.name
    FROM students
    LEFT JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.student_id IS NULL;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        if not results:
            console.print("[yellow]Таких студентов нет.[/yellow]")
            return
        
        table = Table(title="Студенты, которые не записаны ни на один курс")
        table.add_column("ID студента", justify="center", style="cyan", no_wrap=True)
        table.add_column("Имя студента", style="magenta")

        for student_id, student_name in results:
            table.add_row(str(student_id), student_name)

        console.print(table)

    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")
        
def scourse_max_students(connection):
    if connection is None:
        print("Нет подключения к базе данных.")
        return
    query = """
    SELECT courses.id, courses.name, COUNT(student_courses.student_id) AS student_count
    FROM courses
    JOIN student_courses ON courses.id = student_courses.course_id
    GROUP BY courses.id, courses.name
    ORDER BY student_count DESC
    LIMIT 1;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        if result:
            course_id, course_name, student_count = result
            print("\n Курс с наибольшим количеством студентов:")
            print(f"ID: {course_id}, Курс: {course_name}, Количество студентов: {student_count}")
        else:
            print("Нет данных о курсах.")
    except Error as e:
        print(f"Ошибка выполнения запроса: {e}")


def students_same_grade(connection):
    if connection is None:
        console.print("[red]Нет подключения к базе данных.[/red]")
        return
    query = """
    SELECT ROUND(avg_grade, 2) AS rounded_average, ARRAY_AGG(name) AS student_names
    FROM (
        SELECT students.name, AVG(student_courses.grade) AS avg_grade
        FROM students
        JOIN student_courses ON students.id = student_courses.student_id
        GROUP BY students.id, students.name
    ) AS averages
    GROUP BY rounded_average
    HAVING COUNT(*) > 1;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        
        if not results:
            console.print("[yellow]Совпадений с одинаковой средней оценкой не найдено.[/yellow]")
            return
        
        table = Table(title="Студенты с одинаковой средней оценкой")
        table.add_column("Средняя оценка", justify="center", style="cyan", no_wrap=True)
        table.add_column("Студенты", style="magenta")
        
        for rounded_average, student_names in results:
            # student_names — это список, преобразуем в строку через запятую
            students_str = ", ".join(student_names)
            table.add_row(str(rounded_average), students_str)
        
        console.print(table)
        
    except Error as e:
        console.print(f"[red]Ошибка выполнения запроса:[/red] {e}")
def faculty_total_credits(connection):
    if connection is None:
        print("Нет подключения к базе данных.")
        return
    query = """
    SELECT faculties.id, faculties.name, SUM(courses.credits) AS total_credits
    FROM faculties
    JOIN students ON students.faculty_id = faculties.id
    JOIN student_courses ON students.id = student_courses.student_id
    JOIN courses ON student_courses.course_id = courses.id
    GROUP BY faculties.id, faculties.name
    ORDER BY total_credits DESC
    LIMIT 1;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        if result:
            faculty_id, faculty_name, total_credits = result
            print("\n Факультет с наибольшим суммарным количеством кредитов у студентов:")
            print(f"ID: {faculty_id}, Факультет: {faculty_name}, Кредиты: {total_credits}")
        else:
            print("Нет данных о факультетах.")
    except Error as e:
        print(f"Ошибка выполнения запроса: {e}")
