from apscheduler.schedulers.background import BackgroundScheduler


from AlacenenesPyme import settings
from apps.APyme.jobs import jobs


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobs.ppp, 'interval', seconds=settings.SCHEDULER_TIME_SEC)
    scheduler.start()
