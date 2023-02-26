import unittest
from unittest import mock

from src import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self._database = database.Database

    @mock.patch("src.database.Database._drop_table")
    @mock.patch("src.database.sqlite3.connect")
    def test_create_table(self, connect_mock, drop_table_mock):
        cursor_mock = connect_mock().cursor()
        cursor_mock.execute.return_value = [1]
        self._database.create_table()
        connect_mock.assert_called_with("../db/inventario.db")
        drop_table_mock.assert_called_once_with(cursor_mock)
        cursor_mock.execute.assert_called_once()

    @mock.patch("src.database.sqlite3.connect")
    def test_insert_inventory(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        executemany_mock = cursor_mock.executemany
        expected_stmt = (
            "insert into inventario (id, recorded_year, letter, letter_seq, title, interpreter, "
            "date, volume, note) values (?, ?, ?, ?, ?, ?, ?, ?, ?)")
        expected_data = [
            {
                "id": 1, "recorded_year": "22", "letter": "A", "letter_seq": 1, "title": "AAA", "interpreter": "AAA",
                "date": "1990", "volume": "1", "note": None},
            {
                "id": 2, "recorded_year": "22", "letter": "A", "letter_seq": 2, "title": "AAB", "interpreter": "AAB",
                "date": "1990", "volume": "1", "note": None},
        ]
        self._database.insert_inventory(expected_data)
        executemany_mock.assert_called_once_with(expected_stmt, expected_data)

    @mock.patch("src.database.sqlite3.connect")
    def test_update_inventory(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        executemany_mock = cursor_mock.executemany
        expected_stmt = ("update inventario SET letter = ?, letter_seq = ?, title = ?, interpreter = ?, "
                         "date = ?, volume = ?, note = ? "
                         "WHERE id = ?")
        expected_data = [
            {
                "recorded_year": "22", "letter": "A", "letter_seq": 1, "title": "AAB", "interpreter": "AAB",
                "date": "1990", "volume": "1", "note": None, "id": 1},
        ]
        self._database.update_inventory(expected_data)
        executemany_mock.assert_called_once_with(expected_stmt, expected_data)

    @mock.patch("src.database.sqlite3.connect")
    def test_read_inventory(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        expected_data = [
            {
                "id": 1, "recorded_year": "22", "letter": "A", "letter_seq": 1, "title": "AAA", "interpreter": "AAA",
                "date": "1990", "volume": "1", "note": None},
            {
                "id": 2, "recorded_year": "22", "letter": "A", "letter_seq": 2, "title": "AAB", "interpreter": "AAB",
                "date": "1990", "volume": "1", "note": None},
        ]
        execute_mock.return_value = (
            (1, "22", "A", 1, "AAA", "AAA", "1990", "1", None),
            (2, "22", "A", 2, "AAB", "AAB", "1990", "1", None),
        )
        expected_stmt = (
            "SELECT id, recorded_year, letter, letter_seq, title, interpreter, "
            "date, volume, note FROM inventario ORDER BY letter, letter_seq")
        obtained = self._database.read_inventory()
        self.assertEqual(obtained, expected_data)
        execute_mock.assert_called_once_with(expected_stmt)

    @mock.patch("src.database.sqlite3.connect")
    def test_fetch_when_note_is_none(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        expected_data = {
            "Nº": "1.22 | A - 1",
            "Título": "AAA",
            "Intérpretes": "AAA",
            "Data": "1990",
            "Volumes": "1",
        }
        execute_mock.return_value.fetchone.return_value = (1, "22", "A", 1, "AAA", "AAA", "1990", "1", None)
        expected_stmt = ("SELECT id, recorded_year, letter, letter_seq, title, interpreter, date, volume, note "
                         "FROM inventario WHERE id = :id")
        obtained = self._database.fetch(1)
        self.assertEqual(obtained, expected_data)
        execute_mock.assert_called_once_with(expected_stmt, {"id": 1})

    @mock.patch("src.database.sqlite3.connect")
    def test_fetch_when_note_is_not_none(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        expected_data = {
            "Nº": "1.22 | A - 1",
            "Título": "AAA",
            "Intérpretes": "AAA",
            "Data": "1990",
            "Volumes": "1",
            "Observação": "Em bom estado"
        }
        execute_mock.return_value.fetchone.return_value = (1, "22", "A", 1, "AAA", "AAA", "1990", "1", "Em bom estado")
        expected_stmt = ("SELECT id, recorded_year, letter, letter_seq, title, interpreter, date, volume, note "
                         "FROM inventario WHERE id = :id")
        obtained = self._database.fetch(1)
        self.assertEqual(obtained, expected_data)
        execute_mock.assert_called_once_with(expected_stmt, {"id": 1})

    @mock.patch("src.database.sqlite3.connect")
    def test_get_record_id_when_letter_seq_is_one_and_letter_is_numeric(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        obtained = self._database.get_record_id("#", 1)
        self.assertEqual(1, obtained)
        execute_mock.assert_not_called()

    @mock.patch("src.database.sqlite3.connect")
    def test_get_record_id_when_letter_seq_is_one_and_letter_is_not_numeric(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        expected_stmt = "SELECT max(id) FROM inventario WHERE letter = :letter"
        execute_mock.return_value.fetchone.return_value = (17,)
        obtained = self._database.get_record_id("A", 1)
        self.assertEqual(18, obtained)
        execute_mock.assert_called_with(expected_stmt, {"letter": "#"})

    @mock.patch("src.database.sqlite3.connect")
    def test_get_record_id_when_letter_seq_is_not_one_and_letter_is_not_numeric(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        expected_stmt = "SELECT max(id) FROM inventario WHERE letter = :letter"
        execute_mock.return_value.fetchone.return_value = (44,)
        obtained = self._database.get_record_id("B", 8)
        self.assertEqual(45, obtained)
        execute_mock.assert_called_once_with(expected_stmt, {"letter": "B"})

    @mock.patch("src.database.sqlite3.connect")
    def test_get_last_letter_seq(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        expected_stmt = "SELECT max(letter_seq) FROM inventario WHERE letter = :letter"
        execute_mock.return_value.fetchone.return_value = (1,)
        obtained = self._database.get_last_letter_seq("A")
        self.assertEqual(1, obtained)
        execute_mock.assert_called_once_with(expected_stmt, {"letter": "A"})

    @mock.patch("src.database.sqlite3.connect")
    def test_normalize_sequence(self, connect_mock):
        cursor_mock = connect_mock().cursor()
        execute_mock = cursor_mock.execute
        expected_stmt = (
            "UPDATE inventario "
            "SET letter_seq = letter_seq + 1 "
            "WHERE letter = :letter AND letter_seq >= :letter_seq ")
        self._database.normalize_sequence("B", 2)
        execute_mock.assert_called_once_with(expected_stmt, {"letter": "B", "letter_seq": 2})
