import pymysql
from Student import Student
from Faculty import Faculty
from Exceptions import *


class DBHandler:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        try:
            self.__connection = pymysql.connect(host='localhost', user='root', password='Hira*1614', database='fcit')
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(str(e))

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()

    def select_student(self, sql):
        if self.__connection is not None:
            self.connect()
        students_list = []
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
            for row in data:
                stu = Student(row[4], '', '', row[0], row[1], float(row[2]), row[3])
                students_list.append(stu)
            return students_list
        except Exception as e:
            print(str(e))
            return None

    def select_faculty(self, sql):
        if self.__connection is not None:
            self.connect()
        faculty_list = []
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchall()
            for row in data:
                faculty = Faculty(row[3], '', '', row[0], row[1], row[2])
                faculty_list.append(faculty)
            return faculty_list
        except Exception as e:
            print(str(e))
            return None

    def register_student(self, student):
        if self.__connection is None:
            self.connect()
        try:
            stud_list = self.select_student("select * from student")
            for stu in stud_list:
                if student.student_id == stu.student_id:
                    raise InvalidStudent("Invalid Student ID")
            query = 'insert into user (username, password) values(%s,%s)'
            args = (student.username, student.password)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            query = 'select id from user where username = %s and password = %s'
            args = (student.username, student.password)
            self.__cursor.execute(query, args)
            data = self.__cursor.fetchall()
            s = data[0][0]
            query = 'insert into student (semester,Cgpa, Major, user_id) values(%s,%s,%s,%s)'
            args = (student.semester, student.cgpa, student.major, s)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except InvalidStudent as e:
            print(str(e))
            return False
        except Exception as e:
            print(str(e))
            return False

    def register_faculty(self, faculty):
        if self.__connection is None:
            self.connect()
        try:
            fac_list = self.select_faculty("select * from faculty")
            for f in fac_list:
                if faculty.faculty_id == f.faculty_id:
                    raise InvalidFaculty("Invalid faculty ID")
            query = 'insert into user (username, password) values(%s,%s)'
            args = (faculty.username, faculty.password)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            query = 'select id from user where username = %s and password = %s'
            args = (faculty.username, faculty.password)
            self.__cursor.execute(query, args)
            data = self.__cursor.fetchall()
            s = data[0][0]
            query = 'insert into faculty (designation, subject, user_id) values(%s,%s,%s)'
            args = (faculty.designation, faculty.subject, s)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except InvalidFaculty as e:
            print(str(e))
            return False
        except Exception as e:
            print(str(e))
            return False

    def get_student(self, username, password):
        if self.__connection is None:
            self.connect()
        try:
            query = 'select student.id, student.semester, student.Cgpa, student.Major from student, user where user.id = student.user_id and user.username = %s and user.password = %s'
            args = (username, password)
            self.__cursor.execute(query, args)
            data = self.__cursor.fetchall()
            for d in data:
                print("Student_Id = ", d[0])
                print("Student_Semester = ", d[1])
                print("Student_CGPA = ", d[2])
                print("Student_Major = ", d[3])
        except Exception as e:
            print(str(e))

    def get_faculty(self, username, password):
        if self.__connection is None:
            self.connect()
        try:
            query = 'select faculty.id, faculty.designation, faculty.subject from faculty, user where user.id = faculty.user_id and user.username = %s and user.password = %s'
            args = (username, password)
            self.__cursor.execute(query, args)
            data = self.__cursor.fetchall()
            for d in data:
                print("Faculty_Id= ", d[0])
                print("Faculty_Designation = ", d[1])
                print("Faculty_Subject = ", d[2])
        except Exception as e:
            print(str(e))

    def update_student(self, stu_obj):
        if self.__connection is None:
            self.connect()
        try:
            query = 'update student set semester = %s, Cgpa = %s, Major = %s where id = %s'
            args = (stu_obj.semester, stu_obj.cgpa, stu_obj.major, stu_obj.student_id)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            self.disconnect()

    def update_faculty(self, fac_obj):
        if self.__connection is None:
            self.connect()
        try:
            query = 'update faculty set designation = %s, subject = %s where id = %s'
            args = (fac_obj.designation, fac_obj.subject, fac_obj.faculty_id)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            self.disconnect()

    def delete_faculty(self, fac_id):
        if self.__connection is None:
            self.connect()
        try:
            query = 'delete from faculty where id = %s'
            args = (fac_id)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            self.disconnect()

    def delete_student(self, stu_id):
        if self.__connection is None:
            self.connect()
        try:
            query = 'delete from student where id = %s'
            args = (stu_id)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            self.disconnect()
