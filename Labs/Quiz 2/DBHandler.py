import pymysql


class UserModel:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def insert_user(self, user):
        mydb = None
        try:
            mydb = pymysql.Connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mycursor = mydb.cursor()
            sql = "insert into users (uname, uemail, upassword) values (%s, %s, %s)"
            argu = (user.uname, user.u_email, user.u_password)
            mycursor. execute(sql, argu)
            mydb.commit()
            return True
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()

    def login(self, user):
        status = self.check_user(user.u_email)
        return status

    def check_user(self, u_email):
        mydb = None
        status = False
        try:
            mydb = pymysql.Connect(host=self.host, user=self.user, password=self.password, database=self.database)
            mycursor = mydb.cursor()
            sql = "select upassword from users where uemail = %s"
            mycursor.execute(sql)
            m = mycursor.fetchall()
            for i in m:
                if u_email == i[0]:
                    status = True
                    print(i[0])
        except Exception as e:
            print(str(e))
            return False
        finally:
            if mydb != None:
                mydb.close()
            return status
