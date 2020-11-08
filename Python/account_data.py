import psycopg2
import os

class AccountData():
    def __init__(self, dbname: str):
        self.dbname = dbname
        conn = psycopg2.connect(user="postgres", password=os.getenv("postgersql_password"))
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE if not exists users (verifier text, token text, secret_token text)''')
        conn.commit()
        conn.close()

    def insert_verifier(self, verifier: str, token: str, secret_token: str):
        conn = psycopg2.connect(user="postgres", password=os.getenv("postgersql_password"))
        c = conn.cursor()
        exist_token = self.select_token(token)
        if exist_token:
            sql = ("update users set verifier = %s where token = %s")
            data = (verifier, token)
            c.execute(sql, data)
        else:
            sql = ("insert into users values (%s, %s, %s)")
            data = (verifier, token, secret_token)
            c.execute(sql, data)
        conn.commit()
        conn.close()

    def select_token(self, token: str) -> bool:
        conn = psycopg2.connect(user="postgres", password=os.getenv("postgersql_password"))
        c = conn.cursor()
        sql = ("select * from users where token = %s")
        data = (token,)
        c.execute(sql, data)
        exist_token = bool(c.fetchone())
        conn.close()
        return exist_token

    def select_verifier(self, verifier: str) -> list:
        conn = psycopg2.connect(user="postgres", password=os.getenv("postgersql_password"))
        c = conn.cursor()
        sql = ("select * from users where verifier = %s")
        data = (verifier,)
        c.execute(sql, data)
        datalist = c.fetchone()
        conn.close()
        return datalist
