from django.apps import AppConfig


class AdminEnhancedConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.admin_enhanced"
    verbose_name = "Enhanced Admin"
