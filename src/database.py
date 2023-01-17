import sqlite3


class Database:

    @staticmethod
    def create_table():
        con = sqlite3.connect("../db/inventario.db")
        cur = con.cursor()
        cur.execute("DROP TABLE inventario")
        cur.execute("CREATE TABLE inventario(number, title, interpreter, date, volume)")
        cur.close()
        con.close()

    @staticmethod
    def insert_inventory(data):
        conn = sqlite3.connect("../db/inventario.db")
        stmt = "insert into inventario (number, title, interpreter, date, volume) values (?, ?, ?, ?, ?)"

        cur = conn.cursor()
        vals = data
        cur.executemany(stmt, vals)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def read_inventory():
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        for row in cur.execute("SELECT number, title, interpreter, date, volume FROM inventario ORDER BY number"):
            print(row)
