from celery import Celery

# Initialize Celery app
app = Celery('ecommerce_django')

# Load settings from Django settings module
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed apps
app.autodiscover_tasks()
