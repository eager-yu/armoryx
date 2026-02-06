# Django 6.0.2 高级后台管理系统 — 开发需求文档 (xadmin 2.0)

> 本文档为项目需求与开发任务拆解，作为开发与验收依据。

---

## 1. 项目概况与目标

为 **Django 6.0.2**（Python 3.12+）构建一套**功能增强的后台管理系统**，替代或升级原有 xadmin，具备：

- 现代化 **AdminLTE 3** 界面（基于 Bootstrap 4）
- **WebSocket 实时日志**查看（Channels + Redis）
- 列表页**动态列显示**管理（持久化到 Session/用户配置）
- **Celery** 异步任务监控与手动触发

---

## 2. 技术栈

| 类别       | 技术/版本           | 用途 |
|------------|---------------------|------|
| 运行环境   | Python 3.12+        | Django 6.0.2 要求 |
| Web 框架   | Django 6.0.2       | 主框架、Admin 扩展 |
| 前端 UI    | AdminLTE 3         | 后台布局与组件（Bootstrap 4） |
| 实时通信   | Django Channels 4.x | WebSocket |
| 消息/缓存  | Redis               | Channels 后端、日志流、Celery broker |
| 任务队列   | Celery              | 异步任务与监控 |
| 图标       | Font Awesome        | 侧边栏与菜单 |

---

## 3. 核心功能需求

### 3.1 基于 AdminLTE 3 的界面重构

**目标**：用 AdminLTE 3 完全替换 Django 默认 admin 外观，并与 Model 自动联动。

| 功能点         | 要求 |
|----------------|------|
| 侧边栏菜单     | 根据已注册的 Django Models 自动生成；支持多级菜单；支持为每项配置 Font Awesome 图标。 |
| Dashboard      | 提供类似 xadmin 的仪表盘；支持自定义 Widget 插件（统计卡片、快捷入口、图表占位等）。 |
| 响应式布局     | 桌面与移动端可用，侧边栏在移动端可折叠/抽屉式。 |
| 主题与品牌     | 支持通过配置修改主色、Logo、站点名称。 |

**实现要点**：继承/替换 Admin 的 `index`、`changelist`、`change_form` 等模板，统一使用 AdminLTE 3 的 base；菜单数据从 `AdminSite._registry` 及自定义配置生成；AdminLTE 3 静态资源通过 npm 或 CDN 纳入 `staticfiles`。

---

### 3.2 实时日志查看器（Channels + Redis）

**目标**：在后台通过 WebSocket 实时查看写入 Redis 的日志流。

| 功能点         | 要求 |
|----------------|------|
| 连接方式       | Django Channels 提供 WebSocket 端点，前端建立长连接。 |
| 数据流         | 后端订阅 Redis 指定频道/键（如 `site_logs`），新日志实时推送到前端。 |
| 前端能力       | 自动滚动、按关键词过滤、清空当前展示；可配置是否自动滚动。 |
| 日志键/频道    | 约定 Redis 键或频道名，文档与代码统一；写入方可为 Django 日志 handler 或应用代码。 |

**实现要点**：`asgi.py` 挂载 WebSocket 路由；Consumer 内使用 `redis.asyncio` 或 `channels_redis` 订阅 Redis；约定日志消息 JSON 格式（如 `level`、`message`、`timestamp`）；仅对已登录且具 staff 权限的用户开放。

---

### 3.3 动态列显示管理（Model List）

**目标**：在 Model 的 changelist 页面由用户选择要显示的列，并持久化。

| 功能点         | 要求 |
|----------------|------|
| 入口           | 列表页提供「列配置」按钮（工具栏或表头）。 |
| 交互           | 弹窗展示当前 Model 的 `list_display` 候选字段，用户勾选需要显示的列。 |
| 持久化         | 将选择保存到 Session 或用户配置表；下次访问该 Model 列表时自动应用。 |
| 联动           | 与排序、搜索、筛选兼容；列顺序可与勾选顺序一致或支持拖拽（可选）。 |

**实现要点**：通过自定义 `ChangeList` 或重写 `get_list_display` 注入可选列与当前用户已选列；存储 key 含 `app_label`、`model_name`、`user_id` 或 session_key；仅展示用户有权限查看的字段。

---

### 3.4 Celery 异步任务集成

**目标**：在后台提供 Celery 任务监控与手动触发能力。

| 功能点         | 要求 |
|----------------|------|
| 任务列表/状态  | 展示当前运行中、近期已完成、失败的任务。 |
| 状态与详情    | 展示任务 id、名称、参数、返回值、异常堆栈（失败时）；支持按状态/时间筛选。 |
| 手动触发      | 支持选择已注册任务并填写参数后触发，类似 xadmin 的 Action。 |
| 管理后台集成   | 以独立模块形式集成到同一 AdminLTE 后台中。 |

