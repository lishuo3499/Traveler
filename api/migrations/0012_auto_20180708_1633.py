# Generated by Django 2.0.4 on 2018-07-08 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180708_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='lat',
            field=models.FloatField(default=0, verbose_name='纬度'),
        ),
        migrations.AlterField(
            model_name='position',
            name='lon',
            field=models.FloatField(default=0, verbose_name='经度'),
        ),
    ]
