from User import User


class Faculty(User):
    def __init__(self, user_id='', username='', password='', fid='', designation='', subject=''):
        super().__init__(user_id, username, password)
        self.faculty_id = fid
        self.designation = designation
        self.subject = subject

    def __str__(self):
        return f'Faculty_ID:{self.faculty_id}\n Designation:{self.designation} \n Subject:{self.subject}'
