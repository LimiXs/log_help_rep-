import pdf2image
import pytesseract
import sys
import re
from pytesseract import Output


class PDFParser:
    LATIN_TO_CYRILLIC = {
        'A': 'А', 'B': 'В', 'E': 'Е', 'K': 'К', 'M': 'М', 'H': 'Н', 'O': 'О',
        'P': 'Р', 'C': 'С', 'T': 'Т', 'X': 'Х', 'a': 'а', 'e': 'е', 'o': 'о',
        'p': 'р', 'c': 'с', 'y': 'у', 'x': 'х'
    }
    LANGUAGES = 'rus+eng'
    DPI = 400
    POPPLER_PATH = r'C:\Program Files\Poppler\Library\bin'
    TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    PDF = '.pdf'

    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = self.TESSERACT_PATH

    def __convert_to_cyrillic(self, element):
        result = ""
        for char in element:
            result += self.LATIN_TO_CYRILLIC.get(char, char)
        return result

    @staticmethod
    def __is_valid_format(element):
        if len(element) not in (24, 25):
            return False
        pattern = r'^[A-ZА-Я]{2}.{5}/\d{7}/\d{8}$'
        return re.match(pattern, element) is not None

    def parse_pdf_for_number(self, file_path):
        try:
            images = pdf2image.convert_from_path(file_path, self.DPI, poppler_path=self.POPPLER_PATH)
        except FileNotFoundError:
            print(f'File {file_path} does not exist. Please check the file path and try again.')
            sys.exit()

        number_pdf = ''

        for image in images:
            parsed_dict = pytesseract.image_to_data(image, lang=self.LANGUAGES, output_type=Output.DICT)
            if len(number_pdf) > 0:
                break

            number_pdf = ''
            text = ' '.join(parsed_dict['text'])
            text = re.sub(' +', ' ', text)

            for element in text.split(' '):
                print(element)
                if self.__is_valid_format(element):
                    return self.__convert_to_cyrillic(element)
