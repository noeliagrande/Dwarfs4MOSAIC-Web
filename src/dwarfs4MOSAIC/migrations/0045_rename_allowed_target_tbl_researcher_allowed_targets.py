# Generated by Django 5.1.5 on 2025-07-12 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwarfs4MOSAIC', '0044_tbl_researcher_allowed_target_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbl_researcher',
            old_name='allowed_target',
            new_name='allowed_targets',
        ),
    ]
