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
