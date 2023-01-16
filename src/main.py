from PyPDF2 import PdfReader

import configparser
import sys

PRINT = 1
ADD = 2
EXIT = 3


def main():
    print("Olá! Escolha uma das opções:\n")
    received_input = 0
    while received_input != EXIT:
        try:
            received_input = int(input("1-Ler PDF\n2-Adicionar entrada\n3-Sair\n"))
        except ValueError:
            print("opção inválida.\n")
            continue
        if received_input not in (PRINT, ADD, EXIT):
            print("opção inválida.\n")
        if received_input == EXIT:
            sys.exit(0)
        if received_input == PRINT:
            filepath = get_file_path("setup.ini")
            print(get_file_content(filepath))
            continue
        if received_input == ADD:
            print("em construção")
            continue


def get_file_content(filepath):
    reader = PdfReader(filepath)
    total_pages = len(reader.pages)
    full_content = ""
    for index_page in range(total_pages):
        page = reader.pages[index_page]
        full_content += page.extract_text() + "\n"
    return full_content


def get_file_path(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)
    return config.get('filepath', 'pdf')


if __name__ == '__main__':
    main()
