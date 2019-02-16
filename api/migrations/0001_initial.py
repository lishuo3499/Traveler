# Generated by Django 2.0.4 on 2018-07-05 08:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(default='', max_length=500, verbose_name='评论')),
                ('fav_num', models.IntegerField(default=0, verbose_name='评论点击数')),
                ('created_time', models.IntegerField(default=1530080945)),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_friend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_friend', to=settings.AUTH_USER_MODEL)),
                ('self_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('desc', models.CharField(max_length=500)),
                ('img_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, verbose_name='音乐名称')),
                ('desc', models.CharField(max_length=500, null=True)),
                ('image_url', models.CharField(max_length=500, null=True)),
                ('music_url', models.CharField(max_length=500, null=True, verbose_name='音乐地址')),
                ('created_time', models.IntegerField(default=1530080945)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500, null=True)),
                ('notice_type', models.CharField(max_length=20)),
                ('status', models.IntegerField(default=0)),
                ('created_time', models.IntegerField(default=1530080945, null=True)),
                ('updated_time', models.IntegerField(default=1530080945, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Group')),
                ('music', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Music')),
                ('receive_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive_user', to=settings.AUTH_USER_MODEL)),
                ('send_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TravelsNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=5000, null=True)),
                ('permission', models.CharField(choices=[('private', '仅对自己可见'), ('common', '全部可见'), ('part_visual', '部分可见')], default='private', max_length=20, verbose_name='权限')),
                ('image_url', models.CharField(default='', max_length=200, verbose_name='图片地址')),
                ('created_time', models.IntegerField(default=1530080945, verbose_name='创建时间')),
                ('updated_time', models.IntegerField(default=1530080945, verbose_name='最后编辑时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancan', models.IntegerField(default=2)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('private', '仅对自己可见'), ('common', '全部可见'), ('part_visual', '部分可见')], default='private', max_length=20, verbose_name='权限')),
                ('video_url', models.CharField(default='', max_length=200, verbose_name='视频地址')),
                ('image_url', models.CharField(default='', max_length=1000, verbose_name='头像地址')),
                ('send_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='上传时间')),
                ('category', models.CharField(default='', max_length=20, verbose_name='标签')),
                ('fav_num', models.IntegerField(default=0, verbose_name='点赞数')),
                ('comment_num', models.IntegerField(default=0, verbose_name='评论数')),
                ('forwarding_num', models.IntegerField(default=0, verbose_name='转发数')),
                ('desc', models.CharField(default='', max_length=500, verbose_name='描述')),
                ('position', models.CharField(default='', max_length=20, verbose_name='位置')),
                ('this_user_fav_or_not', models.CharField(default='0', max_length=20, verbose_name='位置')),
                ('this_user_attention_or_not', models.CharField(default='0', max_length=20, verbose_name='位置')),
                ('s', models.CharField(default='-1', max_length=100)),
                ('e', models.CharField(default='-1', max_length=100)),
                ('music', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='api.Music')),
                ('travelsnote', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TravelsNote')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Video_Fav_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Music')),
                ('travels_note', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TravelsNote')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_fav_user_self', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_fav_user', to='api.Video')),
            ],
        ),
        migrations.AddField(
            model_name='notice',
            name='travels_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TravelsNote'),
        ),
        migrations.AddField(
            model_name='notice',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notice',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Video'),
        ),
        migrations.AddField(
            model_name='comment',
            name='travels_note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TravelsNote'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Video'),
        ),
    ]
