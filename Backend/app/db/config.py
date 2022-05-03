import psycopg2
from sqlalchemy import false

def conecta_db():
    con = psycopg2.connect(host='ec2-3-209-124-113.compute-1.amazonaws.com', 
                            database='dd9jdc6nipc3hh',
                            user='ojwyfpeihoevxu', 
                            password='e632432f03a787d335c96ab0920e7156d808d8cea213ad94f93c95ae838cbec3')
    return con

def desconecta():
    bd = conecta_db
    return bd.close()

def inserir_db(sql):
    con = conecta_db()
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

def consultar_db(sql):
    con = conecta_db()
    cur = con.cursor()
    cur.execute(sql)
    recset = cur.fetchall()
    registros = []
    for rec in recset:
        registros.append(rec)
    con.close()
    print(registros)
    return registros

print(consultar_db("SELECT * FROM USUARIO"))

