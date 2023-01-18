import sys

from database import Database
from fileutils import FileUtils

INI_PATH = "../setup.ini"
PRINT_FILE = 1
CREATE_DATABASE = 2
READ_TABLE = 3
ADD = 4
FETCH = 5
EXIT = 6


def main():
    print("Olá! Escolha uma das opções:\n")
    received_input = 0
    while received_input != EXIT:
        try:
            received_input = int(input("1-Ler arquivo\n"
                                       "2-Criar banco de dados\n"
                                       "3-Listar a base de dados\n"
                                       "4-Adicionar entrada\n"
                                       "5-Ler registro por número\n"
                                       "6-Sair\n"))
        except ValueError:
            print("opção inválida.\n")
            continue
        if received_input not in (PRINT_FILE, ADD, CREATE_DATABASE, READ_TABLE, FETCH, EXIT):
            print("opção inválida.\n")
        if received_input == EXIT:
            sys.exit(0)
        if received_input == PRINT_FILE:
            print(FileUtils.get_file_content(INI_PATH))
            continue
        if received_input == CREATE_DATABASE:
            create_database()
            continue
        if received_input == READ_TABLE:
            Database.read_inventory()
            continue
        if received_input == ADD:
            print("em construção")
            continue
        if received_input == FETCH:
            numero = input("Digite o número do registro que deseja consultar:\n")
            record = Database.fetch(numero)
            print(record)


def create_database():
    Database.create_table()
    content_as_tuple = FileUtils.get_file_content_as_tuple(INI_PATH)
    Database.insert_inventory(content_as_tuple)
    print("Dados inseridos com sucesso")


if __name__ == '__main__':
    main()
