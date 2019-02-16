# Generated by Django 2.0.4 on 2018-07-08 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20180708_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lon', models.IntegerField(default=0, verbose_name='经度')),
                ('lat', models.IntegerField(default=0, verbose_name='纬度')),
                ('name', models.CharField(default='', max_length=500, verbose_name='name')),
                ('address', models.CharField(default='', max_length=500, verbose_name='address')),
            ],
        ),
        migrations.RemoveField(
            model_name='video',
            name='e',
        ),
        migrations.RemoveField(
            model_name='video',
            name='s',
        ),
        migrations.AlterField(
            model_name='video',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Position', verbose_name='Position'),
        ),
    ]
