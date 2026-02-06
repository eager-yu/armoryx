"""
URL configuration for admin_enhanced app.
"""
from django.urls import path
from . import views

app_name = 'admin_enhanced'

urlpatterns = [
    path(
        '<str:app_label>/<str:model_name>/<str:format_type>/',
        views.export_changelist,
        name='export_changelist'
    ),
]
