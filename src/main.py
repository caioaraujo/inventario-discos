import re
import sys

from database import Database
from fileutils import FileUtils

INI_PATH = "../setup.ini"
PRINT_FILE = 1
ADD = 2
CREATE_DATABASE = 3
READ_TABLE = 4
EXIT = 5


def main():
    print("Olá! Escolha uma das opções:\n")
    received_input = 0
    while received_input != EXIT:
        try:
            received_input = int(input("1-Ler arquivo\n"
                                       "2-Adicionar entrada\n"
                                       "3-Criar banco de dados\n"
                                       "4-Listar a base de dados\n"
                                       "5-Sair\n"))
        except ValueError:
            print("opção inválida.\n")
            continue
        if received_input not in (PRINT_FILE, ADD, CREATE_DATABASE, READ_TABLE, EXIT):
            print("opção inválida.\n")
        if received_input == EXIT:
            sys.exit(0)
        if received_input == PRINT_FILE:
            print(FileUtils.get_file_content(INI_PATH))
            continue
        if received_input == ADD:
            print("em construção")
            continue
        if received_input == CREATE_DATABASE:
            create_database()
            continue
        if received_input == READ_TABLE:
            Database.read_inventory()
            continue


def create_database():
    Database.create_table()
    filecontent = FileUtils.get_file_content(INI_PATH)
    flat_filecontent = filecontent.replace('\n', ' ').replace(u'\xa0', u' ')
    numbers = FileUtils.get_numbers(flat_filecontent)
    titles = FileUtils.get_titles(flat_filecontent)
    interpreters = FileUtils.get_interpreters(flat_filecontent)
    dates = FileUtils.get_dates(flat_filecontent)
    volumes = FileUtils.get_volumes(flat_filecontent)
    assert len(numbers) == len(titles) == len(interpreters) == len(dates) == len(volumes)
    all = zip(numbers, titles, interpreters, dates, volumes)
    Database.insert_inventory(all)
    print("Dados inseridos com sucesso")


if __name__ == '__main__':
    main()
