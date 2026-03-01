from django.db import migrations


def forward(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    PostDept = apps.get_model("blog", "PostDept")

    dept_map = {d.slug: d for d in Department.objects.all()}

    for entry in PostDept.objects.all():
        dept = dept_map.get(entry.dept)
        if dept:
            entry.dept_fk = dept
            entry.save(update_fields=["dept_fk"])


def backward(apps, schema_editor):
    PostDept = apps.get_model("blog", "PostDept")
    for entry in PostDept.objects.exclude(dept_fk=None):
        if entry.dept_fk:
            entry.dept = entry.dept_fk.slug
            entry.save(update_fields=["dept"])


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_postdept_dept_fk_alter_postdept_dept"),
        ("core", "0002_populate_departments"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
