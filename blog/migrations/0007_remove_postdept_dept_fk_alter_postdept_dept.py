import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_populate_dept_fk"),
        ("core", "0002_populate_departments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postdept",
            name="dept",
        ),
        migrations.RenameField(
            model_name="postdept",
            old_name="dept_fk",
            new_name="dept",
        ),
        migrations.AlterField(
            model_name="postdept",
            name="dept",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post_entries",
                to="core.department",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="postdept",
            unique_together={("post", "dept")},
        ),
    ]
