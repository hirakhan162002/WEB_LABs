
from Utils import print_header
from Student import Student
from Controller import ControllerClass
from Faculty import Faculty


def register_student():
    user_name = input("Enter your user name = ")
    password = input("Enter your password = ")
    semester = input("Enter your semester = ")
    if semester >= '0':
        semester = input("Again Enter your semester = ")
    elif semester >= '8':
        semester = input(" Again Enter your semester = ")
    cgpa = float(input("Enter your cgpa = "))
    if cgpa > 4.0:
        cgpa = float(input("Again Enter your cgpa = "))
    major = input("Enter your major = ")
    data = Student('', user_name, password, '', semester, cgpa, major)
    return data


def registration_student_status(status):
    if status is True:
        print("Registration Successfully")
    else:
        print("Registration fail")


def register_faculty():
    user_name = input("Enter your user name = ")
    password = input("Enter your password = ")
    designation = input("Enter your designation = ")
    subject = input("Enter your subject = ")
    data = Faculty('', user_name, password, '', designation, subject)
    return data


def registration_faculty_status(status):
    if status is True:
        print("Registration Successfully")
    else:
        print("Registration fail")


def update_student():
    id_ = input("Enter your id = ")
    semester = input("Enter your new semester = ")
    if semester >= '0':
        semester = input("Again Enter your semester = ")
    elif semester >= '8':
        semester = input(" Again Enter your semester = ")
    cgpa = float(input("Enter your cgpa = "))
    if cgpa > 4.0:
        cgpa = float(input("Again Enter your cgpa = "))
    major = input("Enter your new major detail = ")
    stu = Student('', '', '', id_, semester, cgpa, major)
    return stu


def update_faculty():
    id_ = input("Enter your id = ")
    designation = input("Enter your  new designation = ")
    subject = input("Enter your new subject = ")
    data = Faculty('', '', '', id_, designation, subject)
    return data


def main():
    print_header('Welcome to Student Management System')
    print('1. Register as student')
    print('2. Register as faculty')
    print('3. Authenticate as faculty')
    print('4. Authenticate as student')
    print('5. update as student')
    print('6. update as faculty')
    print('7. Delete student')
    print('8. Delete Faculty')
    print('9. Exit')
    print("-" * 40)
    student = ControllerClass()
    stu = Student()
    faculty = ControllerClass()
    f = Faculty()
    choice = 1
    while True:
        try:
            choice = int(input('Enter your choice: '))
            if choice == 1:
                stu = register_student()
                status = student.register_student(stu)
                registration_student_status(status)
            elif choice == 2:
                f = register_faculty()
                status = faculty.register_faculty(f)
                registration_faculty_status(status)
            elif choice == 3:
                user_name = input("Enter your user name = ")
                password = input("Enter your password = ")
                faculty.authenticate_faculty(user_name, password)
            elif choice == 4:
                user_name = input("Enter your user name = ")
                password = input("Enter your password = ")
                student.authenticate_student(user_name, password)
            elif choice == 5:
                stu = update_student()
                status = student.update_student(stu)
                if status:
                    print("Done changes")
                else:
                    print("Error")
            elif choice == 6:
                f = update_faculty()
                status = faculty.update_faculty(f)
                if status:
                    print("Done changes")
                else:
                    print("Error")
            elif choice == 7:
                user_id = input("Enter your id = ")
                status = student.delete_student(user_id)
                if status:
                    print("Done changes")
                else:
                    print("Error")
            elif choice == 8:
                user_id = input("Enter your id = ")
                status = faculty.delete_faculty(user_id)
                if status:
                    print("Done changes")
                else:
                    print("Error")
            elif choice == 9:
                print("Thank You for using our system")
                break
            else:
                raise ValueError('Invalid choice')
        except ValueError as e:
            print('Invalid choice: ' + str(str(e)))
            continue


# call to main function
if __name__ == '__main__':
    main()


