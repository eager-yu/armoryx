from django.contrib import admin
from django.http import HttpResponseForbidden


class ReadonlyMixin:
    """Mixin to make change form readonly when ?readonly=1 is in the URL"""
    
    def get_readonly_fields(self, request, obj=None):
        """Override to make all fields readonly when readonly=1 is in query params"""
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        
        # Check if readonly=1 is in the query parameters
        if request.GET.get('readonly') == '1':
            # Get all actual model fields (exclude reverse relations)
            from django.db import models
            model_fields = []
            for field in self.model._meta.get_fields():
                # Only include actual model fields, not reverse relations
                if isinstance(field, models.Field) and not isinstance(field, models.ManyToManyRel):
                    model_fields.append(field.name)
            # Add all fields to readonly_fields
            readonly_fields = list(set(readonly_fields + model_fields))
        
        return readonly_fields
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """Override to pass readonly flag to template and prevent POST in readonly mode"""
        extra_context = extra_context or {}
        is_readonly = request.GET.get('readonly') == '1'
        extra_context['is_readonly'] = is_readonly
        
        # Prevent POST requests in readonly mode
        if is_readonly and request.method == 'POST':
            return HttpResponseForbidden("Cannot save in readonly mode")
        
        return super().changeform_view(request, object_id, form_url, extra_context)
