import pymysql
import base64
from db_classes import *
from datetime import datetime
import os

class UserModel:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        try:
            self.__connection = pymysql.connect(host='localhost', user='root', password='pythOn~2022', database='webproject')
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(str(e))

    def verifyAdmin(self,email, password):
        try:
            if self.__connection is None:
                self.connect()
            query = "select email,password from `user` where `role` = %s"
            self.__cursor.execute(query, "admin")
            data = self.__cursor.fetchone()
            if data[0] == email and data[1] == password:
                return True
        except Exception as e:
            print(str(e))
            return False

    def verifyAdminPassword(self,old_password):
        try:
            if self.__connection is None:
                self.connect()
            query = "SELECT password from `user` where `role` = %s"
            args = ("admin")
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchone()
            if data:
                if data[0] == old_password:
                    return True
                else:
                    return False
        except Exception as e:
            print(str(e))
            return False

    def getAdminDetails(self):
        user = None
        try:
            if self.__connection is None:
                self.connect()
            query = "SELECT * from `user` where `role` = %s"
            args = ("admin")
            self.__cursor.execute(query, args)
            data = self.__cursor.fetchone()
            user = User(data[1],data[2],data[3])
        except Exception as e:
            print(str(e))
        finally:
            return user

    def updateAdminDetails(self, user):
        try:
            if self.__connection is None:
                self.connect()
            query = "UPDATE `user` SET `name` = %s, email = %s, password = %s WHERE `role` = %s"
            args = (user.name,user.email,user.password,"admin")
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def verifyCredentials(self,email,password):
        status=False
        result=None
        try:
            if self.__connection is None:
                self.connect()
            query="SELECT * from `user` where (email= %s AND password = %s)"
            args=(email,password)
            self.__cursor.execute(query,args)
            result=self.__cursor.fetchall()
            if result:
                status=True
        except Exception as e:
            print(str(e))
        finally:
            return status

    def getCredentials(self,email,password):
        data={}
        try:
            if self.__connection is None:
                self.connect()
            query="SELECT ID,`name` from `user` where (email= %s AND password = %s)"
            args=(email,password)
            self.__cursor.execute(query,args)
            result=self.__cursor.fetchone()
            data.update({'id':result[0]})
            data.update({'name': result[1]})
        except Exception as e:
            print(str(e))
        finally:
            return data

    def userExist(self,email):
        results=None
        status=False
        try:
            if self.__connection is None:
                self.connect()
            query="select * from `user` where email= %s"
            args=(email)
            self.__cursor.execute(query,args)
            results=self.__cursor.fetchall()
            if results:
                status=True
        except Exception as e:
            print(str(e))
            status=True
        finally:
            return status

    def getUsers(self):
        user_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from `user` where `role` = %s"
            self.__cursor.execute(query,"user")
            data = self.__cursor.fetchall()
            for item in data:
                user = User(item[1], item[2], item[3])
                user_list.append(user)
        except Exception as e:
            print(str(e))
        finally:
            return user_list

    def getUserID(self,email):
        id_ = None
        try:
            if self.__connection is None:
                self.connect()
            query = "select ID from `user` where email = %s"
            args = (email)
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchone()
            id_ = data[0]
        except Exception as e:
            print(str(e))
        finally:
            return id_

    def getUserByID(self,usrID):
        user = None
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from `user` where ID = %s"
            args = (usrID)
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchone()
            user = User(data[1],data[2],data[3])
        except Exception as e:
            print(str(e))
        finally:
            return user

    def insertUser(self,user):
        try:
            if self.__connection is None:
                self.connect()
            query = "insert into `user`(`name`,`email`,`password`,`role`) values (%s,%s,%s,%s)"
            args = (user.name,user.email,user.password, "user")
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def updateName(self, name, email):
        try:
            if self.__connection is None:
                self.connect()
            userID = self.getUserID(email)
            query = "UPDATE `user` SET `name` = %s WHERE ID = %s"
            args = (name,userID)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def updateEmail(self, newEmail, email):
        try:
            if self.__connection is None:
                self.connect()
            userID = self.getUserID(email)
            query = "UPDATE `user` SET email = %s WHERE ID = %s"
            args = (newEmail,userID)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def updatePassword(self, newpsw, email):
        try:
            if self.__connection is None:
                self.connect()
            userID = self.getUserID(email)
            query = "UPDATE `user` SET password = %s WHERE ID = %s"
            args = (newpsw,userID)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def get_total_user(self):
        count = None
        try:
            if self.__connection is None:
                self.connect()
            query = "select COUNT(ID) FROM `user` where `role` = %s"
            self.__cursor.execute(query, "user")
            data = self.__cursor.fetchall()
            count = data[0][0]
            print(count)
        except Exception as e:
            print(str(e))
        finally:
            return count

