import unittest
from unittest import mock

from src import fileutils


class TestFileUtils(unittest.TestCase):

    def setUp(self):
        self.file_utils = fileutils.FileUtils
        self.file_content = (
            "Nº: CM.Dv.00063.022 | A - 35 Título: Adriana Intérpretes: Adriana Data: 1970 | Volumes: 1 "
            "Nº: CM.Dv.00064.022 | A - 36 Título: Adriana Intérpretes: Adriana Data: 1986 | Volumes: 1 Observação: Em bom estado"
            "Nº: CM.Dv.00065.022 | A - 37 Título: Dom de Amar Intérpretes: Adriana Data: 1988 | Volumes: 1"
        )

    def test_get_filepath(self):
        filepath = self.file_utils.get_file_path("test/files/setup_test.ini")
        self.assertEqual("C:/Documents/aaa.txt", filepath)

    @mock.patch("src.fileutils.FileUtils.get_file_path", return_value="test/files/teste.txt")
    def test_get_file_content(self, mock_get_file_path):
        ini_path = "test/files/setup_test.ini"
        file_content = self.file_utils.get_file_content(ini_path)
        self.assertEqual("Arquivo de teste.", file_content.strip())
        mock_get_file_path.assert_called_once_with(ini_path)

    def test_get_numbers(self):
        expected = ["CM.Dv.00063.022 | A - 35", "CM.Dv.00064.022 | A - 36", "CM.Dv.00065.022 | A - 37"]
        numbers = self.file_utils.get_numbers(self.file_content)
        self.assertEqual(3, len(numbers))
        self.assertEqual(expected, numbers)

    def test_get_titles(self):
        expected = ["Adriana", "Adriana", "Dom de Amar"]
        titles = self.file_utils.get_titles(self.file_content)
        self.assertEqual(3, len(titles))
        self.assertEqual(expected, titles)

    def test_get_interpreters(self):
        expected = ["Adriana", "Adriana", "Adriana"]
        interpreters = self.file_utils.get_interpreters(self.file_content)
        self.assertEqual(3, len(interpreters))
        self.assertEqual(expected, interpreters)

    def test_get_dates(self):
        expected = ["1970", "1986", "1988"]
        dates = self.file_utils.get_dates(self.file_content)
        self.assertEqual(3, len(dates))
        self.assertEqual(expected, dates)

    def test_get_volumes_and_notes(self):
        expected_volumes = ["1", "1", "1"]
        expected_notes = ["", "Em bom estado", ""]
        volumes, notes = self.file_utils.get_volumes_and_notes(self.file_content)
        self.assertEqual(3, len(volumes))
        self.assertEqual(3, len(notes))
        self.assertEqual(expected_volumes, volumes)
        self.assertEqual(expected_notes, notes)

    @mock.patch("src.fileutils.FileUtils.get_file_path", return_value="test/files/teste2.txt")
    def test_get_file_content_as_tuple(self, mock_get_file_path):
        expected = (
            ("abc.123", "Let it Be", "The Beatles", "1969", "1", ""),
            ("dfg.456", "Gita", "Raul Seixas", "1974", "1", "Em bom estado"),
            ("hij.789", "The Beatles", "The Beatles", "1968", "2", ""),
        )
        ini_path = "./files/setup_test.ini"
        result = self.file_utils.get_file_content_as_tuple(ini_path)
        self.assertEqual(expected, result)
        mock_get_file_path.assert_called_once_with(ini_path)


