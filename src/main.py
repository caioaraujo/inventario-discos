from PyPDF2 import PdfReader

import configparser


def main():
    filepath = get_file_path("setup.ini")
    return get_file_content(filepath)


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
