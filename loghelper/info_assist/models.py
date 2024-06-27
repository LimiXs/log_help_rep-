from django.db import models


class DocumentInfo(models.Model):
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['id']

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
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True, verbose_name='PDF файл')
    objects = models.Manager()

    def __str__(self):
        return self.num_item or ''


class ERIPDataBase(models.Model):
    class Meta:
        verbose_name = 'ERIP данные'
        verbose_name_plural = 'ERIP данные'
        ordering = ['id']

    id_account = models.CharField(max_length=20, unique=False, null=True, verbose_name='Счёт договора')
    payer_name = models.CharField(max_length=100, unique=False, null=True, verbose_name='ФИО плательщика')
    bill_pay = models.FloatField(null=True, blank=True, verbose_name='Сумма оплаты')
    date = models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')
    last_read_time = models.DateTimeField(null=True, blank=True, verbose_name='Время последнего чтения')

    objects = models.Manager()

    def __str__(self):
        return self.id_account or ''


class PDFDataBase(models.Model):
    doc_number = models.CharField(max_length=70, unique=True, verbose_name='Номер уведомления')
    full_path = models.CharField(max_length=255, blank=True, verbose_name='Полный путь')
    file_name = models.CharField(max_length=30, blank=True, verbose_name='Имя файла')
    in_use = models.BooleanField(default=False, verbose_name='Путь найден')
    # date_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    # date_updated = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    # doc_id = models.OneToOneField('Note', on_delete=models.SET_NULL, null=True, blank=True,
    #                               related_name='uv_doc', verbose_name='Документ')
    objects = models.Manager()

    def __str__(self):
        return self.doc_number or ''