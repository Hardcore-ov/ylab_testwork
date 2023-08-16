from celery import Celery

from src.config import CELERY_BROKER_URL

app = Celery('worker', broker=CELERY_BROKER_URL, include=['src.tasks.tasks'])
app.config_from_object('src.config', namespace='CELERY')
app.autodiscover_tasks()
