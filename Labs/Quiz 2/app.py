from flask import Flask, request, render_template
from user import User
from DBHandler import UserModel
app = Flask(__name__)


@app.route('/')
def registration():
    return render_template("Register.html")


@app.route('/register', methods=["POST"])
def reg_info():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    u = User(name, email, password)
    db_handler = UserModel("localhost", "root", "Hira*1614", "store")
    status = db_handler.insert_user(u)
    if status:
        return render_template("login.html")
    else:
        return render_template("Register.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    u = User('', email, password)
    db_handler = UserModel("localhost", "root", "Hira*1614", "store")
    status = db_handler.login(u)
    if status:
        return render_template("Dashboard.html")
    else:
        return render_template("login.html", msg="Login Failed")


if __name__ == '__main__':
    app.run()
