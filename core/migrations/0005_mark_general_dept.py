from django.db import migrations


def mark_general(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    Department.objects.filter(slug="general").update(is_general=True)


def unmark_general(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    Department.objects.filter(slug="general").update(is_general=False)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_department_is_general"),
        ("core", "0003_add_general_department"),
    ]

    operations = [
        migrations.RunPython(mark_general, unmark_general),
    ]
