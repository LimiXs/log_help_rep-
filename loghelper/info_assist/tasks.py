from .external_utils.file_manager import *
from .external_utils.connecter_fdb import get_data_fdb
from .external_utils.parser_pdf import *
from .models import DocumentInfo, PDFDataBase


def match_pdfs_docs():
    upload_docs_db()

    directory = os.listdir(CATALOG_PDFS)
    if len(directory) > 0:
        for file in directory:
            extension = os.path.splitext(file)[1]
            file_path = os.path.join(CATALOG_PDFS, file)

            doc_number = get_doc_number(file_path) if extension == PDF else None
            if doc_number is None or extension != PDF:
                new_directory = CATALOG_NOT_FOUND_FILES
            else:
                new_directory = CATALOG_DOWNLOAD_PDFS
                download_path = os.path.join(CATALOG_DOWNLOAD_PDFS, file)
                try:
                    record = PDFDataBase(doc_number=doc_number, full_path=download_path, file_name=file)
                    record.save()
                except Exception as e:
                    print(f"Ошибка при сохранении записи: {e}")

            new_file_path = os.path.join(new_directory, file)
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            shutil.move(file_path, new_directory)

    pdf_data = PDFDataBase.objects.all()
    for pdf in pdf_data:
        doc_info = DocumentInfo.objects.filter(num_item=pdf.doc_number)
        if doc_info.exists():
            doc_info.update(path_doc=pdf.full_path)
            doc_info_instance = doc_info.first()
            with open(pdf.full_path, 'rb') as pdf_file:
                doc_info_instance.pdf_blob = pdf_file.read()
                doc_info_instance.save()

            pdf.in_use = True
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
