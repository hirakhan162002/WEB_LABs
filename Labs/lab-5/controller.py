from db import dB

class ContactController():

    def validate_contact_name(self, contactName):
        dbObj = dB("localhost", "root", "Hira*1614", "test")
        status = dbObj.find_contact_name(contactName)
        dbObj.close_connection()
        if status:
            return True
        else:
            return False
    

