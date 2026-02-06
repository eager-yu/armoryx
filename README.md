# armoryx

Django 6.0.2 高级后台管理系统（xadmin 2.0 计划）。需求与任务拆解见 [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md)。

## 环境

- **Python 3.12**（Django 6.0.2 要求）
- Redis（Channels / Celery 使用，阶段 3/5 需要）

## 阶段 1 验收（搭建项目）

```powershell
# 1. 安装依赖（使用 python3.12 / pip3.12）
pip3.12 install -r requirements/base.txt

# 2. 检查项目
python3.12 manage.py check

# 3. 数据库迁移
python3.12 manage.py migrate

# 4. 创建超级用户（用于登录后台）
python3.12 manage.py createsuperuser

# 5. 启动开发服务器
python3.12 manage.py runserver
```

浏览器访问 **http://127.0.0.1:8000/** 应看到 AdminLTE 3 风格的登录页面。

**注意**：本项目移除了 `/admin/` 前缀，所有 admin 功能直接在根路径下访问：
- 根路径 `/`：登录页面（未登录）或 admin index（已登录）
- `/instances/instance/`：实例列表（原 `/admin/instances/instance/`）
- `/export/...`：导出功能（原 `/admin_enhanced/export/...`）

### ASGI（WebSocket 占位）

```powershell
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

连接 `ws://127.0.0.1:8000/ws/logs/` 会收到欢迎消息（阶段 3 接入 Redis 日志流）。

## 项目结构（阶段 1）

```
armoryx/
├── config/           # 项目配置
│   ├── settings/     # base.py, channels.py, celery.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── admin_enhanced/
│   ├── logviewer/
│   └── celery_monitor/
├── requirements/
│   ├── base.txt
│   └── dev.txt
├── manage.py
└── docs/REQUIREMENTS.md
```
