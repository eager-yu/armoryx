# Data migration no longer needed - population done in 0004_instance_vpc

from django.db import migrations


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0004_instance_vpc'),
    ]

    operations = [
        migrations.RunPython(noop, noop),
    ]
