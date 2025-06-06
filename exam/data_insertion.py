def insert_data(connection):
    with connection.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO faculties (name) VALUES
                ('Факультет информатики'),
                ('Факультет экономики'),
                ('Факультет математики'),
                ('Факультет физики')
                RETURNING id, name;
            """)
            faculties = cur.fetchall()
            faculty_ids = {name: id for id, name in faculties}

            cur.execute("""
                INSERT INTO teachers (name, department, salary) VALUES
                ('Алексей Смирнов', 'Информатика', 75000.00),
                ('Ольга Кузнецова', 'Экономика', 68000.00),
                ('Виктор Павлов', 'Математика', 70000.00),
                ('Екатерина Иванова', 'Физика', 72000.00),
                ('Игорь Сидоров', 'Информатика', 77000.00)
                RETURNING id, name;
            """)
            teachers = cur.fetchall()
            teacher_ids = {name: id for id, name in teachers}

            cur.execute("""
                INSERT INTO courses (name, teacher_id, credits) VALUES
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s);
            """, (
                'Программирование', teacher_ids['Алексей Смирнов'], 5,
                'Экономика предприятия', teacher_ids['Ольга Кузнецова'], 4,
                'Высшая математика', teacher_ids['Виктор Павлов'], 6,
                'Квантовая физика', teacher_ids['Екатерина Иванова'], 5,
                'Алгоритмы и структуры данных', teacher_ids['Игорь Сидоров'], 5,
                'Микроэкономика', teacher_ids['Ольга Кузнецова'], 4,
                'Линейная алгебра', teacher_ids['Виктор Павлов'], 5,
            ))

            cur.execute("""
                INSERT INTO students (name, faculty_id, enrollment_year) VALUES
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s),
                (%s, %s, %s);
            """, (
                'Иван Иванов', faculty_ids['Факультет информатики'], 2021,
                'Мария Петрова', faculty_ids['Факультет экономики'], 2020,
                'Александр Смирнов', faculty_ids['Факультет информатики'], 2022,
                'Елена Козлова', faculty_ids['Факультет информатики'], 2023,
                'Дмитрий Васильев', faculty_ids['Факультет экономики'], 2021,
                'Ольга Морозова', faculty_ids['Факультет экономики'], 2022,
                'Сергей Волков', faculty_ids['Факультет информатики'], 2020,
                'Наталья Федорова', faculty_ids['Факультет информатики'], 2021,
                'Павел Никитин', faculty_ids['Факультет экономики'], 2023,
                'Анна Лебедева', faculty_ids['Факультет экономики'], 2023,
                'Константин Орлов', faculty_ids['Факультет математики'], 2022,
                'Татьяна Михайлова', faculty_ids['Факультет математики'], 2021,
                'Владимир Громов', faculty_ids['Факультет физики'], 2020,
                'Ирина Сергеева', faculty_ids['Факультет физики'], 2021,
                'Юрий Ковалёв', faculty_ids['Факультет информатики'], 2020,
                'Марина Лазарева', faculty_ids['Факультет экономики'], 2023,
            ))


            connection.commit()
            print("Данные успешно вставлены!")
        except Exception as e:
            print(f"Ошибка вставки данных: {e}")
            connection.rollback()
            raise
