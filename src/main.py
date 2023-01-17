import configparser
import re
import sys

INI_PATH = "../setup.ini"
PRINT = 1
ADD = 2
CREATE_DATABASE = 3
EXIT = 4


def main():
    print("Olá! Escolha uma das opções:\n")
    received_input = 0
    while received_input != EXIT:
        try:
            received_input = int(input("1-Ler arquivo\n2-Adicionar entrada\n3-Criar banco de dados\n4-Sair\n"))
        except ValueError:
            print("opção inválida.\n")
            continue
        if received_input not in (PRINT, ADD, CREATE_DATABASE, EXIT):
            print("opção inválida.\n")
        if received_input == EXIT:
            sys.exit(0)
        if received_input == PRINT:
            filepath = get_file_path(INI_PATH)
            print(get_file_content(filepath))
            continue
        if received_input == ADD:
            print("em construção")
            continue
        if received_input == CREATE_DATABASE:
            create_database()
            return


def create_database():
    filepath = get_file_path(INI_PATH)
    filecontent = get_file_content(filepath)
    flat_filecontent = filecontent.replace('\n', ' ').replace(u'\xa0', u' ')
    numbers = get_numbers(flat_filecontent)
    titles = get_titles(flat_filecontent)
    interpreters = get_interpreters(flat_filecontent)
    dates = get_dates(flat_filecontent)
    volumes = get_volumes(flat_filecontent)
    assert len(numbers) == len(titles) == len(interpreters) == len(dates) == len(volumes)
    all = zip(numbers, titles, interpreters, dates, volumes)
    tuple(all)


def get_numbers(filecontent):
    numbers = re.findall(r"Nº:(.*?)Título", filecontent)
    return apply_strip(numbers)


def get_titles(filecontent):
    titles = re.findall(r"Título:(.*?)Intérpr", filecontent)
    alt_title = re.findall(r"Título :(.*?)Intérpr", filecontent)
    if alt_title:
        titles.append(alt_title)
    return apply_strip(titles)


def get_interpreters(filecontent):
    interpreters = re.findall(r"Intérpretes:(.*?)Data", filecontent)
    alt_interpreters = re.findall(r"Intérpretes :(.*?)Data", filecontent)
    if alt_interpreters:
        interpreters.append(alt_interpreters)
    return apply_strip(interpreters)


def get_dates(filecontent):
    dates = re.findall(r"Data:(.*?)\| Volumes", filecontent)
    return apply_strip(dates)


def get_volumes(filecontent):
    volumes = re.findall(r"Volumes:(.*?)Nº:", filecontent)
    last_volume = re.split(r"Volumes:", filecontent)[-1]
    volumes.append(last_volume)
    return apply_strip(volumes)


def get_file_content(filepath):
    with open(filepath, 'r') as file:
        return " ".join(file.readlines())


def get_file_path(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)
    return config.get('filepath', 'path')


def apply_strip(items):
    return list(map(str.strip, items))


if __name__ == '__main__':
    main()
