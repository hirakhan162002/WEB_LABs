from flask import Flask, request, render_template, jsonify, json, make_response, send_file, flash, session, redirect
from flask_session import Session
from db_classes import *
from model import *
from datetime import datetime
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/product_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# configure app.config to fetch configuration from config.py
app.config.from_object("config")
app.secret_key=app.config["SECRET_KEY"]
Session(app)


###############################################-----ADMIN SIDE ROUTES-----######################################################
@app.route('/')
def mainHome():
    return render_template("mainHome.html")

@app.route('/adminhome')
def admin_home():
    db_prod = ProductModel()
    pro = db_prod.get_total_products()
    db_order = OrdersModel()
    order = db_order.get_total_orders()
    amount = db_order.get_total_amount()
    db_cust = CustomerModel()
    cus = db_cust.get_total_customers()
    db_usr = UserModel()
    user = db_usr.get_total_user()
    return render_template("Admin/admin_dashboard.html", product=pro, orders=order, amu=amount, customer=cus, users=user )

@app.route('/adminLogin' , methods = ["GET", "POST"])
def adminLogin():
    """route for admin Login"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = UserModel()
        status = db.verifyAdmin(email,password)
        if status:
            return redirect('/adminhome')
        else:
            flash("*Credentials are not verified*")
            return render_template("Admin/adminLogin.html")
    else:
        return render_template("Admin/adminLogin.html")

@app.route('/adminProfile', methods = ["GET","POST"])
def adminProfile():
    """route for updating admin profile"""
    db = UserModel()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        usr = User(name, email, new_password)
        status1 = db.verifyAdminPassword(old_password)
        if status1:
            status2 = db.updateAdminDetails(usr)
            if status2:
                flash("*Credentials Updated Successfully!!*")
                profile_ = db.getAdminDetails()
                return render_template("Admin/adminProfile.html", profile_ = profile_)
        else:
            flash("*Credentials not Verified!!*")
            profile_ = db.getAdminDetails()
            return render_template("Admin/adminProfile.html", profile_=profile_)
    else:
        profile_ = db.getAdminDetails()
        return render_template("Admin/adminProfile.html", profile_=profile_)





@app.route('/addProduct', methods = ["GET","POST"])
def addProduct():
    """route to add product"""
    if request.method == "POST":
        name = request.form["productName"]
        color = request.form["ProductColor"]
        quantity = request.form["productQuantity"]
        price = request.form["ProductPrice"]
        category = request.form["productcategory"]
        subCategory = request.form["productsubcategory"]
        description = request.form["ProductDescription"]
        image = request.files["productImage"]
        # Save the image to the UPLOAD_FOLDER
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        prod = Product('',name,quantity,price,color,category,subCategory,description,image.filename)
        db = ProductModel()
        status = db.insertProduct(prod)
        if status:
            return render_template("Admin/Add Product.html",msg = "*Added successfully!!*")
        else:
            return render_template("Admin/Add Product.html")
    else:
        return render_template("Admin/Add Product.html")

@app.route('/customerReport')
def customerList():
    db = CustomerModel()
    customers_=db.getCustomers()
    return render_template("./Admin/Customer_listing.html", customers=customers_)

@app.route('/orderReport')
def orderList():
    db = OrdersModel()
    orders_=db.getAllOrders()
    return render_template("./Admin/Order_listing.html", orders=orders_)


@app.route('/updateRecord', methods=["POST"])
def updateRecord():
    prodId=request.form["id"]
    category=request.form["category"]
    db=ProductModel()
    prodDetails=db.getProductById_dict(prodId)
    if prodDetails is not []:
        return render_template("./Admin/Add Product.html", data = prodDetails )
    else:
        return render_template("./Admin/Product_listing.html", msg="Some unknown error occurred.")

@app.route('/updateProductData', methods=["POST"])
def updateProductData():
    prodId=request.form["id"]
    name = request.form["productName"]
    color = request.form["ProductColor"]
    quantity = request.form["productQuantity"]
    price = request.form["ProductPrice"]
    category = request.form["productcategory"]
    subCategory = request.form["productsubcategory"]
    description = request.form["ProductDescription"]
    image = request.files["productImage"]
    # Save the image to the UPLOAD_FOLDER
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    prod = Product('', name, quantity, price, color, category, subCategory, description, image.filename)

    db= ProductModel()
    status=db.updateProductById(prod,prodId)
    if status:
        plants_list = db.getPlants()
        seeds_list = db.getSeeds()
        fertilizers_list = db.getFertilizers()
        flash("Details Updated Successfully")
        return render_template("./Admin/Product_listing.html",  plants=plants_list, seeds=seeds_list, fertilizers=fertilizers_list)
    else:
        plants_list = db.getPlants()
        seeds_list = db.getSeeds()
        fertilizers_list = db.getFertilizers()
        flash("Could not update details.")
        return render_template("./Admin/Product_listing.html", plants=plants_list, seeds=seeds_list,
                               fertilizers=fertilizers_list)

@app.route('/deleteRecord', methods=["POST"])
def deleteRecord():
    id = request.form["id"]
    category=request.form["category"]
    db=ProductModel()
    status=db.deleteProduct(id)
    if status:
        plants_list = db.getPlants()
        seeds_list = db.getSeeds()
        fertilizers_list = db.getFertilizers()
        if(category=="plant"):
            flash("Plant product removed successfully.")
            return render_template("./Admin/Product_listing.html", plants=plants_list, seeds=seeds_list, fertilizers=fertilizers_list)
        elif (category == "seed"):
            flash("Seed product removed successfully.")
            return render_template("./Admin/Product_listing.html", plants=plants_list, seeds=seeds_list,
                                   fertilizers=fertilizers_list)
        if (category == "fertilizer"):
            flash("Fertilizer product removed successfully.")
            return render_template("./Admin/Product_listing.html", plants=plants_list, seeds=seeds_list,
                                   fertilizers=fertilizers_list)
    else:
        plants_list = db.getPlants()
        seeds_list = db.getSeeds()
        fertilizers_list = db.getFertilizers()
        if (category == "plant"):
            flash("Plant product deletion unsuccessful.")
            return render_template("./Admin/Product_listing.html", plants=plants_list, seeds=seeds_list,
                                   fertilizers=fertilizers_list, plantMsg="Plant product deletion unsuccessful.")
        elif (category == "seed"):
            flash("Seed product deletion unsuccessful.")
            return render_template("./Admin/Product_listing.html", plants=plants_list, seeds=seeds_list,
                                   fertilizers=fertilizers_list)
        if (category == "fertilizer"):
            flash("Fertilizer product deletion unsuccessful.")
            return render_template("./Admin/Product_listing.html", plants=plants_list, seeds=seeds_list,
                                   fertilizers=fertilizers_list)

@app.route('/productListing')
def productsReport():
    db = ProductModel()
    plants_list = db.getPlants()
    seeds_list=db.getSeeds()
    fertilizers_list=db.getFertilizers()
    if plants_list is not None and seeds_list is not None and fertilizers_list is not None:
        return render_template("./Admin/Product_listing.html", plants = plants_list, seeds=seeds_list, fertilizers=fertilizers_list)

@app.route('/updateOrderDetails', methods=["POST"])
def updateOrderDetail():
    orderId=request.form["id"]
    db = OrdersModel()
    db.updateOrderStatusByID(orderId)
    orders_ = db.getAllOrders()
    return render_template("./Admin/Order_listing.html", orders=orders_)

@app.route('/orderDetails', methods = ["POST"])
def showOrderDetails():
    orderId = request.form["id"]
    db_prod = ProductModel()
    db = OrderItemModel()
    order_list = db.getProductID_ByOrderID(orderId)
    products_list = []
    if order_list is not []:
        for ord in order_list:
            product_ = db_prod.getProductByID(ord['product_id'])
            product_.quantity = ord['quantity']
            products_list.append(product_)
        return render_template("./Admin/order_details.html", orderId = orderId, products_list = products_list)
    else:
        return render_template("./Admin/order_details.html", error = "No products found against this order")







###############################################-----USER SIDE ROUTES-----######################################################

@app.route('/home')
def home():
    db = ProductModel()
    product_list = db.getHomeProducts()
    if product_list is not []:
        return render_template("index.html", products=product_list)

@app.route('/About')
def about():
    return render_template("About.html")

@app.route('/signupForm')
def signupForm():
    return render_template("signup.html")

@app.route('/loginForm')
def loginForm():
    return render_template("login.html")

@app.route('/signup',methods=["POST"])
def signup():
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    password2=request.form["password2"]
    if len(password) < 8:
        return render_template("signup.html", msg="Password must be 8 characters long.")
    if password != password2:
        return render_template("signup.html", msg="Passwords do not match.")
    db=UserModel()
    status=db.userExist(email)
    if status:
        return render_template("signup.html", msg2="A user with this email already exists.")
    usr=User(name,email,password)
    status=db.insertUser(usr)
    if status:
        return render_template("login.html")
    else:
        return render_template("signup.html", errmsg="Some unknown error occurred during registration. Please try again!")

@app.route('/login',methods=["POST"])
def login():
    email=request.form["email"]
    password=request.form["password"]

    db = UserModel()
    status=db.userExist(email)

    if not status:
        return render_template("login.html", msg="No user with this email is registered on our website.")
    else:
        status2 = db.verifyCredentials(email,password)
        if status2:
            data=db.getCredentials(email,password)
            session["uid"]=data["id"]
            session["uname"]=data["name"]
            session["uemail"]=email
            session["upassword"]=password
            return redirect('/home')
        else:
            return render_template("login.html", msg="*Credentials not verified.")


@app.route('/fruits')
def seed_fruits():
    """route to show seeds"""
    category = "seeds"
    subcategory = "fruits"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("seed.html",  products=product_list,  name= "Fruits")
    else:
        return render_template("seed.html", msg="No Available Item in this list", name= "Fruits")


@app.route('/flowers')
def seed_flowers():
    category = "seeds"
    subcategory = "flowers"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("seed.html",  products=product_list,  name= "Flowers")
    else:
        return render_template("seed.html", msg="No Available Item in this list",  name= "Flowers")


@app.route('/vegetables')
def seed_vegetables():
    """route to show seeds"""
    category = "seeds"
    subcategory = "vegetables"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("seed.html",  products=product_list,  name= "Vegetables")
    else:
        return render_template("seed.html", msg="No Available Item in this list", name= "Vegetables")


@app.route('/indoor_plants')
def seed_indoor_plants():
    """route to show seeds"""
    category = "seeds"
    subcategory = "indoor plants"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("seed.html",  products=product_list,  name= "Indoor Plants")
    else:
        return render_template("seed.html", msg="No Available Item in this list", name= "Indoor Plants")



@app.route('/Nfertilizer')
def show_n_fertilizer():
    """route to show fertilizers"""
    db = ProductModel()
    name = "fertilizers"
    subcategory = "nitrogen"
    fertilizer_list = db.get_categories_data(name, subcategory)
    if fertilizer_list:
        return render_template("fertilizer.html", fertilizers=fertilizer_list, fertilizerName=subcategory.capitalize())
    else:
        return render_template("fertilizer.html", msg="No Available Item in this list", fertilizerName=subcategory.capitalize())

@app.route('/PHfertilizer')
def show_ph_fertilizer():
    """route to show fertilizers"""
    name = "fertilizers"
    subcategory = "phosphorus"
    db = ProductModel()
    fertilizer_list = db.get_categories_data(name, subcategory)
    if fertilizer_list:
        return render_template("fertilizer.html", fertilizers=fertilizer_list, fertilizerName=subcategory.capitalize())
    else:
        return render_template("fertilizer.html", msg="No Available Item in this list", fertilizerName=subcategory.capitalize())



@app.route('/Pfertilizer')
def show_pf_fertilizer():
    """route to show fertilizers"""
    name = "fertilizers"
    subcategory = "potassium"
    db = ProductModel()
    fertilizer_list = db.get_categories_data(name, subcategory)
    if fertilizer_list:
        return render_template("fertilizer.html", fertilizers=fertilizer_list, fertilizerName=subcategory.capitalize())
    else:
        return render_template("fertilizer.html", msg="No Available Item in this list", fertilizerName=subcategory.capitalize())



@app.route('/flowering')
def flowering_plants():
    """route to show plants"""
    category = "plants"
    subcategory = "flowering plants"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("plant.html",  products=product_list,  name=subcategory.capitalize())
    else:
        return render_template("plant.html", msg="No Available Item in this list", name=subcategory.capitalize())


@app.route('/non-flowering')
def non_flowering_plants():
    """route to show plants"""
    category = "plants"
    subcategory = "non flowering plants"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("plant.html",  products=product_list,  name= "Non Flowering Plants")
    else:
        return render_template("plant.html", msg="No Available Item in this list", name= "Non Flowering Plants")


@app.route('/climber')
def climber_plants():
    """route to show plants"""
    category = "plants"
    subcategory = "climbing plants"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("plant.html",  products=product_list,  name= "Climbing Plants")
    else:
        return render_template("plant.html", msg="No Available Item in this list", name= "Climbing Plants")


@app.route('/creeper')
def creeper_plants():
    """route to show plants"""
    category = "plants"
    subcategory = "creepers"
    db = ProductModel()
    product_list = db.get_categories_data(category, subcategory)
    if product_list:
        return render_template("plant.html",  products=product_list,  name= "Creepers")
    else:
        return render_template("plant.html", msg="No Available Item in this list", name= "Creepers")


@app.route("/single_product", methods=["GET", "POST"])
def single_product():
    if request.method == "POST":
        id_ = int(request.form['product_id'])
        db = ProductModel()
        product_data = db.get_single_product_detail(id_)
        return render_template("singleProduct.html", product=product_data)
    else:
        return render_template("singleProduct.html")


@app.route('/userProfile')
def showUserProfile():
    """route to show user profile info"""
    if 'uemail' not in session:
        return render_template("login.html")
    else:
        uemail = session['uemail']
        db_usr = UserModel()
        usr_id = db_usr.getUserID(uemail)
        db_cust = CustomerModel()
        cust_id, customerData = db_cust.getCustomerByUserID(usr_id)
        if cust_id:
            db_order = OrdersModel()
            order_list = db_order.getOrdersByCustomerID(cust_id)
            if order_list is not None:
                return render_template("accountinfo.html", customer = customerData, orders = order_list)
            else:
                return render_template("accountinfo.html", customer = customerData)
        else:
            return render_template("accountinfo.html", name=session["uname"])


@app.route('/updateProfile', methods = ["GET","POST"])
def updateProfile():
    """route to update profile data"""
    if request.method == "POST":
        uemail = session["uemail"]
        upassword = session["upassword"]
        psw = request.form["password"]
        if psw == upassword:
            db = UserModel()
            db_cust = CustomerModel()
            if 'firstname' in request.form:
                fname = request.form["firstname"]
                lname = request.form["lastname"]
                name = fname + " " + lname
                status = db.updateName(name, uemail)
            if 'email' in request.form:
                new_email = request.form["email"]
                status = db.updateEmail(new_email, uemail)
                if status:
                    session["uemail"] = new_email
            if 'newpassword' in request.form:
                new_psw = request.form["newpassword"]
                status = db.updatePassword(new_psw,uemail)
                if status:
                    session["upassword"] = new_psw
            if status:
                flash('Profile Updated successfully!')
                return render_template("UpdateProfile.html")
        else:
            flash('Error in updating Profile!!')
            return render_template("UpdateProfile.html")
    else:
        return render_template("UpdateProfile.html")




@app.route('/cart', methods=["GET","POST"])
def viewCart():
    """route to add products in cart"""
    if 'cart' not in session:
        session['cart'] = []
    cart = session.get('cart', [])
    p_quantity = None
    orderTotal = 0
    if request.method == "POST":
        product_id = int(request.form["product_id"])
        db = ProductModel()
        product = db.getProductByID(product_id)#product is list of dictionary objects
        if 'productQuantity' in request.form:
            p_quantity = request.form['productQuantity']
        cart_prod_ID = None
        for p in cart:
            if p.pID == product_id:
                cart_prod_ID = p.pID
                if int(product.quantity) > int(p.quantity):
                    if p_quantity is not None:
                        p.quantity = int(p.quantity) + int(p_quantity)
                    else:
                        p.quantity = int(p.quantity) + 1
        # product is already present in the cart session
        if cart_prod_ID is not None:
            if product is not None:
                for items in cart:
                    orderTotal += int(items.quantity) * int(items.price)
                session['orderTotal'] = orderTotal
                return render_template("cart.html", cart = cart, orderTotal = orderTotal)
            else:
                for items in cart:
                    orderTotal += int(items.quantity) * int(items.price)
                session['orderTotal'] = orderTotal
                flash("Product Out of Stock!!")
                return render_template("cart.html", cart = cart, orderTotal = orderTotal)
        # product is not present in cart session
        else:
            if product is not None:
                if p_quantity is not None:
                    product.quantity = p_quantity
                else:
                    product.quantity = '1'
                session['cart'].append(product)
                for items in cart:
                    orderTotal += int(items.quantity) * int(items.price)
                session['orderTotal'] = orderTotal
                return render_template("cart.html", cart = cart, orderTotal = orderTotal)
            else:
                for items in cart:
                    orderTotal += int(items.quantity) * int(items.price)
                session['orderTotal'] = orderTotal
                flash("Product Out of Stock!!")
                return render_template("cart.html", cart = cart , orderTotal = orderTotal)
    else:
        if len(cart) == 0:
            flash("Nothing in Cart!!")
            return render_template("cart.html", orderTotal = orderTotal)
        else:
            return render_template("cart.html", cart=cart, orderTotal = session['orderTotal'])


@app.route('/removeFromCart', methods = ["POST"])
def removeFromCart():
    if request.method == "POST":
        product_id = request.form["product_id"]
        product_id = int(product_id)
        db = ProductModel()
        product = db.getProductByID(product_id)
        cart = session.get('cart', [])
        for prod in cart:
            if prod.pID == product_id:
                cart.remove(prod)
                break
        orderTotal = 0
        for items in cart:
            orderTotal += int(items.quantity) * int(items.price)
        session['orderTotal'] = orderTotal
        return render_template("cart.html",cart = cart, orderTotal = orderTotal)
    else:
        return render_template("cart.html")

@app.route('/plusQuantity', methods = ["POST"])
def quantityManagement():
    if request.method == "POST":
        product_id = request.form["product_id"]
        product_id = int(product_id)
        db = ProductModel()
        product = db.getProductByID(product_id)
        cart = session.get('cart', [])
        for prod in cart:
            if prod.pID == product_id:
                if int(product.quantity) > int(prod.quantity):
                    prod.quantity = int(prod.quantity) + 1
        orderTotal = 0
        for items in cart:
            orderTotal += int(items.quantity) * int(items.price)
        session['orderTotal'] = orderTotal
        return render_template("cart.html", cart=cart, orderTotal=session['orderTotal'])
    else:
        return render_template("cart.html")

@app.route('/minusQuantity', methods = ["POST"])
def minus_quantity():
    if request.method == "POST":
        product_id = request.form["product_id"]
        product_id = int(product_id)
        db = ProductModel()
        product = db.getProductByID(product_id)
        cart = session.get('cart', [])
        for prod in cart:
            if prod.pID == product_id:
                if (int(prod.quantity) - 1) > 0 and int(product.quantity) > int(prod.quantity):
                    prod.quantity = int(prod.quantity) - 1
                elif (int(prod.quantity) - 1) == 0:
                    cart.remove(prod)
                    break
        orderTotal = 0
        for items in cart:
            orderTotal += int(items.quantity) * int(items.price)
        session['orderTotal'] = orderTotal
        return render_template("cart.html", cart=cart, orderTotal=session['orderTotal'])
    else:
        return render_template("cart.html")

@app.route('/orderConfirmation')
def orderConfirmation():
    return render_template("orderConfirmation.html")

@app.route('/shippingInfo' , methods=["GET","POST"])
def shippingInfo():
    if request.method == "POST":
        number = request.form["phone"]
        address = request.form["address"]
        city = request.form["city"]
        province = request.form["province"]
        zipCode = request.form["zip"]

        orderPrice = session["orderTotal"]
        cart = session.get('cart', [])
        if len(number) != 11:
            return render_template("shipping_info.html",cart=cart, orderTotal=orderPrice,msg="Incorrect phone number!")
        cust=Customer(session["uname"],session["uemail"],session["upassword"],number,address,city,province,str(zipCode))
        db=CustomerModel()
        custID, customer = db.getCustomerByUserID(session["uid"])
        if custID and customer is not None:
            if customer.phone != number or customer.address != address or customer.city != city or customer.province != province or customer.zipCode != zipCode:
                db.updateCustomerByUserID(Customer('','','',number,address,city,province,str(zipCode)), session["uid"])
            orderCount = int(customer.orderCount) + 1
            db.add_order_count_for_existing_customer(custID,orderCount)
            db_prod = ProductModel()
            for p in cart:
                prod_ = db_prod.getProductByID(p.pID)
                quant = int(prod_.quantity) - int(p.quantity)
                db_prod.updateQuantityByPid(p.pID, quant)
            DB = OrdersModel()
            orderID = DB.addOrder(str(int(orderPrice) + 150), custID)
            if orderID is not None:
                db_orderItems = OrderItemModel()
                for product in cart:
                    db_orderItems.insert_into_orderItem(orderID, product.pID, product.quantity)
                t_date = datetime.today().strftime('%Y-%m-%d')
                session.pop("cart",[])
                return render_template("orderConfirmation.html", id=orderID, name=session["uname"], contact=number,
                                           orderTotal=orderPrice, date=t_date, ship_address=address)
            else:
                return render_template("shipping_info.html", cart=cart, orderTotal=orderPrice,
                                       msg="*Some unknown error occurred while proceeding.")
        else:
            status=db.insertCustomer(cust,session["uid"])
            if status is not None:
                db_prod = ProductModel()
                for p in cart:
                    prod_ = db_prod.getProductByID(p.pID)
                    quant = int(prod_.quantity) - int(p.quantity)
                    db_prod.updateQuantityByPid(p.pID,quant)
                DB=OrdersModel()
                orderID =DB.addOrder(str(int(orderPrice) + 150),status[0])
                if orderID is not None:
                    db_orderItems = OrderItemModel()
                    for product in cart:
                        db_orderItems.insert_into_orderItem(orderID,product.pID, product.quantity)
                    t_date = datetime.today().strftime('%Y-%m-%d')
                    session.pop("cart", [])
                    return render_template("orderConfirmation.html", id=orderID, name=session["uname"], contact=number,
                                           orderTotal=orderPrice, date=t_date, ship_address=address)
                else:
                    return render_template("shipping_info.html", cart = cart, orderTotal = orderPrice, msg="*Some unknown error occurred while proceeding.")
            else:
                return render_template("shipping_info.html", cart = cart, orderTotal = orderPrice, msg="*Some unknown error occurred while proceeding.")
    else:
        if 'uemail' and 'uname' not in session:
            return render_template('login.html')
        elif 'orderTotal' not in session:
            flash("Cannot proceed with empty Cart!!")
            return render_template("cart.html", orderTotal="0")
        orderPrice = session["orderTotal"]
        cart = session.get('cart', [])
        return render_template("shipping_info.html", cart=cart, orderTotal=orderPrice)

@app.route('/logout')
def logOut():
    session.clear()
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
