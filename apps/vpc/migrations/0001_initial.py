# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vpc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(help_text='账户名称', max_length=100, verbose_name='Account')),
                ('region', models.CharField(help_text='区域', max_length=50, verbose_name='Region')),
                ('vpc_id', models.CharField(help_text='VPC ID', max_length=100, unique=True, verbose_name='VPC ID')),
                ('vpc_name', models.CharField(help_text='VPC 名称', max_length=200, verbose_name='VPC Name')),
            ],
            options={
                'verbose_name': 'VPC',
                'verbose_name_plural': 'VPCs',
                'ordering': ['-id'],
            },
        ),
        migrations.AddIndex(
            model_name='vpc',
            index=models.Index(fields=['account', 'region'], name='vpc_vpc_account_region_idx'),
        ),
        migrations.AddIndex(
            model_name='vpc',
            index=models.Index(fields=['vpc_id'], name='vpc_vpc_vpc_id_idx'),
        ),
    ]
