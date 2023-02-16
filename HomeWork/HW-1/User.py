class User:
    def __init__(self, user_id='', username='', password=''):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __str__(self):
        return f'User_ID:{self.user_id}\n User_Name:{self.username} \n Password:{self.password}'
