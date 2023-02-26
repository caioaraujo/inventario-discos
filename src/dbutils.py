

import sqlite3

class DBUtils:
    @staticmethod
    def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
        data = {}
        for idx, col in enumerate(cursor.description):
            data[col[0]] = row[idx]
        return data

