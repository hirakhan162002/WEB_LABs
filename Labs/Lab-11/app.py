from flask import Flask, jsonify,request, render_template
from flask_restful import Api,Resource
from database import db
from resource import routes


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    #'host':'mongodb://localhost:27017/test'
    'host': 'mongodb://localhost:27017/Hira'
}
api=Api(app)
db.initialize_db(app)
routes.initialize_routes(api)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/addVeh')
def addvehicleform():
    return render_template("AddVehicle.html")

@app.route('/showData')
def showData():
    return render_template("ShowData.html")

@app.route('/showContacts')
def showContacts():  # put application's code here
    return render_template("ShowContacts.html")

@app.route('/addContacts')
def addContacts():  # put application's code here
    return render_template("AddContact.html")


if __name__ == '__main__':
    app.run()