**实现要点**：通过 Celery inspector 与 result backend 获取任务列表与详情；可触发任务使用白名单配置；仅 staff/superuser 可访问；危险任务可二次确认。

---

## 4. 非功能要求

- **安全**：新页面与 WebSocket 均做登录与 staff 权限校验；列配置、任务触发防 CSRF。
- **性能**：日志 WebSocket 做消息频率或长度限制；Celery 监控列表做分页或数量上限。
- **可维护性**：Redis 键名、Celery 队列名等配置集中到 `settings`。
- **文档**：README 提供运行方式、依赖、环境变量；本需求文档作为验收依据。

---

## 5. 项目结构

```
armoryx/
├── config/                 # 项目配置
│   ├── settings/
│   │   ├── base.py
│   │   ├── channels.py
│   │   └── celery.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── admin_enhanced/     # AdminLTE 3 + 动态列
│   │   ├── templates/
│   │   ├── static/
│   │   ├── admin.py
│   │   └── ...
│   ├── logviewer/          # 实时日志 WebSocket + 页面
│   │   ├── consumers.py
│   │   ├── routing.py
│   │   └── ...
│   └── celery_monitor/     # Celery 任务监控与触发
│       ├── views.py
│       ├── urls.py
│       └── ...
├── manage.py
├── requirements/
│   ├── base.txt
│   └── dev.txt
└── docs/
    └── REQUIREMENTS.md
```

---

## 6. 关键配置要点

### 6.1 settings

- **Django**：`INSTALLED_APPS`（`daphne` 置于最前、`channels`、各 app）、`STATIC/STATICFILES`；若替换默认 admin 则配置自定义 `ADMIN_SITE`。
- **Channels**：`ASGI_APPLICATION`、`CHANNEL_LAYERS`（如 `channels_redis` 的 Redis 地址）。
- **Celery**：`CELERY_BROKER_URL`、`CELERY_RESULT_BACKEND`、时区等。

### 6.2 asgi.py

- 使用 `ProtocolTypeRouter`：`http` 交给 Django ASGI，`websocket` 交给 Channels 的 WebSocket 路由。
- WebSocket 路由指向 logviewer 的 Consumer。

### 6.3 urls.py（URL 配置）

**特殊配置**：移除所有 `/admin/` 前缀，根路径直接显示登录页面。

#### URL 结构

- **根路径 `/`**：直接显示登录页面（未登录）或 admin index（已登录）
- **登录路径 `/login/`**：自定义 AdminLTE 3 风格登录页面
- **Admin URLs**：移除 `/admin/` 前缀，直接在根路径下
  - 例如：`/instances/instance/`（原 `/admin/instances/instance/`）
  - `/logout/`、`/jsi18n/` 等也在根路径下
- **导出功能**：`/export/<app_label>/<model_name>/<format>/`（原 `/admin_enhanced/export/...`）

#### 实现要点

1. **自定义登录视图**：`CustomAdminLoginView` 使用自定义模板 `admin/login.html`
2. **根路径处理**：`root_login` 视图根据用户认证状态显示登录页面或 admin index
3. **Admin URLs 集成**：
   - Django 6.0 中 `admin.site.urls` 返回 `(patterns, app_name, namespace)` 元组
   - 需要手动解包并过滤掉根路径和登录路径（已被自定义视图覆盖）
   - 使用 `include()` 注册 namespace，传递 2-tuple `(filtered_patterns, app_name)` 和 `namespace` 参数
4. **Namespace 注册**：确保 'admin' namespace 正确注册，以便模板中的 `{% url 'admin:index' %}` 等 URL 反向解析正常工作

#### 代码示例

```python
# 根路径和登录路径覆盖
urlpatterns = [
    path("", root_login, name="root"),
    path("login/", CustomAdminLoginView.as_view(), name="login"),
    path("export/", include("apps.admin_enhanced.urls")),
]

# Admin URLs - 移除 /admin/ 前缀
admin_urls_tuple = admin.site.urls
if isinstance(admin_urls_tuple, tuple) and len(admin_urls_tuple) == 3:
    admin_patterns, app_name, namespace = admin_urls_tuple
    # 过滤掉根路径和登录路径
    filtered_patterns = [p for p in admin_patterns 
                        if getattr(p.pattern, '_route', '') not in ('', 'login/')]
    if filtered_patterns:
        urlpatterns.append(path("", include((filtered_patterns, app_name), namespace=namespace)))
```

---

## 7. 开发顺序概览

