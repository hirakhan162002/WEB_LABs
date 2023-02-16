#from resources import ProApi, ProductApi
from flask import request, Response, jsonify
from flask_restful import Resource
from database.model import Product
from mongoengine import Q


class ProductsApi(Resource):
    def get(self):
        prod = Product.objects.to_json()
        return Response(prod, mimetype="application/json", status=200)
    def post(self):
        body=request.get_json()
        prod = Product(name=body["name"],description=body["description"],price=body["price"]).save()
        id=prod.id
        return {'id':str(id)},200
    def put(self):
        body = request.get_json()
        prod = Product.objects.get(name=body["name"],description=body["description"]).update(**body)
        return {'status': 'Updated Successfully'}, 200
    def delete(self):
        body = request.get_json()
        Product.objects.get(name=body["name"],description=body["description"]).delete()
        return {'id': [str(id),'Deleted Successfully']}, 200

class ProductApiByName(Resource):
    def get(self,name):
        prod=Product.objects.get(name=name).to_json()
        return Response(prod,mimetype="application/json",status=200)
    def put(self,name):
        try:
            body=request.get_json()
            Product.objects.get(name=name).update(**body)
            return {'status':'Updated Successfully'}, 200
        except Exception as e:
            print(str(e))
            return 201
    def delete(self,name):
        Product.objects.get(name=name).delete()
        return {'id': [str(id),'Deleted Successfully']}, 200

class ProductApiByNameAndDescription(Resource):
    def get(self):
        name = request.get.args("name")
        description = request.get.args("description")
        prod = Product.objects(Q(name__containes = name) | Q(description__contains = description)).to_json()
        return Response

def initialize_routes(api):
    api.add_resource(ProductApiByName,'/api/prod/<name>')
    api.add_resource(ProductsApi,'/api/products')

