"""
Template tags for admin_enhanced (AdminLTE 3).
"""
import django
from django import template
from django.contrib.admin.templatetags.admin_list import result_headers

register = template.Library()


@register.simple_tag
def get_admin_version():
    """Return Django version for footer (Django admin does not provide this tag)."""
    return django.get_version()

# Font Awesome icon by app_label (AdminLTE sidebar)
APP_ICONS = {
    "auth": "users-cog",
    "contenttypes": "sitemap",
    "sessions": "clock",
    "admin": "cog",
}


@register.filter
def admin_app_icon(app):
    """Return Font Awesome icon name for an app (from get_app_list)."""
    app_label = getattr(app, "app_label", None) or (app.get("app_label") if hasattr(app, "get") else None)
    return APP_ICONS.get(app_label or "", "folder")


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.inclusion_tag('admin/column_selector.html')
def column_selector(cl):
    """列选择器组件"""
    from django.contrib.admin.templatetags.admin_list import result_headers
    from django.utils.html import strip_tags
    headers = list(result_headers(cl))
    # 检查第一个 header 是否是 action_checkbox
    has_action_checkbox = headers and 'action-checkbox-column' in str(headers[0].get('class_attrib', ''))
    
    # 获取 list_display，排除 action_buttons（固定列，不应该在选择器中）
    list_display = list(cl.list_display) if cl.list_display else []
    # 过滤掉 action_buttons 和 action_checkbox
    list_display_filtered = [f for f in list_display if f not in ['action_buttons', 'action_checkbox']]
    
    # 创建映射：display_index -> header (包含处理过的显示文本)
    # 基于 list_display 的顺序，从 result_headers 中找到对应的 header
    header_map = {}
    header_offset = 1 if has_action_checkbox else 0
    
    # 遍历过滤后的 list_display，为每个字段找到对应的 header
    for display_index, field_name in enumerate(list_display_filtered):
        # 找到 field_name 在原始 list_display 中的位置
        original_index = list_display.index(field_name)
        header_index = original_index + header_offset
        if header_index < len(headers):
            original_header = headers[header_index]
            # 创建 header 的副本（如果是 dict）或直接使用
            if isinstance(original_header, dict):
                header = dict(original_header)
            else:
                # 如果不是 dict，尝试转换为 dict
                header = dict(original_header) if hasattr(original_header, '__dict__') else {'text': str(original_header)}
            
            # 处理 header 文本，确保不为空
            header_text = str(header.get('text', '')).strip()
            if header_text:
                # 移除 HTML 标签
                header_text = strip_tags(header_text).strip()
            # 如果文本仍为空，使用 field_name 作为后备
            if not header_text:
                header_text = field_name.replace('_', ' ').title()
            header['display_text'] = header_text
            header_map[display_index] = header
    
    # 创建字段名到原始索引的映射（用于 JavaScript）
    field_to_original_index = {}
    for idx, field_name in enumerate(list_display):
        if field_name not in ['action_buttons', 'action_checkbox']:
            field_to_original_index[field_name] = idx
    
    return {
        'cl': cl,
        'result_headers': headers,
        'header_map': header_map,
        'list_display_filtered': list_display_filtered,  # 传递过滤后的列表
        'field_to_original_index': field_to_original_index,  # 字段名到原始索引的映射
        'has_action_checkbox': has_action_checkbox,
    }
    
    return {
        'cl': cl,
        'result_headers': headers,
        'header_map': header_map,
        'has_action_checkbox': has_action_checkbox,
    }


@register.inclusion_tag('admin/export_selector.html')
def export_selector(cl):
    """导出选择器组件"""
    return {
        'cl': cl,
    }
