from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, DjangoJob
from django_apscheduler import util
from .tasks import scan_and_load_pdfs, link_pdf_to_documents, upload_docs_db


def do_sequence_tasks():
    scan_and_load_pdfs()
    upload_docs_db()
    link_pdf_to_documents()


@util.close_old_connections
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    try:
        # Добавьте задачу
        scheduler.add_job(do_sequence_tasks, 'interval', minutes=10, id='scan_and_load_pdfs_0')
        # Запустите планировщик
        scheduler.start()
        print("Scheduler started!")
    except Exception as e:
        print(f"Error starting scheduler: {e}")
        if "Job 'scan_and_load_pdfs_0' already exists" in str(e):
            print("Scheduler already running with job id 'scan_and_load_pdfs_0'.")


def stop_scheduler():
    job_store = DjangoJobStore()
    jobs = job_store.get_all_jobs()
    for job in jobs:
        job_store.remove_job(job.id)
