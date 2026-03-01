import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_populate_departments"),
        ("home", "0005_populate_dept_fk"),
    ]

    operations = [
        # User.dept_main: remove old CharField, rename FK into its place
        migrations.RemoveField(
            model_name="user",
            name="dept_main",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="dept_main_fk",
            new_name="dept_main",
        ),
        migrations.AlterField(
            model_name="user",
            name="dept_main",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="leaders",
                to="core.department",
                verbose_name="Main Department",
            ),
        ),
        # UserDeptOther.dept: remove old CharField, rename FK into its place
        migrations.AlterUniqueTogether(
            name="userdeptother",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="userdeptother",
            name="dept",
        ),
        migrations.RenameField(
            model_name="userdeptother",
            old_name="dept_fk",
            new_name="dept",
        ),
        migrations.AlterField(
            model_name="userdeptother",
            name="dept",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to="core.department",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="userdeptother",
            unique_together={("user", "dept")},
        ),
    ]
