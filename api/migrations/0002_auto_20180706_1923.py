# Generated by Django 2.0.4 on 2018-07-06 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='img_name',
            field=models.ImageField(default='', max_length=500, upload_to=''),
        ),
        migrations.AlterField(
            model_name='group',
            name='img_url',
            field=models.ImageField(upload_to='media/group_header_img'),
        ),
    ]
