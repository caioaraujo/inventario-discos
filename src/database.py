import sqlite3


class Database:

    @staticmethod
    def create_table():
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        Database._drop_table(cur)
        cur.execute("CREATE TABLE inventario(number, title, interpreter, date, volume)")
        cur.close()
        conn.close()

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
        try:
            for row in cur.execute("SELECT number, title, interpreter, date, volume FROM inventario ORDER BY number"):
                print(row)
        except sqlite3.OperationalError:
            print("O banco de dados ainda não está criado. Favor criar o banco de dados")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def fetch(numero):
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        res = cur.execute("SELECT * FROM inventario WHERE number = :numero", {"numero": numero})
        res = res.fetchone()
        if not res:
            return f"Nenhum registro encontrado pelo número {numero}."
        result = {
            "Nº": res[0],
            "Título": res[1],
            "Intérpretes": res[2],
            "Data": res[3],
            "Volumes": res[4]
        }
        cur.close()
        conn.close()

        return result

    @staticmethod
    def _drop_table(cursor):
        res = cursor.execute("SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='inventario')")
        table_exists = res.fetchone()[0]
        if table_exists:
            cursor.execute("DROP TABLE inventario")