| 阶段 | 名称             | 对应需求   |
|------|------------------|------------|
| 1    | 搭建项目         | §5、§6     |
| 2    | AdminLTE 3 集成  | §3.1       |
| 3    | 实时日志         | §3.2       |
| 4    | 动态列管理       | §3.3       |
| 5    | Celery 集成      | §3.4       |

---

## 8. 开发任务拆解（小步验收）

以下任务按阶段分组，每项可单独开发与验收。

### 阶段 1：搭建项目

| 序号 | Task         | 描述 | 验收标准 |
|------|--------------|------|----------|
| 1.1  | 项目骨架     | 用 Django 6.0.2 创建项目，`manage.py` 与 config 包位于仓库根下 | `python3.12 manage.py check` 通过；目录符合 §5 |
| 1.2  | settings 分包 | 配置拆为 `base.py`、`channels.py`、`celery.py`，主配置合并加载 | 通过 `DJANGO_SETTINGS_MODULE` 正常启动 |
| 1.3  | 依赖清单     | 编写 `requirements/base.txt`、`dev.txt`（Django、Channels、Celery 等） | `pip3.12 install -r requirements/base.txt` 成功 |
| 1.4  | asgi.py 占位 | `ProtocolTypeRouter`，http 走 Django，websocket 路由占位 | ASGI 可被 Daphne 加载，WebSocket 可连接 |
| 1.5  | apps 占位    | 创建 `admin_enhanced`、`logviewer`、`celery_monitor` 并加入 `INSTALLED_APPS` | `manage.py check` 通过；可 `runserver` |
| 1.6  | 默认 admin   | 确保根路径可登录并使用 | 访问 `/` 可见登录页，登录后进入 admin |
| 1.7  | URL 配置优化 | 移除 `/admin/` 前缀，根路径直接显示登录页面 | 访问 `/` 显示登录页；所有 admin URLs 在根路径下 |

---

### 阶段 2：AdminLTE 3 集成

| 序号 | Task           | 描述 | 验收标准 |
|------|----------------|------|----------|
| 2.1  | 静态资源引入   | 引入 AdminLTE 3、Bootstrap 4、Font Awesome，纳入 `staticfiles` | 模板中引用 AdminLTE CSS/JS 无 404 |
| 2.2  | Admin base 模板 | 新建 admin 用 base 模板，采用 AdminLTE 3 结构（顶栏 + 侧边栏 + content） | 继承该 base 的页面呈现 AdminLTE 布局 |
| 2.3  | 替换 index 模板 | 覆盖 admin 的 `index.html`，使用 AdminLTE base | 访问 admin index 显示 AdminLTE 风格首页 |
| 2.4  | 侧边栏菜单数据 | 从 `AdminSite._registry` 生成菜单结构（app/model 分组），支持图标配置 | 模板中能遍历「应用 → 模型」菜单数据 |
| 2.5  | 侧边栏多级渲染 | 在 base 模板中根据菜单数据渲染多级侧边栏与 Font Awesome 图标 | 侧边栏显示 app 与 model 链接，点击进入 changelist |
| 2.6  | changelist/change_form 模板 | 覆盖 `change_list.html`、`change_form.html`，继承 AdminLTE base | 列表页与编辑页均为 AdminLTE 风格 |
| 2.7  | Dashboard 占位 | index 页增加 Dashboard 区域（统计卡片或 Widget 占位） | 首页除应用列表外可见仪表盘区域 |
| 2.8  | 响应式与移动端 | AdminLTE 的 responsive 与侧边栏折叠行为生效 | 缩小视口时侧边栏可折叠/抽屉式 |

---

### 阶段 3：实时日志

| 序号 | Task           | 描述 | 验收标准 |
|------|----------------|------|----------|
| 3.1  | WebSocket 路由 | 在 `asgi.py` 中为 logviewer 挂载 WebSocket 路由（如 `/ws/logs/`） | 客户端可连上该路径并收到占位消息 |
| 3.2  | Log Consumer 骨架 | 实现 `LogViewerConsumer`，仅允许已认证 staff 用户 | 未登录或非 staff 连接被拒绝；staff 连接成功 |
| 3.3  | Redis 订阅    | Consumer 内订阅约定 Redis 频道/键（如 `site_logs`），新消息时通过 WebSocket 发送 | 向 Redis 写入测试日志后，客户端能收到 |
| 3.4  | 日志消息格式  | 约定并实现 JSON 格式（`level`、`message`、`timestamp`） | 前端能解析并区分 level |
| 3.5  | 日志页面入口  | 在 admin 中增加「实时日志」菜单项与页面，页面内建立 WebSocket 连接 | 点击菜单可打开日志页并建立连接 |
| 3.6  | 前端展示与自动滚动 | 接收消息后追加到展示区域，支持自动滚动到底部与开关 | 新日志到达时列表更新；有自动滚动开关 |
| 3.7  | 关键词过滤   | 前端提供输入框，仅展示包含关键词的日志行（本地过滤） | 输入关键词后列表只显示匹配行 |
| 3.8  | 清空日志     | 前端提供「清空」按钮，清空当前展示的日志（不关连接） | 点击后展示区域清空，连接保持 |

