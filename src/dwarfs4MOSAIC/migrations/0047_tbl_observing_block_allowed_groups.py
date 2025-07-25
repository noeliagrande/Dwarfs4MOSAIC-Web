# Generated by Django 5.1.5 on 2025-07-18 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('dwarfs4MOSAIC', '0046_remove_tbl_researcher_allowed_targets_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_observing_block',
            name='allowed_groups',
            field=models.ManyToManyField(blank=True, help_text='Groups that have access to this observing block', related_name='allowed_blocks', to='auth.group'),
        ),
    ]
