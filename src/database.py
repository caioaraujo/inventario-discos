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
    def update_inventory(data):
        conn = sqlite3.connect("../db/inventario.db")
        stmt = ("update inventario SET letter = ?, letter_seq = ?, title = ?, interpreter = ?, "
                "date = ?, volume = ?, note = ? "
                "WHERE id = ?")
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
                "FROM inventario ORDER BY letter, letter_seq")
        inventory = []
        try:
            for row in cur.execute(stmt):
                inventory.append(
                    {"id": row[0], "recorded_year": row[1], "letter": row[2],
                     "letter_seq": row[3], "title": row[4], "interpreter": row[5],
                     "date": row[6], "volume": row[7], "note": row[8]
                     })
            return inventory
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
            cur.close()
            conn.close()
            return None
        result = {
            "Nº": f"{res[0]}.{res[1]} | {res[2]} - {res[3]}",
            "Título": res[4],
            "Intérpretes": res[5],
            "Data": res[6],
            "Volumes": res[7],
        }
        if res[8]:
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
    def normalize_sequence(letter):
        """
        Update all records in given letter, sorted by interpreter and date.

        :param letter: Interpreter letter
        :return: None
        """
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        stmt = "SELECT id, interpreter, date FROM inventario WHERE letter = :letter"
        res = cur.execute(stmt, {"letter": letter})
        all_records = res.fetchall()
        if len(all_records) == 1:
            cur.close()
            conn.close()
            return
        sorted_records = []
        Database._get_cleaned_interpreter_list(all_records, sorted_records)
        Database._get_sorted_interpreter_list(sorted_records)
        Database._update_inventory_in_alphabetical_order(conn, sorted_records)
        cur.close()
        conn.close()

    @staticmethod
    def _update_inventory_in_alphabetical_order(conn, data):
        cur = conn.cursor()
        stmt = "UPDATE inventario SET letter_seq = ? WHERE id = ?"
        cur.executemany(stmt, data)
        conn.commit()
        cur.close()

    @staticmethod
    def _get_sorted_interpreter_list(cleaned_list):
        cleaned_list.sort(key=lambda a: (a[1], a[2]))
        record_index = 1
        for list_index, sorted_record in enumerate(cleaned_list):
            cleaned_list[list_index] = (record_index, sorted_record[0])
            record_index += 1

    @staticmethod
    def _get_cleaned_interpreter_list(raw_interpreter_list, cleaned_list):
        for record in raw_interpreter_list:
            record_id = record[0]
            interpreter = Database._clean_interpreter(record[1])
            date = record[2]
            cleaned_list.append((record_id, interpreter, date))

    @staticmethod
    def _clean_interpreter(interpreter):
        if interpreter.startswith("The "):
            return interpreter[4:]
        if interpreter.startswith("O ") or interpreter.startswith("A "):
            return interpreter[2:]
        if interpreter.startswith("Os ") or interpreter.startswith("As "):
            return interpreter[3:]
        return interpreter

    @staticmethod
    def _drop_table(cursor):
        res = cursor.execute("SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='inventario')")
        table_exists = res.fetchone()[0]
        if table_exists:
            cursor.execute("DROP TABLE inventario")
