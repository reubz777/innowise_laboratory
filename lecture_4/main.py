import os
import sqlite3


def create_database():
    if os.path.exists("school.db"):
        os.remove("school.db")

    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    with open("school_queries.sql", "r") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()

    print("Database created successfully")
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
    for name, avg in cursor.fetchall():
        print(f"  {name}: {avg}")

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
