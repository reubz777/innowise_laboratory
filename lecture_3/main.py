class StudentGradeAnalyzer:
    def __init__(self):
        self.students = []

    def display_menu(self):
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Show report (all students)")
        print("4. Find top performer")
        print("5. Exit")

    def add_new_student(self):
        name = input("Enter student name: ").strip()

        for student in self.students:
            if student["name"].lower() == name.lower():
                print(f"Student '{name}' already exists")
                return

        new_student = {"name": name, "grades": []}
        self.students.append(new_student)
        print(f"Student '{name}' added successfully")

    def add_grades_for_student(self):
        name = input("Enter student name: ").strip()

        student_found = None
        for student in self.students:
            if student["name"].lower() == name.lower():
                student_found = student
                break

        if not student_found:
            print(f"Student '{name}' not found")
            return

        print(f"Adding grades for {student_found['name']}:")
        while True:
            grade_input = input("Enter a grade (or 'done' to finish): ").strip()

            if grade_input.lower() == "done":
                break

            try:
                grade = int(grade_input)
                if grade < 0 or grade > 100:
                    print("Grade must be between 0 and 100")
                    continue

                student_found["grades"].append(grade)
                print(f"Grade {grade} added successfully")

            except ValueError:
                print("Invalid input. Please enter a number between 0 and 100.")

    def show_report(self):
        if not self.students:
            print("No students added yet")
            return

        print("\n--- Student Report ---")

        averages = []
        valid_averages = []

        for student in self.students:
            try:
                if not student["grades"]:
                    print(f"{student['name']}'s average grade is N/A.")
                    averages.append(None)
                else:
                    average = sum(student["grades"]) / len(student["grades"])
                    averages.append(average)
                    valid_averages.append(average)
                    print(f"{student['name']}'s average grade is {average:.1f}.")

            except ZeroDivisionError:
                print(f"{student['name']}'s average grade is N/A.")
                averages.append(None)

        if valid_averages:
            max_avg = max(valid_averages)
            min_avg = min(valid_averages)
            overall_avg = sum(valid_averages) / len(valid_averages)

            print("---")
            print(f"Max Average: {max_avg:.1f}")
            print(f"Min Average: {min_avg:.1f}")
            print(f"Overall Average: {overall_avg:.1f}")
        else:
            print("---")
            print("No grades available for summary statistics.")

    def find_top_performer(self):
        if not self.students:
            print("No students added yet")
            return

        students_with_grades = []
        for student in self.students:
            if student["grades"]:
                try:
                    average = sum(student["grades"]) / len(student["grades"])
                    students_with_grades.append((student, average))
                except ZeroDivisionError:
                    continue

        if not students_with_grades:
            print("No students with grades available")
            return

        top_student, top_average = max(students_with_grades, key=lambda x: x[1])

        print(
            f"The student with the highest average is {top_student['name']} with a grade of {top_average:.1f}."
        )

    def run(self):
        print("Welcome to Student Grade Analyzer")

        while True:
            self.display_menu()

            try:
                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.add_new_student()
                elif choice == "2":
                    self.add_grades_for_student()
                elif choice == "3":
                    self.show_report()
                elif choice == "4":
                    self.find_top_performer()
                elif choice == "5":
                    print("Exiting program. Goodbye")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1-5.")

            except KeyboardInterrupt:
                print("\n\nProgram interrupted. Exiting...")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    analyzer = StudentGradeAnalyzer()
    analyzer.run()
