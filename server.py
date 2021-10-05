# import the Flask class from the flask library
import sqlite3 as sql

from model import *
#from user_authentication import *
from flask import Flask,render_template,request,redirect,jsonify

# create the application object
app = Flask(__name__)

@app.route('/home')
def Home():
    return render_template('home.html')

# show all Products
@app.route('/products')
def Products():
    rows = productList()
    return render_template('products.html', rows=rows)

# show all Customers
@app.route('/customerList')
def custList():
    rows = customerList()
    return render_template('customerList.html', rows=rows)

# show all Sellers
@app.route('/sellerList')
def SellerList():
    rows = sellerList()
    return render_template('seller.html', rows=rows)

# show all Orders
@app.route('/orderList')
def OrderList():
    rows = orders()
    return render_template('order.html', rows=rows)

# Submit New Customer data
@app.route('/newCustomer')
def CustomerSubmit():
    # Make and blank array of five elements
    row=['']*7
    status='0'
    return render_template('customerForm.html',row=row,status=status)

@app.route('/update',methods=['GET','POST'])
def  insert_update():
    customerID = request.form['customerID']
    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    password = request.form['password']
      
    if request.method=='POST' and request.form['status']=='0':                            
        row=['']*7
        row[0] = customerID
        row[1] = name
        row[2] = address
        row[3] = city
        row[4] = state
        row[5] = phone
        row[6] = password
        
        if customerID == '' or name == '' or address == '' or city == '' or state == '' or phone == '' or password == '':
            msg = '';
            if customerID == '':
                msg += 'Cutomer ID' if len(msg)==0 else ',Cutomer ID'
            if name == '':
                msg += 'Name' if len(msg)==0 else ',Name'
            if address == '':
                msg += 'Address' if len(msg)==0 else ',Address'
            if city == '':
                msg += 'City' if len(msg)==0 else ',City'
            if state == '':
                msg += 'State' if len(msg)==0 else ',State'
            if phone == '':
                msg += 'Phone' if len(msg)==0 else ',Phone'
            if password == '':
                msg += 'Password' if len(msg)==0 else ',Password'
            msg = msg + ' cannot be empty!';
            return render_template('customerForm.html',message=msg,status='0',row=row)
        else:
            if check_custID(customerID):
                row[0] = ''
                flash('customer ID already exist!')                
                return render_template('customerForm.html',message='customer ID '+customerID+' already exist!',status='0',row=row)

            else:        
                insert_customer(customerID,name,address,city,state,phone,password)        
                return redirect('/customerList')
             
          
    if request.method=="POST" and request.form['status']=='1':
        update_customer(name,address,city,state,phone,password,customerID) 
        return redirect('/customerList')

# update data
@app.route('/edit/<customerID>')
def edit(customerID): 
    row = find_customer(customerID)
    status='1'
    return render_template('customerForm.html',row=row,status=status)

# delete data
@app.route('/delete/<customerID>')
def delete(customerID):  
     delete_customer(customerID)
     return redirect('/customerList')
    
@app.route('/deleteOrder/<orderNo>')
def DeleteOrder(orderNo):  
     delete_order(orderNo)
     return redirect('/orderList')
    
# Search Customer
@app.route('/searchCustomer',methods=['GET','POST'])
def find():
    if request.method=="POST":
        customerID = request.form['customerID']
        row = find_customer(customerID)
        return render_template('form2.html',row=row)
    else:   
        return render_template('form1.html')
    
# place order
@app.route('/placeOrder')
def PlaceOrder():
    # Make and blank array of six elements
    row=['']*9
    status='0'
    pdt = productList()
    product = productList()
    return render_template('placeOrder.html',row=row,status=status,product=product,pdt=pdt)

@app.route('/inupdateorder',methods=['GET','POST'])
def  insert_updateg():
    orderNo = None
    if 'orderNo' in request.files:
        orderNo = request.form['orderNo']
    Product_No =  request.form['Product_No']      
    quantity=request.form['quantity']    
    totalPrice=request.form['totalPrice']
    placedDate=request.form['placedDate']
    
    if request.method=='POST' and request.form['status']=='0':                            
                
        insert_order(Product_No,quantity,totalPrice,placedDate)        
        return redirect('/orderList') 

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('loginnew.html')
    else:
        return render_template('home.html')

@app.route('/login', methods=['POST'])
def dologin():
    if checklogin(request.form['customerID'],request.form['password']):
        session['logged_in'] = True
        return render_template('home.html')
    else:
        flash('wrong password!')
        return render_template('loginnew.html',message='Invalid Customer ID or Password!!!')
                
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()
 
# start the server using the run() method
if __name__ == "__main__":
     app.secret_key = "!mzo53678912489"
     app.run(debug=False,host='0.0.0.0')
     app.run()    
