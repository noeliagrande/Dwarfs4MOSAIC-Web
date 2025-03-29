# Generated by Django 5.1.5 on 2025-03-29 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwarfs4MOSAIC', '0026_remove_tbl_target_distance_tbl_target_semester_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_observing_block',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='tbl_observing_run',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='tbl_target',
            name='notes',
        ),
        migrations.AddField(
            model_name='tbl_observing_block',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Comments'),
        ),
        migrations.AddField(
            model_name='tbl_observing_run',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Comments'),
        ),
        migrations.AddField(
            model_name='tbl_target',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Comments'),
        ),
    ]
