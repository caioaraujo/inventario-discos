from PyPDF2 import PdfReader

import configparser


def main():
    filepath = get_file_path("setup.ini")
    reader = PdfReader(filepath)
    total_pages = len(reader.pages)
    for index_page in range(total_pages):
        page = reader.pages[index_page]
        print(page.extract_text())


def get_file_path(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)
    return config.get('filepath', 'pdf')


if __name__ == '__main__':
    main()