class ProductModel:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        try:
            self.__connection = pymysql.connect(host='localhost', user='root', password='pythOn~2022', database='webproject')
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(str(e))

    def getProducts(self):
        product_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products"
            self.__cursor.execute(query)
            data = self.__cursor.fetchall()
            for row in data:
                product_list.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'price': row[3],
                    'color': row[4],
                    'description' : row[7],
                    'image': row[8]
                })
        except Exception as e:
            print(str(e))
        finally:
            return product_list

    def getProductByID(self,prodID):
        product_ = None
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where p_id = %s"
            args = (prodID)
            self.__cursor.execute(query,args)
            row = self.__cursor.fetchone()
            product_ = Product(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            if product_ is not None:
                if product_.quantity == '0':
                    product_ = None
        except Exception as e:
            print(str(e))
        finally:
            return product_

    def getProductById_dict(self, prodId):
        product_={}
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where p_id=%s"
            args=(prodId)
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchone()
            product_.update({
                'id': data[0],
                'name': data[1],
                'quantity': data[2],
                'price': data[3],
                'color': data[4],
                'category': data[5],
                'subcategory': data[6],
                'description': data[7],
                'image': data[8]
            })
        except Exception as e:
            print(str(e))
        finally:
            return product_

    def updateProductById(self,prod,id):
        status= True
        try:
            if self.__connection is None:
                self.connect()

            query="update products set name=%s,quantity=%s,price=%s,color=%s,category=%s,subcategory=%s,description=%s,image=%s where p_id=%s"
            args=(prod.name,prod.quantity,prod.price,prod.color,prod.category,prod.subcategory,prod.description, prod.image,id)
            self.__cursor.execute(query,args)
            self.__connection.commit()
        except Exception as e:
            print(str(e))
            status=False
        finally:
            return status

    def getPlants(self):
        plants_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where category=%s"
            args=("plants")
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchall()
            for row in data:
                plants_list.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'price': row[3],
                    'color': row[4],
                    'subcategory':row[6],
                    'description': row[7],
                    'image': row[8]
                })
        except Exception as e:
            print(str(e))
        finally:
            return plants_list

    def getSeeds(self):
        seeds_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where category=%s"
            args=("seeds")
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchall()
            for row in data:
                seeds_list.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'price': row[3],
                    'color': row[4],
                    'subcategory':row[6],
                    'description': row[7],
                    'image': row[8]
                })
        except Exception as e:
            print(str(e))
        finally:
            return seeds_list

    def getFertilizers(self):
        fertilizers_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where category=%s"
            args=("fertilizers")
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchall()
            for row in data:
                fertilizers_list.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'price': row[3],
                    'color': row[4],
                    'subcategory':row[6],
                    'description': row[7],
                    'image': row[8]
                })
        except Exception as e:
            print(str(e))
        finally:
            return fertilizers_list

    def updateQuantityByPid(self, prod_id, quantity):
        try:
            if self.__connection is None:
                self.connect()
            query = "UPDATE products SET quantity = %s WHERE ( p_id = %s )"
            args = (quantity,prod_id)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False


    def insertProduct(self,product):
        try:
            if self.__connection is None:
                self.connect()
            query = "insert into products(`name`,quantity,price,color,category,subcategory,description,image) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (product.name,product.quantity,product.price,product.color,product.category,product.subcategory,product.description,product.image)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def get_categories_data(self, category, subcategory):
        product_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where category = %s and subcategory = %s"
            args = (category,subcategory)
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchall()
            for row in data:
                product_list.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'price': row[3],
                    'color': row[4],
                    'category' : row[5],
                    'subcategory' : row[6],
                    'description': row[7],
                    'image': row[8]
                })
        except Exception as e:
            print(str(e))
        finally:
            return product_list

    def getHomeProducts(self):
        product_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where category = 'plants' and subcategory = 'flowering plants' "
            self.__cursor.execute(query)
            data1 = self.__cursor.fetchone()
            query = "select * from products where category = 'plants' and subcategory = 'non flowering plants' "
            self.__cursor.execute(query)
            data2 = self.__cursor.fetchone()
            query = "select * from products where category = 'plants' and subcategory = 'climbing plants' "
            self.__cursor.execute(query)
            data3 = self.__cursor.fetchone()
            query = "select * from products where category = 'plants' and subcategory = 'creepers' "
            self.__cursor.execute(query)
            data4 = self.__cursor.fetchone()
            query = "select * from products where category = 'seeds' and subcategory = 'fruits' "
            self.__cursor.execute(query)
            data5 = self.__cursor.fetchone()
            query = "select * from products where category = 'seeds' and subcategory = 'vegetables' "
            self.__cursor.execute(query)
            data6 = self.__cursor.fetchone()
            query = "select * from products where category = 'seeds' and subcategory = 'indoor plants' "
            self.__cursor.execute(query)
            data7 = self.__cursor.fetchone()
            query = "select * from products where category = 'seeds' and subcategory = 'flowers' "
            self.__cursor.execute(query)
            data8 = self.__cursor.fetchone()
            query = "select * from products where category = 'fertilizers' and subcategory = 'nitrogen' "
            self.__cursor.execute(query)
            data9 = self.__cursor.fetchone()
            query = "select * from products where category = 'fertilizers' and subcategory = 'phosphorus' "
            self.__cursor.execute(query)
            data10 = self.__cursor.fetchone()
            query = "select * from products where category = 'fertilizers' and subcategory = 'potassium' "
            self.__cursor.execute(query)
            data11 = self.__cursor.fetchone()
            query = "select * from products where category = 'fertilizers' and subcategory = 'potassium' and `name` = 'Potassium sulphate'"
            self.__cursor.execute(query)
            data12 = self.__cursor.fetchone()
            list_of_data=[data1, data2,data3, data4, data5, data6, data7, data8, data9, data10, data11, data12]
            for row in list_of_data:
                    product_list.append({
                        'id': row[0],
                        'name': row[1],
                        'quantity': row[2],
                        'price': row[3],
                        'color': row[4],
                        'description': row[7],
                        'image': row[8]
                    })
        except Exception as e:
            print(str(e))
        finally:
            return product_list

    def get_single_product_detail(self, id_):
        product_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from products where p_id = %s"
            argu = (id_)
            self.__cursor.execute(query, argu)
            data = self.__cursor.fetchall()
            for row in data:
                product_list.append({
                    'id': row[0],
                    'name': row[1],
                    'quantity': row[2],
                    'price': row[3],
                    'color': row[4],
                    'description': row[7],
                    'image': row[8]
                })
        except Exception as e:
            print(str(e))
        finally:
            return product_list

    def deleteProduct(self, id):
        status = True
        try:
            if self.__connection is None:
                self.connect()
            query = "delete from products where p_id=%s"
            args = (id)
            self.__cursor.execute(query, args)
            self.__connection.commit()
        except Exception as e:
            print(str(e))
            status = False
        finally:
            return status

    def get_total_products(self):
        count = None
        try:
            if self.__connection is None:
                self.connect()
            query = "select COUNT(p_id) FROM products"
            self.__cursor.execute(query)
            data = self.__cursor.fetchall()
            count = data[0][0]
            print(count)
        except Exception as e:
            print(str(e))
        finally:
            return count

