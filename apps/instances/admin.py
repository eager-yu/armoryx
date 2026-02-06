from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Instance


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = [
        "instance_id",
        "instance_name",
        "account",
        "region",
        "ip",
        "state",
        "security_groupid",
        "create_time",
        "action_buttons",
    ]
    list_display_links = ["instance_id"]  # 确保操作列不被链接
    list_filter = [
        "account",
        "region",
        "state"
    ]
    search_fields = [
        "instance_id",
        "instance_name",
        "account",
        "ip",
        "security_groupid",
    ]
    readonly_fields = ["create_time"]
    date_hierarchy = "create_time"
    list_per_page = 50
    
    def action_buttons(self, obj):
        """操作按钮列 - 根据权限显示不同的按钮"""
        if not hasattr(self, 'request'):
            return "-"
        
        buttons = []
        opts = self.model._meta
        app_label = opts.app_label
        model_name = opts.model_name
        
        # 检查权限
        has_view_permission = self.has_view_permission(self.request, obj) if hasattr(self, 'has_view_permission') else self.has_change_permission(self.request, obj)
        has_change_permission = self.has_change_permission(self.request, obj)
        has_delete_permission = self.has_delete_permission(self.request, obj)
        
        # 查看按钮（如果有查看权限或编辑权限）
        if has_view_permission or has_change_permission:
            view_url = reverse(
                f"admin:{app_label}_{model_name}_change",
                args=[obj.pk]
            )
            buttons.append(
                format_html(
                    '<a href="{}" class="btn btn-sm btn-outline-info">{}</a>',
                    view_url,
                    _("View")
                )
            )
        
        # 编辑按钮（需要编辑权限）
        if has_change_permission:
            change_url = reverse(
                f"admin:{app_label}_{model_name}_change",
                args=[obj.pk]
            )
            buttons.append(
                format_html(
                    '<a href="{}" class="btn btn-sm btn-outline-primary">{}</a>',
                    change_url,
                    _("Edit")
                )
            )
        
        # 删除按钮（需要删除权限）
        if has_delete_permission:
            delete_url = reverse(
                f"admin:{app_label}_{model_name}_delete",
                args=[obj.pk]
            )
            buttons.append(
                format_html(
                    '<a href="{}" class="btn btn-sm btn-outline-danger" '
                    'onclick="return confirm(\'{}\');">{}</a>',
                    delete_url,
                    _("Are you sure you want to delete this item?"),
                    _("Delete")
                )
            )
        
        if buttons:
            return mark_safe('<div class="action-buttons-group">{}</div>'.format(" ".join(buttons)))
        return "-"
    
    action_buttons.short_description = _("Actions")
    
    def get_list_display(self, request):
        """重写以传递 request 对象"""
        self.request = request
        return super().get_list_display(request)
    
    def get_queryset(self, request):
        """重写以传递 request 对象"""
        self.request = request
        return super().get_queryset(request)
