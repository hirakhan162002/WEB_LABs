from resources import  StuApi ,StudentApi
#VehiclesApi,Test,VehicleApi ,ContactsAPI,ContactCRUDAPI, searchContact
def initialize_routes(api):
    #api.add_resource(ProApi, '/api/pro/<id>')
    #api.add_resource(ProductApi, '/api/product')
    api.add_resource(StuApi, '/api/stu/<id>')
    api.add_resource(StudentApi,'/api/student')
    #api.add_resource(VehiclesApi, '/api/buses')
    #api.add_resource(Test, "/api/test")
    #api.add_resource(VehicleApi, "/api/bus/<id>")
    #api.add_resource(ContactsAPI, "/api/contacts")
    #api.add_resource(ContactCRUDAPI,"/api/contacts/<id>")
    #api.add_resource(searchContact,"/api/searchcontacts/<name>")
    #api.add_resource(Hello, '/api/')
    #api.add_resource(Square, '/square/<int:num>')