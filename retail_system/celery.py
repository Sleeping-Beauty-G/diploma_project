import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retail_system.settings")

app = Celery("retail_system")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.timezone = "UTC"