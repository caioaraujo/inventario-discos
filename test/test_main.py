import unittest

from src import main


class TestMain(unittest.TestCase):

    def test_get_filepath(self):
        filepath = main.get_file_path("./files/setup_test.ini")
        self.assertEqual("C:/Documents/aaa.pdf", filepath)
