import configparser
import re


class FileUtils:

    @staticmethod
    def get_file_path(ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)
        return config.get('filepath', 'path')

    @staticmethod
    def get_file_content(ini_file):
        filepath = FileUtils.get_file_path(ini_file)
        with open(filepath, 'r') as file:
            return " ".join(file.readlines())

    @staticmethod
    def get_numbers(filecontent):
        numbers = re.findall(r"Nº:(.*?)Título", filecontent)
        return FileUtils._apply_strip(numbers)

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
    def get_volumes(filecontent):
        volumes = re.findall(r"Volumes:(.*?)Nº:", filecontent)
        last_volume = re.split(r"Volumes:", filecontent)[-1]
        volumes.append(last_volume)
        return FileUtils._apply_strip(volumes)

    @staticmethod
    def get_file_content_as_tuple(ini_path):
        filecontent = FileUtils.get_file_content(ini_path)
        flat_filecontent = filecontent.replace('\n', ' ').replace(u'\xa0', u' ')
        numbers = FileUtils.get_numbers(flat_filecontent)
        titles = FileUtils.get_titles(flat_filecontent)
        interpreters = FileUtils.get_interpreters(flat_filecontent)
        dates = FileUtils.get_dates(flat_filecontent)
        volumes = FileUtils.get_volumes(flat_filecontent)
        if len(numbers) != len(titles) != len(interpreters) != len(dates) != len(volumes):
            raise Exception("Erro ao ler arquivo. A quantidade de dados está inconsistente")
        return zip(numbers, titles, interpreters, dates, volumes)

    @staticmethod
    def _apply_strip(items):
        return list(map(str.strip, items))
