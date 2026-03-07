from django.db import migrations, models

ICONS = {
    "elec": (
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="9" y="9" width="6" height="6" rx="1"/>'
        '<rect x="4" y="4" width="16" height="16" rx="2"/>'
        '<line x1="9" y1="4" x2="9" y2="2"/>'
        '<line x1="12" y1="4" x2="12" y2="2"/>'
        '<line x1="15" y1="4" x2="15" y2="2"/>'
        '<line x1="9" y1="22" x2="9" y2="20"/>'
        '<line x1="12" y1="22" x2="12" y2="20"/>'
        '<line x1="15" y1="22" x2="15" y2="20"/>'
        '<line x1="4" y1="9" x2="2" y2="9"/>'
        '<line x1="4" y1="12" x2="2" y2="12"/>'
        '<line x1="4" y1="15" x2="2" y2="15"/>'
        '<line x1="22" y1="9" x2="20" y2="9"/>'
        '<line x1="22" y1="12" x2="20" y2="12"/>'
        '<line x1="22" y1="15" x2="20" y2="15"/>'
        '</svg>'
    ),
    "math": (
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="18" height="18" rx="2"/>'
        '<line x1="3" y1="9" x2="21" y2="9"/>'
        '<line x1="3" y1="15" x2="21" y2="15"/>'
        '<line x1="9" y1="9" x2="9" y2="21"/>'
        '<line x1="15" y1="9" x2="15" y2="21"/>'
        '</svg>'
    ),
    "finance": (
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="6" width="20" height="12" rx="2"/>'
        '<circle cx="12" cy="12" r="2.5"/>'
        '<line x1="6" y1="12" x2="6" y2="12"/>'
        '<line x1="18" y1="12" x2="18" y2="12"/>'
        '</svg>'
    ),
    "relations": (
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="9" cy="7" r="3"/>'
        '<path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/>'
        '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
        '<path d="M21 21v-2a4 4 0 0 0-3-3.85"/>'
        '</svg>'
    ),
    "dev": (
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
        ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="3" width="20" height="14" rx="2"/>'
        '<line x1="8" y1="21" x2="16" y2="21"/>'
        '<line x1="12" y1="17" x2="12" y2="21"/>'
        '</svg>'
    ),
}


def populate_icons(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    for slug, svg in ICONS.items():
        Department.objects.filter(slug=slug).update(icon_svg=svg)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_add_subteam"),
    ]

    operations = [
        migrations.AddField(
            model_name="department",
            name="icon_svg",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.RunPython(populate_icons, migrations.RunPython.noop),
    ]
