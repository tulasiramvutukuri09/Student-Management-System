
import json
import os


class StudentManagement:
    def __init__(self):
        self.students_file = "students.json"
        self.subjects_file = "subjects.json"
        self.students = []
        self.subjects = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.students_file):
            with open(self.students_file, "r") as file:
                self.students = json.load(file)

        if os.path.exists(self.subjects_file):
            with open(self.subjects_file, "r") as file:
                self.subjects = json.load(file)

    def save_students(self):
        with open(self.students_file, "w") as file:
            json.dump(self.students, file, indent=4)

    def save_subjects(self):
        with open(self.subjects_file, "w") as file:
            json.dump(self.subjects, file, indent=4)

    def get_branch(self):
        branches = ["CSE", "ECE", "EEE", "IT", "MECH", "CIVIL", "AI&DS"]

        print("\nAvailable branches:")
        for branch in branches:
            print("-", branch)

        branch = input("Enter branch: ").strip().upper()

        if branch not in branches:
            print("Invalid branch.")
            return None

        return branch

    def get_student(self, student_id):
        for student in self.students:
            if student["student_id"] == student_id:
                return student
        return None

    def get_semester_registration(self, student, semester):
        for registration in student["registrations"]:
            if registration["semester"] == semester:
                return registration
        return None

    # ADMIN FUNCTIONS

    def add_student(self):
        print("\n--- Register Student ---")

        student_id = input("Enter 5-digit student ID: ").strip()

        if len(student_id) != 5 or not student_id.isdigit():
            print("ID must contain exactly 5 digits.")
            return

        if self.get_student(student_id) is not None:
            print("Student ID already exists.")
            return

        name = input("Enter student name: ").strip()

        if name == "":
            print("Name cannot be empty.")
            return

        year = input("Enter year (1-4): ").strip()

        if year not in ["1", "2", "3", "4"]:
            print("Invalid year.")
            return

        semester = input("Enter semester (1-8): ").strip()

        if semester not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Invalid semester.")
            return

        if int(semester) not in [int(year) * 2 - 1, int(year) * 2]:
            print("Semester does not match the year.")
            return

        cgpa_text = input("Enter CGPA (0-10): ").strip()

        try:
            cgpa = float(cgpa_text)
        except ValueError:
            print("Enter a valid CGPA.")
            return

        if cgpa < 0 or cgpa > 10:
            print("CGPA must be between 0 and 10.")
            return

        branch = self.get_branch()

        if branch is None:
            return

        student = {
            "student_id": student_id,
            "name": name,
            "year": int(year),
            "semester": int(semester),
            "cgpa": cgpa,
            "branch": branch,
            "registrations": []
        }

        self.students.append(student)
        self.save_students()
        print("Student registered successfully.")

    def add_subject(self):
        print("\n--- Add Subject ---")

        name = input("Enter subject name: ").strip()

        if name == "":
            print("Subject name cannot be empty.")
            return

        branch = self.get_branch()

        if branch is None:
            return

        print("\nEnter eligible years separated by commas.")
        print("Example: 2,3,4")

        years_text = input("Eligible years (1-4): ").strip()
        years = []

        for item in years_text.split(","):
            item = item.strip()

            if item not in ["1", "2", "3", "4"]:
                print("Invalid year.")
                return

            if int(item) not in years:
                years.append(int(item))

        if len(years) == 0:
            print("Select at least one eligible year.")
            return

        for subject in self.subjects:
            if (subject["name"].lower() == name.lower()
                    and subject["branch"] == branch):
                print("This subject already exists for this branch.")
                return

        subject = {
            "subject_id": str(len(self.subjects) + 1).zfill(4),
            "name": name,
            "branch": branch,
            "credits": 3,
            "eligible_years": years
        }

        self.subjects.append(subject)
        self.save_subjects()

        print("Subject added successfully.")
        print("Credits assigned automatically: 3")

    def view_subjects(self):
        if len(self.subjects) == 0:
            print("No subjects available.")
            return

        for subject in self.subjects:
            print("\n----------------------")
            print("Subject ID:", subject["subject_id"])
            print("Name:", subject["name"])
            print("Branch:", subject["branch"])
            print("Credits:", subject["credits"])
            print("Eligible years:", subject["eligible_years"])

    def display_student_details(self, student):
        print("\n----------------------")
        print("Student ID:", student["student_id"])
        print("Name:", student["name"])
        print("Year:", student["year"])
        print("Semester:", student["semester"])
        print("Branch:", student["branch"])
        print("CGPA:", student["cgpa"])

        current = self.get_semester_registration(
            student, student["semester"]
        )

        current_count = 0
        current_credits = 0

        if current is not None:
            current_count = len(current["subjects"])
            current_credits = current["credits"]

            print("\nCurrent semester subjects:")
            for subject in current["subjects"]:
                print("-", subject["name"], "|", subject["credits"], "credits")

        total_count = 0
        total_credits = 0

        for registration in student["registrations"]:
            total_count += len(registration["subjects"])
            total_credits += registration["credits"]

        print("\nSubjects this semester:", current_count)
        print("Credits this semester:", current_credits)
        print("Total subjects across semesters:", total_count)
        print("Total credits across semesters:", total_credits)
        print("----------------------")

    def view_all_students(self):
        if len(self.students) == 0:
            print("No students registered.")
            return

        for student in self.students:
            self.display_student_details(student)

    def search_student(self):
        student_id = input("Enter student ID: ").strip()
        student = self.get_student(student_id)

        if student is None:
            print("Student not found.")
            return

        self.display_student_details(student)

    # STUDENT FUNCTIONS

    def register_subjects(self):
        student_id = input("Enter your 5-digit student ID: ").strip()
        student = self.get_student(student_id)

        if student is None:
            print("Student not found. Contact the admin.")
            return

        year = student["year"]
        branch = student["branch"]
        semester = student["semester"]

        existing = self.get_semester_registration(student, semester)
        selected = []

        if existing is not None:
            for subject in existing["subjects"]:
                selected.append(subject.copy())

        total_credits = 0

        for subject in selected:
            total_credits += subject["credits"]

        while True:
            available = []

            for subject in self.subjects:
                if (subject["branch"] == branch
                        and year in subject["eligible_years"]):

                    already_selected = False

                    for item in selected:
                        if item["subject_id"] == subject["subject_id"]:
                            already_selected = True

                    if not already_selected:
                        available.append(subject)

            print("\nStudent:", student["name"])
            print("Branch:", branch)
            print("Year:", year)
            print("Semester:", semester)
            print("Selected credits:", total_credits)
            print("Required credits: 15 to 27")

            if len(available) == 0:
                print("No more eligible subjects available.")
                break

            for i in range(len(available)):
                subject = available[i]
                print(
                    i + 1, ".", subject["name"],
                    "-", subject["credits"], "credits"
                )

            print("0. Save and exit")

            choice = input("Choose a subject: ").strip()

            if choice == "0":
                break

            if not choice.isdigit():
                print("Enter a valid number.")
                continue

            number = int(choice)

            if number < 1 or number > len(available):
                print("Invalid choice.")
                continue

            subject = available[number - 1]

            if total_credits + subject["credits"] > 27:
                print("Cannot exceed 27 credits.")
                continue

            selected.append({
                "subject_id": subject["subject_id"],
                "name": subject["name"],
                "credits": subject["credits"]
            })

            total_credits += subject["credits"]
            print("Subject selected.")

        if len(selected) > 0:
            if existing is not None:
                student["registrations"].remove(existing)

            if 15 <= total_credits <= 27:
                status = "Complete"
            else:
                status = "Draft"

            registration = {
                "semester": semester,
                "subjects": selected,
                "credits": total_credits,
                "status": status
            }

            student["registrations"].append(registration)
            self.save_students()

        print("\nRegistration saved.")
        print("Total selected credits:", total_credits)

        if 15 <= total_credits <= 27:
            print("Status: Complete")
        else:
            print("Status: Draft. You can continue later.")

    def view_my_details(self):
        student_id = input("Enter your 5-digit student ID: ").strip()
        student = self.get_student(student_id)

        if student is None:
            print("Student not found.")
            return

        self.display_student_details(student)
