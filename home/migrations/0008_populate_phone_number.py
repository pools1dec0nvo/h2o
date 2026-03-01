from django.db import migrations


def set_default_phone(apps, schema_editor):
    User = apps.get_model("home", "User")
    User.objects.filter(phone_number="").update(phone_number="+351900000000")


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_add_phone_number"),
    ]

    operations = [
        migrations.RunPython(set_default_phone, migrations.RunPython.noop),
    ]
