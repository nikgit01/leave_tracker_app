from core.leave_logic import (
    add_student, update_student_email, view_leave_count, reset_leaves, mark_leave, delete_student
)

def menu():
    print("\n=== Leave Tracker ===")
    print("1) Add student")
    print("2) Update student email")
    print("3) View leave count")
    print("4) Reset leaves (student)")
    print("5) Mark leave")
    print("6) Delete Student Record")
    print("0) Exit")

def main():
    while True:
        menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            roll_no = int(input("Roll No: "))
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            subjects = input("Subjects (comma-separated, e.g., Math,Physics,Chemistry): ").replace(" ", "").split(",")
            add_student(roll_no, name, email, subjects)

        elif choice == "2":
            roll_no = int(input("Roll_noNo: "))
            email = input("New Email: ").strip()
            update_student_email(roll_no, email)

        elif choice == "3":
            roll_no = int(input("Roll_noNo: "))
            subject = input("Subject: ").strip().title()
            view_leave_count(roll_no, subject)
        
        elif choice == "4":
            roll_no = int(input("Roll_noNo: "))
            reset_leaves(roll_no)

        elif choice == "5":
            roll_no = int(input("Roll_noNo: "))
            subject = input("Subject: ").strip().title()
            mark_leave(roll_no, subject)

        elif choice == "6":
            roll_no = int(input("Roll No: "))
            delete_student(roll_no)

        elif choice == "0":
            print("bye!")
            break
        else:
            print("invalid choice")


main()