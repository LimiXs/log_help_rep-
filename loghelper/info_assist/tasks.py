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
            print(file, doc_number)
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
                    record.save()
                else:
                    file = f"{os.path.splitext(file)[0]}_exist{extension}"

                record.save()

            new_file_path = os.path.join(new_directory, file)
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            shutil.move(file_path, new_directory)


def link_pdf_to_documents():
    pdf_files = PDFDataBase.objects.all()
    for pdf in pdf_files:
        try:
            document = DocumentInfo.objects.get(num_item=pdf.doc_number)
            pdf.document = document
            pdf.status = 'linked'
        except DocumentInfo.DoesNotExist:
            pdf.status = 'not_found'
        pdf.save()


def upload_docs_db():
    records = get_data_fdb()
    for record in records:
        doc_obj = DocumentInfo.objects.filter(num_item=record[0])
        if not doc_obj.exists():
            DocumentInfo.objects.create(
                date_placement=record[1],
                num_item=record[0],
                num_transport=record[3],
                num_doc=record[4],
                date_docs=record[7],
                documents=record[6],
                status=record[8],
                num_nine=record[10],
                num_td=record[11]
            )
        elif doc_obj.exists():
            doc_obj.update(
                status=record[8],
                num_nine=record[10],
                num_td=record[11]
            )
