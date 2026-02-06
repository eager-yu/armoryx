# Fix vpc_id column: replace string values with integer FK (SQLite)

from django.db import migrations, connection


def fix_vpc_id_column(apps, schema_editor):
    """Convert vpc_id from varchar (vpc_id string) to integer (vpc.id FK)."""
    if connection.vendor != 'sqlite':
        return
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(instances_instance)")
        rows = cursor.fetchall()
        # (cid, name, type, notnull, dflt_value, pk)
        col_info = {row[1]: row[2].upper() for row in rows}
        if 'vpc_id' not in col_info:
            return
        # Only fix if vpc_id is still TEXT (old CharField)
        if col_info['vpc_id'] == 'INTEGER':
            return
        # Add temporary integer column for FK
        cursor.execute(
            "ALTER TABLE instances_instance ADD COLUMN vpc_ref_id INTEGER NULL REFERENCES vpc_vpc(id)"
        )
        # Copy: set vpc_ref_id = Vpc.id where Vpc.vpc_id = Instance.vpc_id (string)
        cursor.execute("""
            UPDATE instances_instance
            SET vpc_ref_id = (SELECT id FROM vpc_vpc WHERE vpc_vpc.vpc_id = instances_instance.vpc_id)
        """)
        # Drop old varchar column
        cursor.execute("ALTER TABLE instances_instance DROP COLUMN vpc_id")
        # Rename new column to vpc_id
        cursor.execute("ALTER TABLE instances_instance RENAME COLUMN vpc_ref_id TO vpc_id")


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0006_rename_instances_i_account_idx_instances_i_account_0d65a4_idx_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_vpc_id_column, noop),
    ]
