import unittest
from unittest import mock
from unittest.mock import mock_open

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
        expected_ids = [63, 64, 65]
        expected_recorded_years = ["22", "22", "22"]
        expected_letters = ["A", "A", "A"]
        expected_letter_seqs = [35, 36, 37]
        ids, recorded_years, letters, letter_seqs = self.file_utils.get_numbers(self.file_content)
        self.assertEqual(3, len(expected_ids))
        self.assertEqual(3, len(expected_recorded_years))
        self.assertEqual(3, len(expected_letters))
        self.assertEqual(3, len(expected_letter_seqs))
        self.assertEqual(expected_ids, ids)
        self.assertEqual(expected_recorded_years, recorded_years)
        self.assertEqual(expected_letters, letters)
        self.assertEqual(expected_recorded_years, recorded_years)
        self.assertEqual(expected_letter_seqs, letter_seqs)

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
            (1, "22", "B", 1, "Let it Be", "The Beatles", "1969", "1", ""),
            (2, "22", "R", 1, "Gita", "Raul Seixas", "1974", "1", "Em bom estado"),
            (3, "22", "B", 2, "The Beatles", "The Beatles", "1968", "2", ""),
        )
        ini_path = "./files/setup_test.ini"
        result = self.file_utils.get_file_content_as_tuple(ini_path)
        self.assertEqual(expected, result)
        mock_get_file_path.assert_called_once_with(ini_path)

    def test_get_first_letter(self):
        interpreter_with_number = "14 Bis"
        letter = self.file_utils.get_first_letter(interpreter_with_number)
        self.assertEqual("#", letter)
        interpreter_with_number_and_article = "Os 10 Mandamentos"
        letter = self.file_utils.get_first_letter(interpreter_with_number_and_article)
        self.assertEqual("#", letter)
        interpreter_with_the = "The Beatles"
        letter = self.file_utils.get_first_letter(interpreter_with_the)
        self.assertEqual("B", letter)
        interpreter_with_o = "O Terço"
        letter = self.file_utils.get_first_letter(interpreter_with_o)
        self.assertEqual("T", letter)
        interpreter_with_a = "A Melhor Banda do Mundo"
        letter = self.file_utils.get_first_letter(interpreter_with_a)
        self.assertEqual("M", letter)
        interpreter_with_os = "Os Paralamas do Sucesso"
        letter = self.file_utils.get_first_letter(interpreter_with_os)
        self.assertEqual("P", letter)
        interpreter_with_as = "As Panteras"
        letter = self.file_utils.get_first_letter(interpreter_with_as)
        self.assertEqual("P", letter)
        interpreter_without_prefix = "Raul Seixas"
        letter = self.file_utils.get_first_letter(interpreter_without_prefix)
        self.assertEqual("R", letter)

    @mock.patch("src.fileutils.FileUtils._get_filepath")
    def test_write_txt(self, mock_get_file_path):
        fakefile = "test/files/inventario.txt"
        mock_get_file_path.return_value = fakefile
        filedir = "test/files/"
        inventory = [
            {
                "id": 1, "recorded_year": "22", "letter": "A", "letter_seq": 1, "title": "AAA", "interpreter": "AAA",
                "date": "1990", "volume": "1", "note": None},
            {
                "id": 2, "recorded_year": "22", "letter": "A", "letter_seq": 2, "title": "AAB", "interpreter": "AAB",
                "date": "1990", "volume": "1", "note": "Muito bom"},
        ]
        expected_calls = [
            mock.call("Nº: CM.Dv.00001.022 | A - 1\n"),
            mock.call("Título: AAA\n"),
            mock.call("Intérpretes: AAA\n"),
            mock.call("Data: 1990 | Volumes: 1"),
            mock.call("\n\n"),
            mock.call("Nº: CM.Dv.00002.022 | A - 2\n"),
            mock.call("Título: AAB\n"),
            mock.call("Intérpretes: AAB\n"),
            mock.call("Data: 1990 | Volumes: 1"),
            mock.call("\nObservação: Muito bom"),
            mock.call("\n\n")
        ]
        with mock.patch('builtins.open', mock_open()) as mocked_file:
            self.file_utils.write_txt(inventory, filedir)
            mocked_file.assert_called_once_with(fakefile, 'w', encoding='utf-8')
            mocked_file().write.assert_has_calls(expected_calls)
            mock_get_file_path.assert_called_once_with(filedir, "txt")
