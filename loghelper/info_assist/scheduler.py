# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
#
#
# class Scheduler:
#     def __init__(self):
#         self.plan = None
#
#     def start_scheduler(self, *tasks):
#         if self.plan is None:
#             self.plan = BackgroundScheduler()
#             self.plan.add_jobstore(DjangoJobStore(), 'default')
#             for task in tasks:
#                 self.plan.add_job(task['func'], 'interval', minutes=task['interval'])
#             self.plan.start()
#
#     @staticmethod
#     def stop_scheduler():
#         jobstore = DjangoJobStore()
#         jobs = jobstore.get_all_jobs()
#         for job in jobs:
#             jobstore.remove_job(job.id)
#
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, DjangoJob
from django_apscheduler import util
from .tasks import scan_and_load_pdfs


@util.close_old_connections
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Добавьте задачу
    scheduler.add_job(scan_and_load_pdfs, 'interval', minutes=5, id='scan_and_load_pdfs_0')

    # Запустите планировщик
    scheduler.start()
    print("Scheduler started!")


def stop_scheduler():
    jobstore = DjangoJobStore()
    jobs = jobstore.get_all_jobs()
    for job in jobs:
        jobstore.remove_job(job.id)
