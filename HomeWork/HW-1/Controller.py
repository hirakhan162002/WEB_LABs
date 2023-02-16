
from Model import DBHandler


class ControllerClass:

    def register_student(self, student):
        db_handler = DBHandler()
        status = db_handler.register_student(student)
        return status

    def register_faculty(self, faculty):
        db_handler = DBHandler()
        status = db_handler.register_faculty(faculty)
        return status

    def authenticate_faculty(self, username, password):
        db_handler = DBHandler()
        db_handler.get_faculty(username, password)

    def authenticate_student(self, username, password):
        db_handler = DBHandler()
        db_handler.get_student(username, password)

    def update_student(self, student):
        db_handler = DBHandler()
        status = db_handler.update_student(student)
        return status

    def update_faculty(self, faculty):
        db_handler = DBHandler()
        status = db_handler.update_faculty(faculty)
        return status

    def delete_student(self, user_id):
        db_handler = DBHandler()
        status = db_handler.delete_student(user_id)
        return status

    def delete_faculty(self, user_id):
        db_handler = DBHandler()
        status = db_handler.delete_faculty(user_id)
        return status
