# Generated by Django 5.1.5 on 2025-03-19 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwarfs4MOSAIC', '0024_tbl_target_alter_tbl_observing_block_exposure_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_observing_block',
            name='target',
            field=models.ManyToManyField(related_name='observing_blocks', to='dwarfs4MOSAIC.tbl_target'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='declination',
            field=models.CharField(blank=True, help_text='+/- deg:min:sec', max_length=15, null=True, verbose_name='Declination'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='right_ascension',
            field=models.CharField(blank=True, help_text='HH:MM:SS', max_length=15, null=True, verbose_name='Right Ascension'),
        ),
    ]
