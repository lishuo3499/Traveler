# Generated by Django 2.0.4 on 2018-07-08 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180707_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='send_time',
            field=models.IntegerField(default=1530080945, verbose_name='上传时间'),
        ),
    ]