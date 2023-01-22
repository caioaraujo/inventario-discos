import json
import sys
import time

from database import Database
from fileutils import FileUtils

INI_PATH = "../setup.ini"
PRINT_FILE = 1
CREATE_DATABASE = 2
READ_TABLE = 3
ADD = 4
FETCH = 5
UPDATE = 6
EXPORT_TO_PDF = 7
EXIT = 8


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
                                       "6-Atualizar registro\n"
                                       "7-Exportar para PDF\n"
                                       "8-Sair\n"))
        except ValueError:
            print("opção inválida.\n")
            continue
        if received_input == EXIT:
            sys.exit(0)
        if received_input == PRINT_FILE:
            print(FileUtils.get_file_content(INI_PATH))
            continue
        if received_input == CREATE_DATABASE:
            create_database()
            continue
        if received_input == READ_TABLE:
            inventory = Database.read_inventory()
            inventory_as_json = json.dumps(inventory, indent=4, ensure_ascii=False).encode('utf8')
            print(inventory_as_json.decode())
            continue
        if received_input == ADD:
            insert_data()
            print("Dados inseridos com sucesso.")
            continue
        if received_input == FETCH:
            numero = int(input("Digite o número do registro que deseja consultar:\n"))
            record = Database.fetch(numero)
            if not record:
                print(f"Nenhum registro encontrado pelo número {numero}.")
            print(record)
            continue
        if received_input == UPDATE:
            numero = int(input("Digite o número do registro que deseja atualizar:\n"))
            record = Database.fetch(numero)
            if not record:
                print(f"Nenhum registro encontrado pelo número {numero}.")
                continue
            print(f"Registro encontrado: \n{record}")
            answer = input("Deseja alterar esse registro: (s/n):")
            if answer in ("n", "N"):
                continue
            if answer in ("s", "S"):
                update_data(numero)
                print("Dados alterados com sucesso.")
                continue
            print("Opção inválida.")
            continue
        if received_input == EXPORT_TO_PDF:
            print("Em construção.")
            continue
        print("opção inválida.\n")


def create_database():
    Database.create_table()
    content_as_tuple = FileUtils.get_file_content_as_tuple(INI_PATH)
    Database.insert_inventory(content_as_tuple)
    print("Dados inseridos com sucesso")


def insert_data():
    title = input("Digite o título:\n")
    interpreter = input("Digite o intérprete:\n")
    date = input("Digite a data:\n")
    volume = input("Total de volumes:\n")
    note = input("Alguma observação?:\n")
    last_id = Database.get_last_id()
    new_id = last_id + 1
    letter = FileUtils.get_first_letter(interpreter)
    last_letter_seq = Database.get_last_letter_seq(letter)
    new_letter_seq = last_letter_seq + 1 if last_letter_seq else 1
    recorded_year = time.strftime("%y", time.localtime())
    data = ((new_id, recorded_year, letter, new_letter_seq, title, interpreter, date, volume, note),)
    Database.insert_inventory(data)
    Database.normalize_sequence(letter)


def update_data(numero):
    title = input("Digite o novo título:\n")
    interpreter = input("Digite o novo intérprete:\n")
    date = input("Digite a nova data:\n")
    volume = input("Total de volumes:\n")
    note = input("Alguma observação?:\n")
    letter = input("Qual a letra da ordem alfabética?:\n")
    letter_seq = int(input("Qual a sequência desse disco na ordem alfabética?:\n"))
    data = ((letter, letter_seq, title, interpreter, date, volume, note, numero),)
    Database.update_inventory(data)
    Database.normalize_sequence(letter)


if __name__ == '__main__':
    main()
