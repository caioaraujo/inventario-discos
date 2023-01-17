import unittest

from src import main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.file_content = (
            "Nº: CM.Dv.00063.022 | A - 35 Título: Adriana Intérpretes: Adriana Data: 1970 | Volumes: 1 "
            "Nº: CM.Dv.00064.022 | A - 36 Título: Adriana Intérpretes: Adriana Data: 1986 | Volumes: 1 "
            "Nº: CM.Dv.00065.022 | A - 37 Título: Dom de Amar Intérpretes: Adriana Data: 1988 | Volumes: 1"
        )

    def test_get_filepath(self):
        filepath = main.get_file_path("./files/setup_test.ini")
        self.assertEqual("C:/Documents/aaa.txt", filepath)

    def test_get_file_content(self):
        file_content = main.get_file_content("./files/teste.txt")
        self.assertEqual("Arquivo de teste.", file_content.strip())

    def test_get_titles(self):
        titles = main.get_titles(self.file_content)
        self.assertEqual(3, len(titles))

    def test_get_numbers(self):
        numbers = main.get_numbers(self.file_content)
        self.assertEqual(3, len(numbers))

    def test_get_interpreters(self):
        interpreters = main.get_numbers(self.file_content)
        self.assertEqual(3, len(interpreters))

    def test_get_dates(self):
        dates = main.get_dates(self.file_content)
        self.assertEqual(3, len(dates))

    def test_get_volumes(self):
        volumes = main.get_volumes(self.file_content)
        self.assertEqual(3, len(volumes))
