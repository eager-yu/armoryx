# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="Instance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "account",
                    models.CharField(
                        help_text="账户名称",
                        max_length=100,
                        verbose_name="Account",
                    ),
                ),
                (
                    "region",
                    models.CharField(
                        help_text="区域",
                        max_length=50,
                        verbose_name="Region",
                    ),
                ),
                (
                    "instance_id",
                    models.CharField(
                        help_text="实例ID",
                        max_length=100,
                        unique=True,
                        verbose_name="Instance ID",
                    ),
                ),
                (
                    "instance_name",
                    models.CharField(
                        help_text="实例名称",
                        max_length=200,
                        verbose_name="Instance Name",
                    ),
                ),
                (
                    "ip",
                    models.GenericIPAddressField(
                        help_text="IP地址",
                        verbose_name="IP Address",
                    ),
                ),
                (
                    "security_groupid",
                    models.CharField(
                        help_text="安全组ID",
                        max_length=100,
                        verbose_name="Security Group ID",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("running", "Running"),
                            ("stopped", "Stopped"),
                            ("pending", "Pending"),
                            ("terminated", "Terminated"),
                        ],
                        default="running",
                        help_text="实例状态",
                        max_length=20,
                        verbose_name="State",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="创建时间",
                        verbose_name="Create Time",
                    ),
                ),
            ],
            options={
                "verbose_name": "Instance",
                "verbose_name_plural": "Instances",
                "ordering": ["-create_time"],
            },
        ),
        migrations.AddIndex(
            model_name="instance",
            index=models.Index(
                fields=["account", "region"], name="instances_i_account_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="instance",
            index=models.Index(fields=["state"], name="instances_i_state_idx"),
        ),
        migrations.AddIndex(
            model_name="instance",
            index=models.Index(
                fields=["create_time"], name="instances_i_create_t_idx"
            ),
        ),
    ]
