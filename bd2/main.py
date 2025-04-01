import sqlite3

connection = sqlite3.connect('bz.bd')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS `students` (
	`student_id` integer primary key NOT NULL UNIQUE,
	`level_id` INTEGER NOT NULL,
	`direction_id` INTEGER NOT NULL,
	`type_id` INTEGER NOT NULL,
	`surname` TEXT NOT NULL,
	`name` TEXT NOT NULL,
	`patronymic` TEXT NOT NULL,
	`average_score` FLOAT NOT NULL
); """)

cursor.execute("""CREATE TABLE IF NOT EXISTS `levels` (
	`level_id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
FOREIGN KEY(`level_id`) REFERENCES `students`(`level_id`)
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS `directions` (
	`direction_id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
FOREIGN KEY(`direction_id`) REFERENCES `students`(`direction_id`)
); """)


cursor.execute(""" CREATE TABLE IF NOT EXISTS `types` (
	`type_id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
FOREIGN KEY(`type_id`) REFERENCES `students`(`type_id`)
);""")

for s in open('students.txt','r', encoding='utf-8'):
    data = s.strip().split()
    cursor.execute('''INSERT OR IGNORE INTO students (student_id, level_id, direction_id, type_id,
     surname, name, patronymic, average_score) VALUES(?,?,?,?,?,?,?,?)''',( int(data[0]), int(data[1]), int(data[2]), int(data[3]), data[4], data[5],
    data[6], float(data[7])))
connection.commit()

for s in open('levels.txt','r', encoding='utf-8'):
    data = s.strip().split()
    cursor.execute('''INSERT OR IGNORE INTO levels (level_id, name) VALUES(?,?)''', (int(data[0]), data[1]))
connection.commit()

for s in open('directions.txt', 'r', encoding='utf-8'):
    data = s.strip().split()
    cursor.execute('''INSERT OR IGNORE INTO directions (direction_id, name) VALUES(?,?) ''', (int(data[0]), data[1]))
connection.commit()

for s in open('types.txt','r', encoding='utf-8'):
    data = s.strip().split()
    cursor.execute('INSERT OR IGNORE INTO types (type_id, name) VALUES(?,?)',(int(data[0]), data[1]))
     
cursor.execute('SELECT COUNT(*) as total_students FROM students')
res = cursor.fetchone()
print(f"Кол-во студентов: {res[0]}")


cursor.execute("""
    SELECT d.name AS direction, COUNT(s.student_id) AS student_count
    FROM directions d
    LEFT JOIN students s ON d.direction_id = s.direction_id
    GROUP BY d.name
    ORDER BY student_count DESC;
""")

print("Количество студентов по направлениям:")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")
    

cursor.execute("""
    SELECT t.name AS study_type, COUNT(s.student_id) AS student_count
    FROM types t
    LEFT JOIN students s ON t.type_id = s.type_id
    GROUP BY t.name
    ORDER BY student_count DESC;
""")
print("\nКоличество студентов по формам обучения:")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")
    
cursor.execute("""
    SELECT 
        d.name AS direction,
        MAX(s.average_score) AS max_score,
        MIN(s.average_score) AS min_score,
        AVG(s.average_score) AS avg_score
    FROM directions d
    LEFT JOIN students s ON d.direction_id = s.direction_id
    GROUP BY d.name
    ORDER BY d.name;
""")

print("\nСтатистика баллов по направлениям:")
for row in cursor.fetchall():
    print(f"{row[0]}: Макс={row[1]:.2f}, Мин={row[2]:.2f}, Средн={row[3]:.2f}")
    
cursor.execute("""
    SELECT l.name, AVG(s.average_score)
    FROM students s JOIN levels l ON s.level_id = l.level_id
    GROUP BY l.name ORDER BY AVG(s.average_score) DESC
""")
print("\nСредний балл по уровням обучения: ")
for row in cursor.fetchall():
    print(f"{row[0]}: cредний балл={row[1]:.2f}")
    
cursor.execute("""
    SELECT t.name, AVG(s.average_score), COUNT(s.student_id)
    FROM students s JOIN types t ON s.type_id = t.type_id
    GROUP BY t.name ORDER BY AVG(s.average_score) DESC
""")
print("\nСредний балл по формам обучения: ")
for row in cursor.fetchall():
    print(f"{row[0]}: cредний балл={row[1]:.2f}")
    
cursor.execute("""
    SELECT s.student_id, s.surname, s.name, s.patronymic, s.average_score
    FROM students s
    JOIN directions d ON s.direction_id = d.direction_id
    JOIN types t ON s.type_id = t.type_id
    WHERE d.name = 'Информатика' AND t.name = 'Очная'
    ORDER BY s.average_score DESC
    LIMIT 5
""")
print("\n5 отобранных студентов для повышенной стипендии на направлении Информатика очной формы обучения: ")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Фамилия: {row[1]}, Имя: {row[2]}, Отчество: {row[3]}, Средний балл: {row[4]}")

cursor.execute("""
    SELECT SUM(count) as total_namesakes
    FROM (
        SELECT COUNT(*) as count
        FROM students
        GROUP BY surname
        HAVING COUNT(*) > 1
    ) AS same_surnames
""")
red = cursor.fetchone()
print(f"\nКол-во однофамильцев: {red[0]}")

cursor.execute("""
        SELECT surname, name, patronymic, COUNT(*) as count
        FROM students
        GROUP BY surname, name, patronymic
        HAVING COUNT(*) > 1
        ORDER BY count DESC
    """)
    
results = cursor.fetchall()
if results:
    print("\nПолные тезки: ")
    for row in results:
        print(f"Фамилия: {row[0]}, Имя: {row[1]}, Отчество: {row[2]}, Кол-во тезок: {row[3]}")
else:
    print("\nПолных тезок в группе нет")
connection.close()
