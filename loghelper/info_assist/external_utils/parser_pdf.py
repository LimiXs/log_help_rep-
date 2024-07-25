import pdf2image
import pytesseract
import sys
import re
from pytesseract import Output
from info_assist.external_utils.miscellaneous import *

LATIN_TO_CYRILLIC = {
    'A': 'А', 'B': 'В', 'E': 'Е', 'K': 'К', 'M': 'М', 'H': 'Н', 'O': 'О',
    'P': 'Р', 'C': 'С', 'T': 'Т', 'X': 'Х', 'a': 'а', 'e': 'е', 'o': 'о',
    'p': 'р', 'c': 'с', 'y': 'у', 'x': 'х'
}


def convert_to_cyrillic(element):
    result = ""
    for char in element:
        result += LATIN_TO_CYRILLIC.get(char, char)
    return result


def get_doc_number(file_path):
    try:
        images = pdf2image.convert_from_path(file_path, DPI, poppler_path=POPPLER_PATH)
    except FileNotFoundError:
        print(f'File {file_path} does not exist. Please check the file path and try again.')
        sys.exit()

    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    number_pdf = ''

    for image in images:

        parsed_dict = pytesseract.image_to_data(image, lang=LANGUAGES, output_type=Output.DICT)

        if len(number_pdf) > 0:
            break

        number_pdf = ''
        text = ' '.join(parsed_dict['text'])
        text = re.sub(' +', ' ', text)

        for element in text.split(' '):
            if '-' in element and '/' in element and (len(element) == 24 or len(element) == 25):
                return convert_to_cyrillic(element)
