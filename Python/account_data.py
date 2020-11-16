import psycopg2
import os


class AccountData():
    def __init__(self, dbname: str):
        self.dbname = dbname
        self.postgersql_password = os.getenv["password"]
        conn = psycopg2.connect(
            user=self.dbname, password=self.postgersql_password)
        c = conn.cursor()
        c.execute("create extension if not exists pgcrypto")
        c.execute("create table if not exists users (verifier text, token text, secret_token text)")
        conn.commit()
        conn.close()

    def insert_verifier(self, verifier: str, token: str, secret_token: str):
        conn = psycopg2.connect(
            user=self.dbname, password=self.postgersql_password)

        c = conn.cursor()
        exist_token = self.select_token(token)
        if exist_token:
            sql = (
                "update users set verifier = pgp_sym_encrypt(%s, 'my_pass') where token = pgp_sym_encrypt(%s, 'my_pass')")
            data = (verifier, token)
            c.execute(sql, data)
        else:
            sql = ("insert into users values (pgp_sym_encrypt(%s, 'my_pass'), pgp_sym_encrypt(%s, 'my_pass'), pgp_sym_encrypt(%s, 'my_pass'))")
            data = (verifier, token, secret_token)
            c.execute(sql, data)
        conn.commit()
        conn.close()

    def select_token(self, token: str) -> bool:
        conn = psycopg2.connect(
            user=self.dbname, password=self.postgersql_password)
        c = conn.cursor()
        sql = ("""select pgp_sym_decrypt(bytea(verifier), 'my_pass'), 
                pgp_sym_decrypt(bytea(token), 'my_pass'), 
                pgp_sym_decrypt(bytea(secret_token), 'my_pass') 
                from users where pgp_sym_decrypt(bytea(verifier), 'my_pass') = %s""")
        data = (token,)
        c.execute(sql, data)
        exist_token = bool(c.fetchone())
        conn.close()
        return exist_token

    def select_verifier(self, verifier: str) -> list:
        conn = psycopg2.connect(
            user=self.dbname, password=self.postgersql_password)
        c = conn.cursor()
        sql = ("""select pgp_sym_decrypt(bytea(verifier), 'my_pass'), 
                pgp_sym_decrypt(bytea(token), 'my_pass'), 
                pgp_sym_decrypt(bytea(secret_token), 'my_pass') 
                from users where pgp_sym_decrypt(bytea(verifier), 'my_pass') = %s""")
        data = (verifier,)
        c.execute(sql, data)
        datalist = c.fetchone()
        conn.close()
        return datalist
