# Generated by Django 2.0.4 on 2018-07-07 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_notice_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.CharField(max_length=1000, null=True)),
                ('traffic', models.CharField(max_length=1000, null=True)),
                ('stay', models.CharField(max_length=1000, null=True)),
                ('other', models.CharField(max_length=1000, null=True)),
                ('index', models.IntegerField(default=0, null=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Video')),
            ],
        ),
    ]
