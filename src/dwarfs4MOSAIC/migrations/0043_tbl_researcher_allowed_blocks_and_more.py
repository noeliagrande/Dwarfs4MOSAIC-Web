# Generated by Django 5.1.5 on 2025-07-12 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwarfs4MOSAIC', '0042_alter_tbl_observing_block_seeing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_researcher',
            name='allowed_blocks',
            field=models.ManyToManyField(blank=True, related_name='allowed_researchers', to='dwarfs4MOSAIC.tbl_observing_block'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='datafiles_path',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='Data files path'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='image',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='magnitude',
            field=models.FloatField(blank=True, help_text='Referenced to Vega System', null=True, verbose_name='Magnitude'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tbl_target',
            name='type',
            field=models.CharField(choices=[('galaxy_image', 'Galaxy image'), ('galaxy_spectrum', 'Galaxy spectrum'), ('standard_image', 'Standard image'), ('standard_spectrum', 'Standard spectrum'), ('calibration', 'Calibration'), ('other', 'Other')], default='galaxy', max_length=20, verbose_name='Type'),
        ),
    ]
