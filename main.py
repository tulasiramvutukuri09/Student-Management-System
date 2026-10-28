
from student import StudentManagement


def admin_menu(system):
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Register student")
        print("2. View all student details")
        print("3. Search student")
        print("4. Add subject")
        print("5. View all subjects")
        print("6. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            system.add_student()
        elif choice == "2":
            system.view_all_students()
        elif choice == "3":
            system.search_student()
        elif choice == "4":
            system.add_subject()
        elif choice == "5":
            system.view_subjects()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def student_menu(system):
    while True:
        print("\n===== STUDENT MENU =====")
        print("1. Register subjects")
        print("2. View my details")
        print("3. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            system.register_subjects()
        elif choice == "2":
            system.view_my_details()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def main():
    system = StudentManagement()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Admin")
        print("2. Student")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_menu(system)
        elif choice == "2":
            student_menu(system)
        elif choice == "3":
            print("Thank you for using the system.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
