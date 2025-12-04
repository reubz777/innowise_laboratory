import os
import sqlite3


def create_database():
    if os.path.exists("school.db"):
        os.remove("school.db")

    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_year INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            grade INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    students = [
        ("Alice Johnson", 2005),
        ("Brian Smith", 2004),
        ("Carla Reyes", 2006),
        ("Daniel Kim", 2005),
        ("Eva Thompson", 2003),
        ("Felix Nguyen", 2007),
        ("Grace Patel", 2005),
        ("Henry Lopez", 2004),
        ("Isabella Martinez", 2006),
    ]

    cursor.executemany(
        "INSERT INTO students (full_name, birth_year) VALUES (?, ?)", students
    )

    grades = [
        (1, "Math", 88),
        (1, "English", 92),
        (1, "Science", 85),
        (2, "Math", 75),
        (2, "History", 83),
        (2, "English", 79),
        (3, "Science", 95),
        (3, "Math", 91),
        (3, "Art", 89),
        (4, "Math", 84),
        (4, "Science", 88),
        (4, "Physical Education", 93),
        (5, "English", 90),
        (5, "History", 85),
        (5, "Math", 88),
        (6, "Science", 72),
        (6, "Math", 78),
        (6, "English", 81),
        (7, "Art", 94),
        (7, "Science", 87),
        (7, "Math", 90),
        (8, "History", 77),
        (8, "Math", 83),
        (8, "Science", 80),
        (9, "English", 96),
        (9, "Math", 89),
        (9, "Art", 92),
    ]

    cursor.executemany(
        "INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", grades
    )

    cursor.execute("CREATE INDEX idx_students_name ON students(full_name)")
    cursor.execute("CREATE INDEX idx_students_year ON students(birth_year)")
    cursor.execute("CREATE INDEX idx_grades_student ON grades(student_id)")
    cursor.execute("CREATE INDEX idx_grades_subject ON grades(subject)")
    cursor.execute("CREATE INDEX idx_grades_grade ON grades(grade)")

    conn.commit()

    print("  Database created successfully")
    print()
    conn.close()


def show_results():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    print("1. All grades for Alice Johnson:")
    cursor.execute("""
        SELECT subject, grade
        FROM grades
        WHERE student_id = (SELECT id FROM students WHERE full_name = 'Alice Johnson')
        ORDER BY subject
    """)
    for subject, grade in cursor.fetchall():
        print(f"  {subject}: {grade}")

    print("\n2. Average grade per student:")
    cursor.execute("""
        SELECT s.full_name, ROUND(AVG(g.grade), 2)
        FROM students s
        JOIN grades g ON s.id = g.student_id
        GROUP BY s.id, s.full_name
        ORDER BY AVG(g.grade) DESC
    """)
    for name, avg in cursor.fetchall():
        print(f"  {name}: {avg}")

    print("\n3. Students born after 2004:")
    cursor.execute("""
        SELECT full_name, birth_year
        FROM students
        WHERE birth_year > 2004
        ORDER BY birth_year
    """)
    for name, year in cursor.fetchall():
        print(f"  {name} (born {year})")

    print("\n4. Subjects and their average grades:")
    cursor.execute("""
        SELECT subject, ROUND(AVG(grade), 2)
        FROM grades
        GROUP BY subject
        ORDER BY AVG(grade) DESC
    """)
    for subject, avg in cursor.fetchall():
        print(f"  {subject}: {avg}")

    print("\n5. Top 3 students with highest average grades:")
    cursor.execute("""
        SELECT s.full_name, ROUND(AVG(g.grade), 2)
        FROM students s
        JOIN grades g ON s.id = g.student_id
        GROUP BY s.id, s.full_name
        ORDER BY AVG(g.grade) DESC
        LIMIT 3
    """)
    for i, (name, avg) in enumerate(cursor.fetchall(), 1):
        print(f"  {i}. {name}: {avg}")

    print("\n6. Students who scored below 80 in any subject:")
    cursor.execute("""
        SELECT DISTINCT s.full_name, g.subject, g.grade
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE g.grade < 80
        ORDER BY s.full_name, g.grade
    """)
    results = cursor.fetchall()
    if results:
        for name, subject, grade in results:
            print(f"  {name}: {subject} - {grade}")
    else:
        print("  No students with grades below 80")

    conn.close()


def main():
    create_database()
    show_results()


if __name__ == "__main__":
    main()
