import pymysql
from contact import Contact
from Exceptions import *

class dB():
        def __init__(self, host, user, password, database):
            self.__host=host
            self.__user=user
            self.__password=password
            self.__databaseName=database
            self.__myConnection = None
            self.__myCursor = None
            try:
                self.__myConnection = pymysql.connect(host = self.__host, user = self.__user, password = self.__password, database = self.__databaseName)
                self.__myCursor = self.__myConnection.cursor()
            except Exception as e:
                print("Connection NOT Opened Succesfully")
                print(str(e))
        

        def find_contact_name(self, contactName):
            try:
                query = "SELECT name FROM contacts WHERE name = %s"
                args = (contactName)
                self.__myCursor.execute(query, args)
                result = self.__myCursor.fetchall()
                if len(result) == 0:
                    return True
                else:
                    raise DuplicateName
            except DuplicateName as e:
                return False
            except Exception as e:
                return False


        def store_contact(self, contact):
            try:
                query = "INSERT into contacts(Id, name, mobileno, city, profession) VALUES (%s, %s, %s, %s, %s)"
                args = (contact.id, contact.name, contact.mobileNo, contact.city, contact.profession)
                self.__myCursor.execute(query, args)
                self.__myConnection.commit()
            except Exception as e:
                 print(str(e))

            
        def show_contacts(self):
            try:
                query = "SELECT * FROM contacts"
                self.__myCursor.execute(query)
                result = self.__myCursor.fetchall()
                contactList = []
                for i in result:
                    contact = Contact(i[0], i[1], i[2], i[3], i[4])
                    contactList.append(contact)
                return contactList
            except Exception as e:
                 print(str(e))

        def search_contact(self, contactName: object) -> object:
            try:
                query = "SELECT * FROM contacts WHERE Name = %s"
                args = (contactName)
                self.__myCursor.execute(query, args)
                result = self.__myCursor.fetchall()
                if len(result) == 0:
                    return False
                else:
                    c = Contact(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
                    contact = [c]
                    return contact
            except Exception as e:
                 print(str(e))

        def close_connection(self):
            if self.__myCursor != None:
                self.__myCursor.close()
            if self.__myConnection != None:
                self.__myConnection.close()