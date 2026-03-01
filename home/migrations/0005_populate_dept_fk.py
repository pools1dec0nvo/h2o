from django.db import migrations


def forward(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    User = apps.get_model("home", "User")
    UserDeptOther = apps.get_model("home", "UserDeptOther")

    dept_map = {d.slug: d for d in Department.objects.all()}

    for user in User.objects.exclude(dept_main=""):
        dept = dept_map.get(user.dept_main)
        if dept:
            user.dept_main_fk = dept
            user.save(update_fields=["dept_main_fk"])

    for entry in UserDeptOther.objects.all():
        dept = dept_map.get(entry.dept)
        if dept:
            entry.dept_fk = dept
            entry.save(update_fields=["dept_fk"])


def backward(apps, schema_editor):
    User = apps.get_model("home", "User")
    UserDeptOther = apps.get_model("home", "UserDeptOther")

    for user in User.objects.exclude(dept_main_fk=None):
        if user.dept_main_fk:
            user.dept_main = user.dept_main_fk.slug
            user.save(update_fields=["dept_main"])

    for entry in UserDeptOther.objects.exclude(dept_fk=None):
        if entry.dept_fk:
            entry.dept = entry.dept_fk.slug
            entry.save(update_fields=["dept"])


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_user_dept_main_fk_userdeptother_dept_fk"),
        ("core", "0002_populate_departments"),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
