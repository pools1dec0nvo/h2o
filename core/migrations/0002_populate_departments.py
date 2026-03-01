from django.db import migrations


DEPT_DATA = [
    {
        "slug": "elec",
        "full_name": "Electronics",
        "short_name": "Electronics",
        "portuguese_name": "Eletrónica",
        "description": "",
        "color": "#e53e3e",
    },
    {
        "slug": "dev",
        "full_name": "Software + Firmware",
        "short_name": "Software",
        "portuguese_name": "Software e Firmware",
        "description": "",
        "color": "#f6c90e",
    },
    {
        "slug": "math",
        "full_name": "Geography and Statistics",
        "short_name": "Geography",
        "portuguese_name": "Geografia e Estatística",
        "description": "",
        "color": "#38a169",
    },
    {
        "slug": "finance",
        "full_name": "Finance",
        "short_name": "Finance",
        "portuguese_name": "Finanças",
        "description": "",
        "color": "#3182ce",
    },
    {
        "slug": "relations",
        "full_name": "External Relations",
        "short_name": "Relations",
        "portuguese_name": "Relações Externas",
        "description": "",
        "color": "#d53f8c",
    },
]


def populate_departments(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    for data in DEPT_DATA:
        Department.objects.get_or_create(slug=data["slug"], defaults=data)


def depopulate_departments(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    Department.objects.filter(slug__in=[d["slug"] for d in DEPT_DATA]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_departments, depopulate_departments),
    ]