---

### 阶段 4：动态列管理

| 序号 | Task           | 描述 | 验收标准 |
|------|----------------|------|----------|
| 4.1  | 列配置入口     | 在 changelist 页增加「列配置」按钮 | 列表页可见按钮，点击有反馈（如弹窗） |
| 4.2  | 候选列数据     | changelist 的 context 或 API 提供当前 Model 的 `list_display` 候选字段列表 | 前端能拿到可选字段 id 与显示名 |
| 4.3  | 弹窗与勾选 UI  | 弹窗内展示候选字段复选框，支持全选/反选；显示当前已选列 | 用户可勾选/取消，与当前列表一致 |
| 4.4  | 保存列配置 API | 提供接口保存用户选择的列，存储 key 含 app_label、model_name、user_id 或 session | 提交后成功；不同 Model 互不干扰 |
| 4.5  | 读取列配置    | changelist 加载时根据当前 user/session 读取已保存列配置 | 再次打开该 model 列表时应用上次选择 |
| 4.6  | 应用列到列表  | 使用自定义 `ChangeList` 或重写 `get_list_display`，按用户选择渲染列与顺序 | 表头与数据列与用户选择一致 |
| 4.7  | 与排序/搜索联动 | 列配置与 `list_filter`、`search_fields`、排序参数兼容 | 切换列后排序、搜索、筛选仍正常 |

---

### 阶段 5：Celery 集成

| 序号 | Task           | 描述 | 验收标准 |
|------|----------------|------|----------|
| 5.1  | Celery 应用与配置 | 配置 Celery app（broker、result backend、时区），可独立启动 worker | `celery -A config worker` 能启动；有简单测试任务可执行 |
| 5.2  | 监控页入口与权限 | 在 admin 中增加「Celery 任务」菜单与监控页，仅 staff 可访问 | 仅 staff 可访问；其他用户 403 |
| 5.3  | 任务列表展示   | 从 inspector 和/或 result backend 获取运行中、已完成、失败任务并分页展示 | 页面展示任务 id、名称、状态、时间等 |
| 5.4  | 任务详情       | 点击某任务可查看参数、返回值、异常堆栈（失败时） | 详情页展示完整信息且堆栈可读 |
| 5.5  | 可触发任务白名单 | 在 settings 或注册表中配置允许在后台触发的任务名列表 | 仅白名单内任务出现在「手动触发」列表 |
| 5.6  | 手动触发表单   | 表单：选择任务、填写参数，提交后调用 `apply_async` | 提交后任务进入队列；返回 task_id 并可跳转详情 |
| 5.7  | 与 AdminLTE 统一 | 监控页与任务详情页使用同一 AdminLTE base 模板 | 与其余 admin 页面视觉统一 |

---

### 任务索引

- **阶段 1**：1.1～1.7（7 项）
- **阶段 2**：2.1～2.8（8 项）
- **阶段 3**：3.1～3.8（8 项）
- **阶段 4**：4.1～4.7（7 项）
- **阶段 5**：5.1～5.7（7 项）

合计 **37 项** 可验收子任务。

---

## 9. 开发指令示例（可直接使用）

```
请基于 Django 6.0.2（Python 3.12）完成 armoryx 增强后台的下列能力：

1. 使用 AdminLTE 3 替换默认 admin 模板，侧边栏根据已注册 Model 自动生成，支持多级菜单与 Font Awesome 图标，并提供基础 Dashboard。
2. 配置 Django Channels，实现后台页面通过 WebSocket 实时读取 Redis 里约定的 site_logs 键（或频道）并展示；前端支持自动滚动、关键词过滤和清空。
3. 在 ModelAdmin changelist 添加「列配置」按钮与弹窗，允许用户勾选显示的字段，并将选择持久化到 Session 或用户配置，下次访问自动应用；与排序、搜索联动。
4. 集成 Celery，在后台提供监控面板：查看运行中/已完成/失败任务的状态、参数与异常堆栈，并支持对白名单任务进行手动触发。

请按 docs/REQUIREMENTS.md §8 中的任务拆解分步实现，优先完成当前阶段验收标准。
```

---

**文档版本**：1.0  
**适用项目**：armoryx（Django 6.0.2 高级后台管理系统）
