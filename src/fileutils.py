import configparser
from datetime import datetime
import re

import jinja2
import pdfkit

import src.static as static


class FileUtils:

    @staticmethod
    def get_file_path(ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)
        return config.get('filepath', 'path')

    @staticmethod
    def get_file_content(ini_file):
        filepath = FileUtils.get_file_path(ini_file)
        with open(filepath, 'r', encoding=static.ENCODING) as file:
            return " ".join(file.readlines())

    @staticmethod
    def get_numbers(filecontent):
        ids = []
        recorded_years = []
        letters = []
        letter_seqs = []
        numbers = re.findall(r"Nº: CM\.Dv\.(.*?)Título", filecontent)
        for number in numbers:
            splitted = number.split("|")
            id_part = splitted[0]
            letter_part = splitted[1]
            FileUtils._set_ids(id_part, ids)
            FileUtils._set_recorded_years(id_part, recorded_years)
            FileUtils._set_letters(letter_part, letters)
            FileUtils._set_letter_seqs(letter_part, letter_seqs)
        return ids, recorded_years, letters, letter_seqs

    @staticmethod
    def _set_ids(id_part, ids):
        id_splitted = id_part.split(".")
        inventory_id = id_splitted[0].strip().lstrip("0")
        ids.append(int(inventory_id))

    @staticmethod
    def _set_recorded_years(id_part, recorded_years):
        id_splitted = id_part.split(".")
        recorded_year = id_splitted[1].strip().lstrip("0")
        recorded_years.append(recorded_year)

    @staticmethod
    def _set_letters(letter_part, letters):
        letter_splitted = letter_part.split("-")
        letter = letter_splitted[0].strip()
        letters.append(letter)

    @staticmethod
    def _set_letter_seqs(letter_part, letter_seqs):
        letter_splitted = letter_part.split("-")
        letter_seq = letter_splitted[1].strip()
        letter_seqs.append(int(letter_seq))

    @staticmethod
    def get_titles(filecontent):
        titles = re.findall(r"Título:(.*?)Intérpr", filecontent)
        alt_title = re.findall(r"Título :(.*?)Intérpr", filecontent)
        if alt_title:
            titles.append(alt_title)
        return FileUtils._apply_strip(titles)

    @staticmethod
    def get_interpreters(filecontent):
        interpreters = re.findall(r"Intérpretes:(.*?)Data", filecontent)
        alt_interpreters = re.findall(r"Intérpretes :(.*?)Data", filecontent)
        if alt_interpreters:
            interpreters.append(alt_interpreters)
        return FileUtils._apply_strip(interpreters)

    @staticmethod
    def get_dates(filecontent):
        dates = re.findall(r"Data:(.*?)\| Volumes", filecontent)
        return FileUtils._apply_strip(dates)

    @staticmethod
    def get_volumes_and_notes(filecontent):
        notes = []
        cleaned_volumes = []
        volumes = re.findall(r"Volumes:(.*?)Nº:", filecontent)
        last_volume = re.split(r"Volumes:", filecontent)[-1]
        volumes.append(last_volume)
        for value in volumes:
            splitted_volume = value.split("Observação:")
            cleaned_volumes.append(splitted_volume[0])
            if len(splitted_volume) > 1:
                note = splitted_volume[1]
            else:
                note = ""
            notes.append(note)
        cleaned_volumes = FileUtils._apply_strip(cleaned_volumes)
        notes = FileUtils._apply_strip(notes)
        return cleaned_volumes, notes

    @staticmethod
    def get_file_content_as_tuple(ini_path):
        filecontent = FileUtils.get_file_content(ini_path)
        flat_filecontent = filecontent.replace('\n', ' ')
        ids, recorded_years, letters, letter_seqs = FileUtils.get_numbers(flat_filecontent)
        titles = FileUtils.get_titles(flat_filecontent)
        interpreters = FileUtils.get_interpreters(flat_filecontent)
        dates = FileUtils.get_dates(flat_filecontent)
        volumes, notes = FileUtils.get_volumes_and_notes(flat_filecontent)
        if (len(ids) != len(recorded_years) != len(letters)
                != len(letter_seqs) != len(titles) != len(interpreters)
                != len(dates) != len(volumes) != len(notes)):
            raise Exception("Erro ao ler arquivo. A quantidade de dados está inconsistente")
        return tuple(zip(ids, recorded_years, letters, letter_seqs, titles, interpreters, dates, volumes, notes))

    @staticmethod
    def get_first_letter(interpreter):
        first_letter = interpreter[0]
        if interpreter.startswith("The "):
            first_letter = interpreter[4]
        if interpreter.startswith("O ") or interpreter.startswith("A "):
            first_letter = interpreter[2]
        if interpreter.startswith("Os ") or interpreter.startswith("As "):
            first_letter = interpreter[3]
        if first_letter.isdigit():
            return "#"
        return first_letter

    @staticmethod
    def write_txt(inventory, filedir):
        if not filedir.endswith("/"):
            filedir = filedir + "/"
        filepath = FileUtils._get_filepath(filedir, "txt")
        with open(filepath, "w", encoding=static.ENCODING) as output:
            for data in inventory:
                id_zfilled = str(data["id"]).zfill(5)
                year_zfilled = data["recorded_year"].zfill(3)
                number = f"CM.Dv.{id_zfilled}.{year_zfilled} | {data['letter']} - {data['letter_seq']}"
                output.write(f"Nº: {number}\n")
                output.write(f"Título: {data['title']}\n")
                output.write(f"Intérpretes: {data['interpreter']}\n")
                output.write(f"Data: {data['date']} | Volumes: {data['volume']}")
                note = data["note"]
                if note:
                    output.write(f"\nObservação: {note}")
                output.write("\n\n")

    @staticmethod
    def write_pdf(inventory, filedir):
        if not filedir.endswith("/"):
            filedir = filedir + "/"
        filepath = FileUtils._get_filepath(filedir, "pdf")
        template_loader = jinja2.FileSystemLoader("../files/")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("template_pdf.html")
        context = {"volumes_numerais": [i for i in inventory if i["letter"] == "#"]}
        for letter in static.ALPHABET:
            context_key = f"volumes_{letter.lower()}"
            context[context_key] = [i for i in inventory if i["letter"] == letter]
        output_text = template.render(context)
        wkhtmltopdf_path = FileUtils._get_wkhtmltopdf_path("../setup.ini")
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_string(output_text, filepath, configuration=config)

    @staticmethod
    def _get_wkhtmltopdf_path(ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)
        return config.get('filepath', 'wkhtmltopdf_path')

    @staticmethod
    def _get_filepath(filedir, format):
        cur_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{filedir}inventario_{cur_datetime}.{format}"

    @staticmethod
    def _apply_strip(items):
        return list(map(str.strip, items))
