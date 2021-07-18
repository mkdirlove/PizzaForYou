import sqlite3 as sql

from functools import wraps
from flask import session,flash,redirect,url_for

connect_db ='pizza.db'

def productList():
  with sql.connect(connect_db) as db:
    qry = 'select * from PRODUCT' 
    result = db.execute(qry)
    return(result)

def customerList():
  with sql.connect(connect_db) as db:
    qry = 'select * from CUSTOMER' 
    result = db.execute(qry)
    return(result)

def sellerList():
  with sql.connect(connect_db) as db:
    qry = 'select * from SELLER' 
    result = db.execute(qry)
    return(result)

def orders():
  with sql.connect(connect_db) as db:
    qry = 'select History.orderNo, PRODUCT.Product_Description, PRODUCT.Unit_Price, History.quantity, History.totalPrice, History.placedDate, SELLER.Shop_Name from PRODUCT, History, SELLER where PRODUCT.Product_No = History.Product_No and PRODUCT.Product_No = SELLER.Product_No'
    result = db.execute(qry)
    return(result)

def check_custID(customerID):
  with sql.connect(connect_db) as db: 
    qry = 'select customerID,password from CUSTOMER where customerID=?'
    result=db.execute(qry,(customerID,)).fetchone()
    return(result)

def insert_customer(customerID,name,address,city,state,phone,password):
  with sql.connect(connect_db) as db:
    qry='insert into CUSTOMER (customerID,name,address,city,state,phone,password) values (?,?,?,?,?,?,?)' 
    db.execute(qry,(customerID,name,address,city,state,phone,password))
    
def update_customer(name,address,city,state,phone,password,customerID):
  with sql.connect(connect_db) as db:
    qry='update CUSTOMER set name=?,address=?,city=?,state=?,phone=?,password=? where customerID=?' 
    db.execute(qry, (name,address,city,state,phone,password,customerID))
    
def find_customer(customerID):
  with sql.connect(connect_db) as db:
    qry = 'select * from CUSTOMER where customerID=?'
    result=db.execute(qry,(customerID,)).fetchone()
    return(result)

def delete_customer(customerID):
  with sql.connect(connect_db) as db:
    qry='delete from CUSTOMER where customerID=?' 
    db.execute(qry,(customerID,))
    
def delete_order(orderNo):
  with sql.connect(connect_db) as db:
    qry='delete from History where orderNo=?' 
    db.execute(qry,(orderNo,))
    
def insert_order(Product_No,quantity,totalPrice,placedDate):
  with sql.connect(connect_db) as db:
    qry='insert into History (Product_No,quantity,totalPrice,placedDate) values (?,?,?,?)' 
    db.execute(qry,(Product_No,quantity,totalPrice,placedDate))

def checklogin(customerID,password):
  with sql.connect(connect_db) as db: 
    qry = 'select customerID,password from CUSTOMER where customerID=? and password=?'
    result=db.execute(qry,(customerID,password)).fetchone()
    return(result)

def result():
  #rows=productList()
  #rows=customerList()
  rows=sellerList()
  rows=orderList()  
  for row in rows:
      print (row)   
