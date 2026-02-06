# Replace CharField vpc_id with ForeignKey vpc (DB column vpc_fk_id to avoid rename issues)

from django.db import migrations, models
import django.db.models.deletion


def populate_vpc_fk(apps, schema_editor):
    Instance = apps.get_model('instances', 'Instance')
    Vpc = apps.get_model('vpc', 'Vpc')
    vpc_by_id = {v.vpc_id: v for v in Vpc.objects.all()}
    for obj in Instance.objects.all():
        vpc_id_str = getattr(obj, 'vpc_id', None)
        if vpc_id_str and vpc_id_str in vpc_by_id:
            obj.vpc = vpc_by_id[vpc_id_str]
            obj.save(update_fields=['vpc'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('vpc', '0001_initial'),
        ('instances', '0003_random_vpc_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='vpc',
            field=models.ForeignKey(
                blank=True,
                help_text='所属 VPC',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='instances',
                to='vpc.vpc',
                verbose_name='VPC',
                db_column='vpc_fk_id',
            ),
        ),
        migrations.RunPython(populate_vpc_fk, noop),
        migrations.RemoveField(
            model_name='instance',
            name='vpc_id',
        ),
    ]
