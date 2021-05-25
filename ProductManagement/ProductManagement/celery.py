import os
from django.conf import settings
from celery import Celery

if eval(os.environ.get('IS_PRODUCTION')):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProductManagement.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProductManagement.settings.local')


app = Celery('product-management')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(settings.INSTALLED_APPS)
