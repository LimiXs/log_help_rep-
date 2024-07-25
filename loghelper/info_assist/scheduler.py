from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore


class Scheduler:
    def __init__(self):
        self.plan = None

    def start_scheduler(self, *tasks):
        if self.plan is None:
            self.plan = BackgroundScheduler()
            self.plan.add_jobstore(DjangoJobStore(), 'default')
            for task in tasks:
                self.plan.add_job(task['func'], 'interval', minutes=task['interval'])
            self.plan.start()

    @staticmethod
    def stop_scheduler():
        jobstore = DjangoJobStore()
        jobs = jobstore.get_all_jobs()
        for job in jobs:
            jobstore.remove_job(job.id)

