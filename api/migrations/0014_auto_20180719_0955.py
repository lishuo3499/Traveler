# Generated by Django 2.0.4 on 2018-07-19 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20180717_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_url',
            field=models.CharField(default='', max_length=2000, verbose_name='视频地址'),
        ),
    ]
