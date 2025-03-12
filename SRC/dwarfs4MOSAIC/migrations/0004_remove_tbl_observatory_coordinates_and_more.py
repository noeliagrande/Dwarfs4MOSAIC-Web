# Generated by Django 5.1.5 on 2025-03-12 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwarfs4MOSAIC', '0003_tbl_observatory_coordinates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_observatory',
            name='coordinates',
        ),
        migrations.AddField(
            model_name='tbl_observatory',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tbl_observatory',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
