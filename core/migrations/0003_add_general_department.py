from django.db import migrations


def add_general(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    Department.objects.get_or_create(
        slug="general",
        defaults={
            "full_name": "General",
            "short_name": "General",
            "portuguese_name": "Geral",
            "description": "",
            "color": "#94a3b8",
        },
    )


def remove_general(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    Department.objects.filter(slug="general").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_populate_departments"),
    ]

    operations = [
        migrations.RunPython(add_general, remove_general),
    ]
