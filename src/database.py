import sqlite3


class Database:

    @staticmethod
    def create_table():
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        Database._drop_table(cur)
        cur.execute("CREATE TABLE inventario(id, recorded_year, letter, letter_seq, title, "
                    "interpreter, date, volume, note)")
        cur.close()
        conn.close()

    @staticmethod
    def insert_inventory(data):
        conn = sqlite3.connect("../db/inventario.db")
        stmt = ("insert into inventario (id, recorded_year, letter, letter_seq, title, interpreter, "
                "date, volume, note) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?)")
        cur = conn.cursor()
        cur.executemany(stmt, data)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def read_inventory():
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        stmt = ("SELECT id, recorded_year, letter, letter_seq, title, interpreter, "
                "date, volume, note "
                "FROM inventario ORDER BY id")
        try:
            for row in cur.execute(stmt):
                print(row)
        except sqlite3.OperationalError:
            print("O banco de dados ainda não está criado. Favor criar o banco de dados")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def fetch(record_id):
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        res = cur.execute("SELECT id, recorded_year, letter, letter_seq, title, interpreter, date, volume, note "
                          "FROM inventario WHERE id = :id", {"id": record_id})
        res = res.fetchone()
        if not res:
            return f"Nenhum registro encontrado pelo número {record_id}."
        result = {
            "Nº": f"{res[0]}.{res[1]} | {res[2]} - {res[3]}",
            "Título": res[4],
            "Intérpretes": res[5],
            "Data": res[6],
            "Volumes": res[7],
        }
        if res[5]:
            result["Observação"] = res[8]
        cur.close()
        conn.close()

        return result

    @staticmethod
    def get_last_id():
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        stmt = "SELECT max(id) FROM inventario"
        try:
            res = cur.execute(stmt)
            res = res.fetchone()
            if len(res):
                return res[0]
            return 1
        except sqlite3.OperationalError:
            print("O banco de dados ainda não está criado. Favor criar o banco de dados")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_last_letter_seq(letter):
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        stmt = "SELECT max(letter_seq) FROM inventario WHERE letter = :letter"
        try:
            res = cur.execute(stmt, {"letter": letter})
            res = res.fetchone()
            if len(res):
                return res[0]
            return 1
        except sqlite3.OperationalError:
            print("O banco de dados ainda não está criado. Favor criar o banco de dados")
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def _drop_table(cursor):
        res = cursor.execute("SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='inventario')")
        table_exists = res.fetchone()[0]
        if table_exists:
            cursor.execute("DROP TABLE inventario")
