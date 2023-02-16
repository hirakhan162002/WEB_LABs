from User import User


class Student(User):
    def __init__(self, user_id='', username='', password='', stu_id='', semester='', cgpa=0.0, major=''):
        super().__init__(user_id, username, password)
        self.student_id = stu_id
        self.semester = semester
        self.cgpa = cgpa
        self.major = major

    def __str__(self):
        return f'Student_ID:{self.student_id}\n Semester:{self.semester} \n CGPA:{self.cgpa} \n Major:{self.major}'
