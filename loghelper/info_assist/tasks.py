from .external_utils.file_manager import *
from .external_utils.miscellaneous import *
from .external_utils.parser_pdf import PDFParser
from .external_utils.connecter_fdb import get_data_fdb
from .models import DocumentInfo, PDFDataBase


def scan_and_load_pdfs():

    directory = os.listdir(CATALOG_PDFS)
    if len(directory) > 0:
        parser = PDFParser()

        for file in directory:
            extension = os.path.splitext(file)[1]
            file_path = os.path.join(CATALOG_PDFS, file)
            doc_number = parser.parse_pdf_for_number(file_path) if extension == parser.PDF else None

            if doc_number is None:
                new_directory = CATALOG_NOT_FOUND_FILES
            else:
                new_directory = CATALOG_DOWNLOAD_PDFS
                with open(file_path, 'rb') as pdf_file:
                    pdf_blob = pdf_file.read()

                record, created = PDFDataBase.objects.get_or_create(doc_number=doc_number)

                if created:
                    record.full_path = os.path.join(CATALOG_DOWNLOAD_PDFS, file)
                    record.file_name = file
                    record.blob = pdf_blob

                    document = None
                    try:
                        document = DocumentInfo.objects.get(num_item=doc_number)
                        record.document = document
                        record.status = 'linked'
                    except DocumentInfo.DoesNotExist:
                        pass
                    record.save()
                else:
                    file = f"{os.path.splitext(file)[0]}_exist{extension}"

            new_file_path = os.path.join(new_directory, file)
            # print(new_file_path, doc_number)
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            shutil.move(file_path, new_directory)


def link_pdf_to_documents():
    # Выбираем только те PDF, которые не связаны с документами
    pdf_files = PDFDataBase.objects.filter(document__isnull=True)

    for pdf in pdf_files:
        try:
            document = DocumentInfo.objects.get(num_item=pdf.doc_number)
            pdf.document = document
            pdf.status = 'linked'
            pdf.save()
        except DocumentInfo.DoesNotExist:
            # Если документ не найден, можно обновить статус PDF, если это необходимо
            pdf.status = 'not_found'  # или любое другое значение, которое вы хотите установить
            pdf.save()
            continue


def upload_docs_db():
    records = get_data_fdb()

    # Списки для пакетного создания и обновления
    to_create = []
    to_update = []

    for record in records:
        num_item = record[0]
        status = record[4]
        num_nine = record[6]
        num_td = record[7]

        # Попытка получить существующий объект
        doc_obj, created = DocumentInfo.objects.get_or_create(
            num_item=num_item,
            defaults={
                'date_placement': record[1],
                'num_transport': record[3],
                'status': status,
                'num_nine': num_nine,
                'num_td': num_td
            }
        )

        # Если объект уже существует и у него нет num_td, добавляем в список обновлений
        if not created and not doc_obj.num_td:
            doc_obj.status = status
            doc_obj.num_nine = num_nine
            doc_obj.num_td = num_td
            to_update.append(doc_obj)

    # Пакетное обновление
    if to_update:
        DocumentInfo.objects.bulk_update(to_update, ['status', 'num_nine', 'num_td'])

    # Пакетное создание
    if to_create:
        DocumentInfo.objects.bulk_create(to_create)
