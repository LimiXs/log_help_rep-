from django.db import models


class DocumentInfo(models.Model):
    date_placement = models.DateField(blank=False, verbose_name='Дата')
    num_item = models.CharField(max_length=30, unique=True, null=True, db_index=True, verbose_name='№ УВР')
    num_transport = models.CharField(max_length=255, blank=False, null=True, db_index=True, verbose_name='№ авто')
    num_doc = models.CharField(max_length=255, blank=True, null=True, verbose_name='№ документов')
    date_docs = models.CharField(max_length=255, blank=True, null=True, verbose_name='Дата доков')
    documents = models.CharField(max_length=255, blank=True, null=True, verbose_name='Документы')
    status = models.CharField(max_length=255, blank=True, null=True, verbose_name='Статус УВР')
    num_nine = models.CharField(max_length=30, blank=True, null=True, verbose_name='№ Длинной "9"')
    num_td = models.CharField(max_length=50, blank=True, null=True, verbose_name='Таможенное разрешение')
    path_doc = models.CharField(max_length=255, blank=True, null=True, verbose_name='Путь')
    pdf_blob = models.BinaryField(null=True, blank=True, verbose_name='PDF файл')
    objects = models.Manager()
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['id']
    
    def __str__(self):
        return self.num_item or ''


class PDFDataBase(models.Model):
    doc_number = models.CharField(max_length=70, unique=True, verbose_name='Номер уведомления')
    full_path = models.CharField(max_length=255, blank=True, verbose_name='Полный путь')
    file_name = models.CharField(max_length=30, blank=True, verbose_name='Имя файла')
    in_use = models.BooleanField(default=False, verbose_name='Путь найден')
    objects = models.Manager()

    def __str__(self):
        return self.doc_number or ''


# class DeclarationsInfo(models.Model):
#     id_declaration = models.CharField(primary_key=True, max_length=50, verbose_name='ID декларации')
#     declarant_org_name = models.CharField(max_length=255, verbose_name='Наименование организации-декларанта')
#     customs_procedure = models.CharField(max_length=255, verbose_name='Таможенная процедура')
#     customs_mode_code = models.CharField(max_length=255, verbose_name='Код таможенного режима')
#     reg_number_a = models.CharField(max_length=255, verbose_name='Регистрационный номер А')
#     date_a = models.DateField(verbose_name='Дата А')
#     reg_number_c = models.CharField(max_length=255, verbose_name='Регистрационный номер С')
#     date_c = models.DateField(verbose_name='Дата С')
#     filler_dt_surname = models.CharField(max_length=255, verbose_name='Фамилия заполнившего')
#     sender_org_name = models.CharField(max_length=255, verbose_name='Наименование организации-отправителя')
#     presented_document_number = models.CharField(max_length=255, verbose_name='Номер представленного документа')
#     presented_document_count = models.IntegerField(verbose_name='Количество представленных документов')
#     objects = models.Manager()
#
#     class Meta:
#         verbose_name = 'Таможенная декларация'
#         verbose_name_plural = 'Таможенные декларации'
#
#     def __str__(self):
#         return self.id_declaration or ''
    
    
class ERIPDataBase(models.Model):
    id_account = models.CharField(max_length=20, unique=False, null=True, verbose_name='Счёт договора')
    payer_name = models.CharField(max_length=100, unique=False, null=True, verbose_name='ФИО плательщика')
    bill_pay = models.FloatField(null=True, blank=True, verbose_name='Сумма оплаты')
    date = models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')
    last_read_time = models.DateTimeField(null=True, blank=True, verbose_name='Время последнего чтения')
    objects = models.Manager()
    
    class Meta:
        verbose_name = 'ERIP данные'
        verbose_name_plural = 'ERIP данные'
        ordering = ['id']
        
    def __str__(self):
        return self.id_account or ''
  
"""  
SELECT ('TLC2'||'-'||dtdeclaration.id),
    dtdeclaration.declarantorgname,
    dtdeclaration.customsprocedure,
    dtdeclaration.customsmodecode,
    dtdeclaration.regnumbera,
    dtdeclaration.datea,
    dtdeclaration.regnumberc,
    dtdeclaration.datec,
    dtdeclaration.fillerdtsurname,
    dtdeclaration.senderorgname,
    dtpresenteddocument.prdocumentnumber,
    count(dtdeclaration.fillerdtsurname)
FROM dtdeclaration
INNER join dtware on dtdeclaration.id = dtware.declaration
INNER join dtpresenteddocument on dtware.id=dtpresenteddocument.ware
WHERE
dtpresenteddocument.prdocumentmodecode = '09019' and
dtpresenteddocument.prdocumentdate >= :date_on
Group by dtdeclaration.id, dtdeclaration.declarantorgname,
    dtdeclaration.customsprocedure, dtdeclaration.customsmodecode,
    dtdeclaration.regnumbera, dtdeclaration.datea, dtdeclaration.regnumberc,
    dtdeclaration.datec, dtdeclaration.fillerdtsurname,
    dtdeclaration.senderorgname, dtpresenteddocument.prdocumentnumber
"""