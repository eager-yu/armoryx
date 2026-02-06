# Generated data migration: assign random vpc_id to each Instance

import random
from django.db import migrations


def random_vpc_id_for_instances(apps, schema_editor):
    """为每条 Instance 记录随机分配一个 vpc_id。优先从 Vpc 表随机取，若无则生成随机字符串。"""
    Instance = apps.get_model('instances', 'Instance')
    vpc_ids = []
    try:
        Vpc = apps.get_model('vpc', 'Vpc')
        vpc_ids = list(Vpc.objects.values_list('vpc_id', flat=True))
    except LookupError:
        pass

    def random_id():
        if vpc_ids:
            return random.choice(vpc_ids)
        prefix = random.choice(['vpc-', 'vpc_'])
        return prefix + ''.join(random.choices('0123456789abcdef', k=12))

    for obj in Instance.objects.all():
        if not obj.vpc_id:
            obj.vpc_id = random_id()
            obj.save(update_fields=['vpc_id'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0002_instance_vpc_id'),
    ]

    operations = [
        migrations.RunPython(random_vpc_id_for_instances, noop),
    ]
