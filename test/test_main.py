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
        expected = ["Adriana", "Adriana", "Dom de Amar"]
        titles = main.get_titles(self.file_content)
        self.assertEqual(3, len(titles))
        self.assertEqual(expected, titles)

    def test_get_numbers(self):
        expected = ["CM.Dv.00063.022 | A - 35", "CM.Dv.00064.022 | A - 36", "CM.Dv.00065.022 | A - 37"]
        numbers = main.get_numbers(self.file_content)
        self.assertEqual(3, len(numbers))
        self.assertEqual(expected, numbers)

    def test_get_interpreters(self):
        expected = ["Adriana", "Adriana", "Adriana"]
        interpreters = main.get_interpreters(self.file_content)
        self.assertEqual(3, len(interpreters))
        self.assertEqual(expected, interpreters)

    def test_get_dates(self):
        expected = ["1970", "1986", "1988"]
        dates = main.get_dates(self.file_content)
        self.assertEqual(3, len(dates))
        self.assertEqual(expected, dates)

    def test_get_volumes(self):
        expected = ["1", "1", "1"]
        volumes = main.get_volumes(self.file_content)
        self.assertEqual(3, len(volumes))
