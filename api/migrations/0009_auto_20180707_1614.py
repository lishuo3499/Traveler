# Generated by Django 2.0.4 on 2018-07-07 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180707_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='e',
            field=models.FloatField(default=-1, max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='s',
            field=models.FloatField(default=-1, max_length=100),
        ),
    ]