class OrdersModel:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        try:
            self.__connection = pymysql.connect(host='localhost', user='root', password='pythOn~2022', database='webproject')
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(str(e))

    def getOrders(self):
        order_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from `order`"
            self.__cursor.execute(query)
            data = self.__cursor.fetchall()
            for item in data:
                order = Order(item[1],item[2],item[3])
                order_list.append(order)
        except Exception as e:
            print(str(e))
        finally:
            return order_list

    def getOrdersByCustomerID(self, custID):
        order_list = []
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from `order` where customer_id = %s"
            args = (custID)
            self.__cursor.execute(query, args)
            data = self.__cursor.fetchall()
            for item in data:
                order_list.append(
                    {'id' : item[0],
                     'date' : item[1],
                     'status' : item[2],
                     'amount' : item[3]}
                )
        except Exception as e:
            print(str(e))
        finally:
            return order_list

    def getAllOrders(self):
        orders_=[]
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from `order`"
            self.__cursor.execute(query)
            results= self.__cursor.fetchall()
            for result in results:
                orders_.append({
                    'ID':result[0],
                    'date':result[1],
                    'status':result[2],
                    'amount':result[3],
                    'customer_id':result[4]
                })
            print(orders_)
        except Exception as e:
            print(str(e))
        finally:
            return orders_

    def addOrder(self, orderPrice, custId):
        order_id = None
        try:
            if self.__connection is None:
                self.connect()
            query= "insert into `order`(`date`,status,amount,customer_id) values(curdate(),default,%s,%s)"
            args=(orderPrice, custId)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            query2 = "select ID from `order` where `date`=%s AND status=%s AND amount=%s AND customer_id=%s"
            s = datetime.today().strftime('%Y-%m-%d')
            args2 = (s, 'pending', orderPrice, custId)
            self.__cursor.execute(query2, args2)
            data = self.__cursor.fetchone()
            order_id = data[0]
        except Exception as e:
            print(str(e))
        finally:
            return order_id

    def get_total_orders(self):
        count = 0
        try:
            if self.__connection is None:
                self.connect()
            query = 'select  count(ID) from `order`'
            self.__cursor.execute(query)
            data = self.__cursor.fetchall()
            count = data[0][0]
        except Exception as e:
            print(str(e))
        finally:
            return count


    def get_total_amount(self):
        count = 0
        try:
            if self.__connection is None:
                self.connect()
            query = 'select  amount from `order`'
            self.__cursor.execute(query)
            data = self.__cursor.fetchall()
            for item in data:
                print(item[0])
                count = count + int(item[0])
        except Exception as e:
            print(str(e))
        finally:
            return count

    def updateOrderStatusByID(self,id):
        status=True
        try:
            if self.__connection is None:
                self.connect()

            query="update `order` set status=%s where ID= %s"
            args=("Delivered",id)
            self.__cursor.execute(query,args)
            self.__connection.commit()
        except Exception as e:
            print(str(e))
            status=False
        finally:
            return status


