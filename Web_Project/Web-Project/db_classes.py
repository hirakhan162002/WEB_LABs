class User:
    """user class"""
    def __init__(self,name='',email='',password=''):
        self.name=name
        self.email=email
        self.password=password

class Customer(User):
    """customer class"""
    def __init__(self,name='',email='',password='',phone = '', address = '',
                 city = '', province = '', zipCode = '', orderCount = 1):
        User.__init__(self,name,email,password)
        self.phone = phone
        self.address = address
        self.city = city
        self.province = province
        self.zipCode = zipCode
        self.orderCount = orderCount
    def __str__(self):
        return f"Name: {self.name}\nEmail: {self.email}\nPhone: {self.phone}\nAddress: {self.address}\nCity: {self.city}\nProvince: {self.province}\nZipCode: {self.zipCode}\nOrder Count: {self.orderCount}"

class Product:
    """product class"""
    def __init__(self,pID = '',name = '',quantity = 1,price = 0.00,color = '',category = '',
                 subcategory = '',description = '',image = ''):
        self.pID = pID
        self.name = name
        self.price = price
        self.quantity = quantity
        self.color = color
        self.category = category
        self.subcategory = subcategory
        self.description = description
        self.image = image
    def __str__(self):
        return f"P_ID: {self.pID}\nName: {self.name}\nPrice: {self.price}\nQuantity: {self.quantity}\nColor: {self.color}\nCategory: {self.category}\nSubCategory: {self.subcategory}\nDescription: {self.description}\nImage: {self.image}"



class Order:
    """order class"""
    def __init__(self,date='',status='',amount=0.00):
        self.date = date
        self.status = status
        self.amount = amount

    def __str__(self):
        return f"Date: {self.date}\nStatus: {self.status}\nAmount: {self.amount}\n"

