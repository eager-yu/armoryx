"""
Django settings for armoryx.
Loads base, then channels and celery extensions.
"""
from .base import *  # noqa: F401, F403
from .channels import *  # noqa: F401, F403
from .celery import *  # noqa: F401, F403
