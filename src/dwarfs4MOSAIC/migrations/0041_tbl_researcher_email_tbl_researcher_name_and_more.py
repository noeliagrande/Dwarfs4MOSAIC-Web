# Generated by Django 5.1.5 on 2025-04-07 05:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwarfs4MOSAIC', '0040_alter_tbl_target_datafiles_path_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_researcher',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email'),
        ),
        migrations.AddField(
            model_name='tbl_researcher',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tbl_researcher',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='researcher', to=settings.AUTH_USER_MODEL, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='datafiles_path',
            field=models.CharField(blank=True, help_text="Path relative to 'Dwarfs4MOSAIC/src/media'", max_length=255, null=True, verbose_name='Data files path'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='image',
            field=models.CharField(blank=True, help_text="Path relative to 'Dwarfs4MOSAIC/src/media'", max_length=255, null=True, verbose_name='Image'),
        ),
    ]
