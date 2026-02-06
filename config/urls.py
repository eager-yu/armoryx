"""
URL configuration for armoryx project.
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache

# 自定义登录视图，使用自定义模板
class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # 登录成功后跳转到 admin index
        # 由于根路径 '/' 现在是登录页面，我们需要跳转到一个明确的 admin index 路径
        # 但实际上，由于我们移除了 /admin/ 前缀，admin index 应该在 '/'
        # 但由于 '/' 被登录页面占用，我们需要创建一个新的路径，比如 '/dashboard/'
        # 或者，我们可以让登录后跳转到第一个可用的 app/model
        # 但最简单的方式是跳转到 '/'，然后让 root_login 处理（如果已登录，显示 admin index）
        return '/'

@never_cache
@staff_member_required
def admin_index_view(request):
    """Admin index 视图"""
    # 使用 admin.site.index 方法，这是 Django 6.0+ 的正确方式
    return admin.site.index(request)

@never_cache
def root_login(request):
    """根路径直接显示登录页面"""
    if request.user.is_authenticated and request.user.is_staff:
        # 如果已登录，显示 admin index 页面
        return admin_index_view(request)
    # 否则显示登录页面
    return CustomAdminLoginView.as_view()(request)

# URL 配置：先注册覆盖路径，再注册 admin URLs
# 这样覆盖路径会优先匹配，admin 的其他路径（如 /app/model/）仍然可以访问
urlpatterns = [
    # 覆盖根路径为登录页面（如果未登录）或 admin index（如果已登录）
    path("", root_login, name="root"),
    # 覆盖登录路径为自定义登录页面
    path("login/", CustomAdminLoginView.as_view(), name="login"),
    # 导出功能 URLs - 移除 /admin_enhanced/ 前缀
    path("export/", include("apps.admin_enhanced.urls")),
]

# Django admin URLs - 移除 /admin/ 前缀，直接在根路径下
# 在 Django 6.0 中，admin.site.urls 返回一个包含 (patterns, app_name, namespace) 的元组
# 我们需要使用 include() 来正确注册 namespace，但需要排除根路径和登录路径
admin_urls_tuple = admin.site.urls
if isinstance(admin_urls_tuple, tuple) and len(admin_urls_tuple) == 3:
    # Django 6.0+ 返回 (patterns, app_name, namespace)
    admin_patterns, app_name, namespace = admin_urls_tuple
    # 过滤掉根路径和登录路径
    filtered_patterns = []
    for pattern in admin_patterns:
        # 获取路由路径
        route = getattr(pattern.pattern, '_route', '')
        if not route:
            # 如果没有 _route 属性，尝试其他方式获取
            route = str(getattr(pattern.pattern, 'regex', ''))
        # 跳过根路径和登录路径，因为它们已经被覆盖
        if route != '' and route != 'login/':
            filtered_patterns.append(pattern)
    
    # 使用 include() 注册 namespace，传递 2-tuple (patterns, app_name) 和 namespace 参数
    if filtered_patterns:
        urlpatterns.append(path("", include((filtered_patterns, app_name), namespace=namespace)))
else:
    # 如果不是预期的元组格式，尝试直接使用（这种情况不应该发生）
    raise ValueError("admin.site.urls 返回的格式不符合预期")
