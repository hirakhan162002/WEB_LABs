from flask import request, Response, jsonify
from flask_restful import Resource
from database.model import Vehicle, Contacts, Student

class StudentApi(Resource):
    def get(self):
        stud=Student.objects().to_json()
        return Response(stud, mimetype="application/json", status=200)
    def post(self):
        body=request.get_json()
        #veh=Vehicle(**body).save()
        veh = Student(name=body["name"],rollno=body["rollno"],cgpa=body["cgpa"]).save()
        id=veh.id
        return {'id':str(id)},200

class VehiclesApi(Resource):
    def get(self):
        buses=Vehicle.objects().to_json()
        return Response(buses, mimetype="application/json", status=200)
    def post(self):
        body=request.get_json()
        #veh=Vehicle(**body).save()
        veh = Vehicle(reg=body["reg"],model=body["model"]).save()
        id=veh.id
        return {'id':str(id)},200

class VehicleApi(Resource):
    def get(self,id):
        veh=Vehicle.objects.get(id=id).to_json()
        return Response(veh,mimetype="application/json",status=200)
    def put(self,id):
        body=request.get_json()
        Vehicle.objects.get(id=id).update(**body)
        return {'id':str(id)},200
    def delete(self,id):
        Vehicle.objects.get(id=id).delete()


class Test(Resource):
    def get(self):
        return jsonify({"msg":"Hello World"})

    def post(self):
        data = request.get_json()  # status code
        print(data)
        data.update(name="Sanam")
        data.update(magic=78952369841)
        data.update(sep="operator")
        return data, 201



class ContactsAPI(Resource):
    def get(self):
        contacts = Contacts.objects()
        return Response(contacts.to_json(), mimetype="application/json", status=200)


    def post(self):
        reqdata = request.get_json()
        contact = Contacts(**reqdata).save()
        return {"id":str(contact.id)} , 200

class ContactCRUDAPI(Resource):
    def get(self,id):
        contact=Contacts.objects.get(id=id)
        return Response(contact.to_json(), mimetype="application/json", status=200)

    def put(self,id):
        reqdata=request.get_json()
        Contacts.objects.get(id=id).update(**reqdata)
        return {'id': str(id)}, 200

    def delete(self,id):
        Contacts.objects.get(id=id).delete()
        return {'id': str(id),'delete':'done'}, 200

class searchContact(Resource):
      def get(self,name):
          contact=Contacts.objects.get(name=name)
          return Response(contact.to_json(), mimetype="application/json", status=200)

class StuApi(Resource):
    def get(self,id):
        veh=Student.objects.get(id=id).to_json()
        return Response(veh,mimetype="application/json",status=200)
    def put(self,id):
        body=request.get_json()
        Student.objects.get(id=id).update(**body)
        return {'id':str(id)},200
    def delete(self,id):
        Student.objects.get(id=id).delete()