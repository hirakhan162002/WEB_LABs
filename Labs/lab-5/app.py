from flask import Flask, render_template, request
from contact import Contact
from db import dB
from controller import ContactController

app = Flask(__name__)

@app.route('/contact_form')
def display_contact_form():
    return render_template("create_contact.html")

@app.route('/save_data', methods = ["POST"])
def save_date():
    id = request.form["id"]
    name = request.form["name"]
    mobileNo = request.form["mobileNo"]
    city = request.form["city"]
    profession = request.form["profession"]
    contact = Contact(id, name, mobileNo, city, profession)
    controller = ContactController()
    status = controller.validate_contact_name(contact.name)
    if status:
        dbObj = dB("localhost", "root", "Hira*1614", "test")
        dbObj.store_contact(contact)
        dbObj.close_connection()
        return render_template("create_contact.html", message1 = "The Contact is stored successfully")
    else:
        return render_template("create_contact.html", message2 = "The Contact Name already Exist. Enter another name")


@app.route('/show_contacts')
def show_contacts():
    dbObj = dB("localhost", "root", "Hira*1614", "test")
    contactList = dbObj.show_contacts()
    dbObj.close_connection()
    return render_template("show_contact.html", contacts = contactList)


@app.route('/search_form')
def search_form():
    return render_template("search_contact.html")

@app.route('/search_contact', methods = ["POST"])
def search_contact():
    dbObj = dB("localhost", "root", "Hira*1614", "test")
    name = request.form["name"]
    contact = dbObj.search_contact(name)
    print(contact)
    dbObj.close_connection()
    if not(contact):
        return render_template("search_contact.html", message = "Invalid Contact Name")
    else:
        return render_template("search_contact.html", contactData = contact)



app.run()