class CustomerModel:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        try:
            self.__connection = pymysql.connect(host='localhost', user='root', password='pythOn~2022', database='webproject')
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(str(e))

    def getCustomerByUserID(self,usrID):
        customer = None
        cust_id = None
        try:
            if self.__connection is None:
                self.connect()
            query = "select * from customer where user_id = %s"
            args = (usrID)
            self.__cursor.execute(query,args)
            data = self.__cursor.fetchone()
            db = UserModel()
            user_data = db.getUserByID(usrID)
            cust_id = data[0]
            customer = Customer(user_data.name,user_data.email,user_data.password,data[1],data[2],data[3],data[4],data[5],data[7])
        except Exception as e:
            print(str(e))
        finally:
            return cust_id,customer

    def getCustomers(self):
        customer_list = []
        try:
            if self.__connection is None:
                self.connect()
            query1 = "select * from customer"
            self.__cursor.execute(query1)
            data = self.__cursor.fetchall()
            print("got Data from customers.")
            for customer in data:
                id=customer[6]
                print(id)
                print("Gonna get data from user")
                query2 = "select * from user where ID = %s"
                args=(id)
                self.__cursor.execute(query2,args)
                udata = self.__cursor.fetchone()
                print("got data from user")
                customer_list.append({
                    'ID':customer[0],
                    'name': udata[1],
                    'email': udata[2],
                    'password': udata[3],
                    'phone': customer[1],
                    'address': customer[2],
                    'city': customer[3],
                    'province': customer[4],
                    'zipCode': customer[5],
                    'orderCount': customer[7],
                    'user_id': customer[6]
                })
        except Exception as e:
            print(str(e))
        finally:
            return customer_list


    def insertCustomer(self,customer, userID):
        data =None
        try:
            if self.__connection is None:
                self.connect()
            query1 = "insert into customer(phone,address,city,province,zip_code,user_id) values (%s,%s,%s,%s,%s,%s)"
            args1 = (customer.phone,customer.address,customer.city,customer.province,customer.zipCode,userID)
            self.__cursor.execute(query1,args1)
            self.__connection.commit()
            query2="select ID from customer where phone=%s AND address=%s AND city= %s AND province=%s AND zip_code=%s AND user_id=%s"
            args2=(customer.phone,customer.address,customer.city,customer.province,customer.zipCode,userID)
            self.__cursor.execute(query2,args2)
            data = self.__cursor.fetchone()
        except Exception as e:
            print(str(e))
        finally:
            return data

    def updateCustomerByUserID(self, cust_data, userID):
        try:
            if self.__connection is None:
                self.connect()
            query = "UPDATE customer SET phone = %s, address = %s, city = %s, province = %s, zip_code = %s WHERE user_id = %s"
            args = (cust_data.phone, cust_data.address, cust_data.city, cust_data.province, cust_data.zipCode, userID)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def add_order_count_for_existing_customer(self, custID, orderCount):
        try:
            if self.__connection is None:
                self.connect()
            query = "UPDATE customer SET order_count = %s WHERE ID = %s"
            args = (orderCount,custID)
            self.__cursor.execute(query, args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def updatePhoneNo(self, phoneno, email):
        try:
            if self.__connection is None:
                self.connect()
            db_user = UserModel()
            userID = db_user.getUserID(email)
            query = "UPDATE customer SET phone = %s WHERE user_id = %s"
            args = (phoneno,userID)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def updateAddress(self, address, email):
        try:
            if self.__connection is None:
                self.connect()
            db_user = UserModel()
            userID = db_user.getUserID(email)
            query = "UPDATE customer SET address = %s WHERE user_id = %s"
            args = (address,userID)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def get_total_customers(self):
        count = None
        try:
            if self.__connection is None:
                self.connect()
            query = "select COUNT(ID) FROM customer"
            self.__cursor.execute(query)
            data = self.__cursor.fetchall()
            count = data[0][0]
            print(count)
        except Exception as e:
            print(str(e))
        finally:
            return count

class OrderItemModel:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        try:
            self.__connection = pymysql.connect(host='localhost', user='root', password='pythOn~2022', database='webproject')
            self.__cursor = self.__connection.cursor()
        except Exception as e:
            print(str(e))

    def insert_into_orderItem(self, orderID, prodID, quantity):
        try:
            if self.__connection is None:
                self.connect()
            query = "insert into order_items(order_id, product_id, quantity) values (%s,%s,%s)"
            args = (orderID,prodID,quantity)
            self.__cursor.execute(query,args)
            self.__connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def getProductID_ByOrderID(self, orderID):
        orderDetailsList = []
        try:
            if self.__connection is None:
                self.connect()
            query = "SELECT product_id, quantity from order_items where order_id = %s"
            args = (orderID)
            self.__cursor.execute(query, args)
            data = self.__cursor.fetchall()
            for item in data:
                orderDetailsList.append({'product_id': item[0], 'quantity' : item[1]})
        except Exception as e:
            print(str(e))
        finally:
            return orderDetailsList


