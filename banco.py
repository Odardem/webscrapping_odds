from time import sleep
import json
import pyodbc
from connections import *
import psycopg2

def conecta_db():
  con = pyodbc.connect(URL_CONEXAO_BANCO)
  return con

def conecta_dblocal():
  con = psycopg2.connect(URL_CONEXAO_BANCO_LOCAL)
  return con

def criar_db(sql):
  con = conecta_db()
  cur = con.cursor()
  cur.execute(sql)
  con.commit()
  con.close()

def inserir_db(sql):
  con = conecta_db()
  cur = con.cursor()
  #users = check_table_users() 
  try:
    cur.execute(sql)
    con.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print("Error: %s" % error)
    con.rollback()
    cur.close()
    return 1
  cur.close()

def deletar_tabela(tabela):
  sql = f'DROP TABLE IF EXISTS {tabela}'
  inserir_db(sql)

  
if __name__ == '__main__':

  cursor = conecta_db()
  teste =  cursor.execute('SELECT top 100 * FROM ligas')
  rows = teste.fetchall()  
  print(rows)
