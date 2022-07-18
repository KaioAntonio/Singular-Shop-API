import psycopg2
import os

USER = "inixdviasnbjiz"
KEY = "7d3b08f9f3321c6db320a9aaf409268500f66269cbe9a19bde6c8d8664727679"

def connect_db():
    con = psycopg2.connect(host='ec2-52-5-110-35.compute-1.amazonaws.com', 
                            database='d27fpf0b9mc5lk',
                            user= os.getenv(USER,"inixdviasnbjiz" ),
                            password= os.getenv(KEY, "7d3b08f9f3321c6db320a9aaf409268500f66269cbe9a19bde6c8d8664727679"))
    return con

def disconnect():
    bd = connect_db()
    return bd.close()

def insert_db(sql):
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        con.rollback()
        cur.close()
        return False
    cur.close()

def read_db(sql):
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    list_users = []
    for rec in recset:
        requireds = {"user_id": rec[0], "username": rec[1], "password": rec[2], "email": rec[3], "admin": rec[4], "avatar": rec[5]}
        list_users.append(requireds)
    return list_users

def read_db_user_necessary(sql): #get user information necessary for autentication token
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    for rec in recset:
        requireds = {"username": rec[0], "email": rec[1], "admin": rec[2], "avatar": rec[3]}
    return requireds

def read_db_product(sql):
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    list_products = []
    for rec in recset:
        requireds = {"cod_product": rec[0], "name_product": rec[1], "description": rec[2], "price": rec[3], "image": rec[4]}
        list_products.append(requireds)
    return list_products

def read_password(sql):
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    return recset
                
def read_db_section(sql):
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    list_products = []
    for rec in recset:
        requireds = {"id_section": rec[0], "name_section": rec[1], "products_id": rec[2]}
        list_products.append(requireds)
    return list_products

def read_db_section_products(sql):
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    list_products = []
    for rec in recset:
        requireds = {"products_id": rec[0]}
        list_products.append(requireds)
    return list_products[0]

def read_db_cart(sql):
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    list_products = []
    for rec in recset:
        requireds = {"id_cart": rec[0], "products_cart": rec[1]}
        list_products.append(requireds)
    return list_products[0]