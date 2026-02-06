from django import template
from django.contrib.admin.helpers import AdminForm

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter to get item from dictionary"""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def admin_app_icon(app):
    """
    Return Font Awesome icon name for Django admin app.
    Maps app names to appropriate icons.
    """
    if not app:
        return 'cube'
    
    app_name = app.get('app_label', '').lower() if isinstance(app, dict) else str(app).lower()
    
    # Map common app names to icons
    icon_map = {
        'auth': 'users',
        'sessions': 'clock',
        'contenttypes': 'database',
        'admin': 'cog',
        'instances': 'server',
        'vpc': 'network-wired',
        'celery_monitor': 'tasks',
        'admin_enhanced': 'tools',
    }
    
    # Check if app_name is in the map
    if app_name in icon_map:
        return icon_map[app_name]
    
    # Default icon
    return 'cube'


@register.simple_tag
def get_admin_version():
    """
    Return Django version string for display in footer.
    """
    import django
    return django.get_version()


@register.inclusion_tag('admin/column_selector.html', takes_context=False)
def column_selector(cl):
    """
    Inclusion tag for column selector dropdown.
    Prepares context for column_selector.html template.
    """
    if not cl.list_display:
        return {'cl': cl}
    
    # Filter out action_checkbox and action_buttons from list_display
    list_display_filtered = [field for field in cl.list_display if field not in ['action_checkbox', 'action_buttons']]
    
    # Build header map for column headers
    header_map = {}
    field_to_original_index = {}
    
    for idx, field_name in enumerate(cl.list_display):
        if field_name not in ['action_checkbox', 'action_buttons']:
            # Get the display text for this field
            try:
                if hasattr(cl.model_admin, field_name):
                    method = getattr(cl.model_admin, field_name)
                    display_text = getattr(method, 'short_description', None) or field_name.replace('_', ' ').title()
                elif hasattr(cl.model, field_name):
                    field = cl.model._meta.get_field(field_name)
                    display_text = field.verbose_name or field_name.replace('_', ' ').title()
                else:
                    display_text = field_name.replace('_', ' ').title()
            except Exception:
                display_text = field_name.replace('_', ' ').title()
            
            filtered_idx = list_display_filtered.index(field_name)
            header_map[filtered_idx] = {
                'display_text': display_text,
                'field_name': field_name
            }
            field_to_original_index[field_name] = idx
    
    return {
        'cl': cl,
        'list_display_filtered': list_display_filtered,
        'header_map': header_map,
        'field_to_original_index': field_to_original_index,
    }


@register.inclusion_tag('admin/export_selector.html', takes_context=False)
def export_selector(cl):
    """
    Inclusion tag for export selector dropdown.
    """
    return {
        'cl': cl,
    }
