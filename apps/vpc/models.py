from django.db import models
from django.utils.translation import gettext_lazy as _


class Vpc(models.Model):
    """VPC 模型"""
    
    account = models.CharField(
        _("Account"),
        max_length=100,
        help_text=_("账户名称")
    )
    
    region = models.CharField(
        _("Region"),
        max_length=50,
        help_text=_("区域")
    )
    
    vpc_id = models.CharField(
        _("VPC ID"),
        max_length=100,
        unique=True,
        help_text=_("VPC ID")
    )
    
    vpc_name = models.CharField(
        _("VPC Name"),
        max_length=200,
        help_text=_("VPC 名称")
    )
    
    class Meta:
        verbose_name = _("VPC")
        verbose_name_plural = _("VPCs")
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["account", "region"]),
            models.Index(fields=["vpc_id"]),
        ]
    
    def __str__(self):
        return f"{self.vpc_name} ({self.vpc_id})"
