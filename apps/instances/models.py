from django.db import models
from django.utils.translation import gettext_lazy as _


class Instance(models.Model):
    """云实例模型"""
    
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
    
    instance_id = models.CharField(
        _("Instance ID"),
        max_length=100,
        unique=True,
        help_text=_("实例ID")
    )
    
    instance_name = models.CharField(
        _("Instance Name"),
        max_length=200,
        help_text=_("实例名称")
    )
    
    ip = models.GenericIPAddressField(
        _("IP Address"),
        help_text=_("IP地址")
    )
    
    security_groupid = models.CharField(
        _("Security Group ID"),
        max_length=100,
        help_text=_("安全组ID")
    )
    
    vpc = models.ForeignKey(
        "vpc.Vpc",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instances",
        verbose_name=_("VPC"),
        help_text=_("所属 VPC"),
    )
    
    STATE_CHOICES = [
        ("running", _("Running")),
        ("stopped", _("Stopped")),
        ("pending", _("Pending")),
        ("terminated", _("Terminated")),
    ]
    
    state = models.CharField(
        _("State"),
        max_length=20,
        choices=STATE_CHOICES,
        default="running",
        help_text=_("实例状态")
    )
    
    create_time = models.DateTimeField(
        _("Create Time"),
        auto_now_add=True,
        help_text=_("创建时间")
    )
    
    class Meta:
        verbose_name = _("Instance")
        verbose_name_plural = _("Instances")
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["account", "region"]),
            models.Index(fields=["state"]),
            models.Index(fields=["create_time"]),
        ]
    
    def __str__(self):
        return f"{self.instance_name} ({self.instance_id})"
