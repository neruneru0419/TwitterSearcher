import sqlite3

class AccountData():
    def __init__(self, dbname: str):
        self.dbname = dbname
        conn = sqlite3.connect(self.dbname)
        """
        c = conn.cursor()
        c.execute('''CREATE TABLE users(verifier text, token text, secret_token text)''')
        conn.commit()
        """
        conn.close()
    def insert_verifier(self, verifier: str, token: str, secret_token: str):
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        exist_token = self.select_token(token)
        if exist_token:
            sql = ("update users set verifier = ? where token = ?")
            data = (verifier, token)
            c.execute(sql, data)
        else:
            sql = ("insert into users values (?, ?, ?)")
            data = (verifier, token, secret_token)
            c.execute(sql, data)
        conn.commit()
        conn.close()
    def select_token(self, token: str) -> bool:
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        sql = ("select * from users where token=?")
        data = (token,)
        c.execute(sql, data)
        exist_token = bool(c.fetchone())
        conn.close()
        return exist_token
    def select_verifier(self, verifier: str) -> list:
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        sql = ("select * from users where verifier=?")
        data = (verifier,)
        c.execute(sql, data)
        datalist = c.fetchone()
        conn.close()
        return datalist
