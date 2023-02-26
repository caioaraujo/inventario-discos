import sqlite3

import src.static as static


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
    def get_record_id(letter, letter_seq):
        """
        Get the current id

        :param letter: Record letter
        :param letter_seq: Sequence in this letter
        :return: int
        """
        if letter_seq == 1:
            if letter == "#":
                return 1
            letter = Database._get_previous_letter(letter)
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        stmt = "SELECT max(id) FROM inventario WHERE letter = :letter"
        try:
            res = cur.execute(stmt, {"letter": letter})
            res = res.fetchone()
            if res[0]:
                return res[0] + 1
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
    def normalize_sequence(letter, letter_seq):
        """
        Increment all records after the given letter_seq in given letter.

        :param letter: Interpreter letter
        :param letter_seq: Current sequential. All sequentials after this number will be incremented.
        :return: None
        """
        conn = sqlite3.connect("../db/inventario.db")
        cur = conn.cursor()
        stmt = ("UPDATE inventario "
                "SET letter_seq = letter_seq + 1 "
                "WHERE letter = :letter AND letter_seq >= :letter_seq ")
        cur.execute(stmt, {"letter": letter, "letter_seq": letter_seq})
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def _get_previous_letter(letter):
        if letter == "A":
            return "#"
        all_letters = static.ALPHABET
        cur_letter_index = all_letters.index(letter)
        previous_letter = all_letters[cur_letter_index-1]
        return previous_letter

    @staticmethod
    def _drop_table(cursor):
        res = cursor.execute("SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='inventario')")
        table_exists = res.fetchone()[0]
        if table_exists:
            cursor.execute("DROP TABLE inventario")
