from django.apps import AppConfig


class CeleryMonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.celery_monitor"
    verbose_name = "Celery Monitor"
