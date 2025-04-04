# Generated by Django 5.1.5 on 2025-03-19 11:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwarfs4MOSAIC', '0022_alter_tbl_observatory_altitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_observing_block',
            name='researchers',
        ),
        migrations.AlterField(
            model_name='tbl_telescope',
            name='aperture',
            field=models.FloatField(default=0, help_text='meters', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Aperture'),
        ),
    ]
