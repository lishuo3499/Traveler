from django.db import models
from datetime import datetime
from userInfo.models import UserInfo

# 音乐
class Music(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,null=False) # 上传人
    name = models.CharField(verbose_name='音乐名称', max_length=50, null=True) #名字
    desc = models.CharField(max_length=500,null=True) #描述
    image_url = models.CharField(max_length=500,null=True) #封面图
    music_url = models.CharField(verbose_name='音乐地址', max_length=500, null=True) #地址
    created_time = models.IntegerField(null=False,default=1530080945) #上传时间

# 游记
class TravelsNote(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50,null=False)
    desc = models.CharField(max_length=5000,null=True)
    permission = models.CharField(choices=(('private', u'仅对自己可见'), ('common', u'全部可见'), ('part_visual', '部分可见')),
                                  max_length=20, default='private', verbose_name='权限')
    image_url = models.CharField(max_length=200, default='', verbose_name='图片地址')
    created_time = models.IntegerField(default=1530080945,verbose_name='创建时间')
    updated_time = models.IntegerField(default=1530080945,verbose_name='最后编辑时间')

class Position(models.Model):
    lon = models.FloatField(default=0, verbose_name='经度')
    lat = models.FloatField(default=0, verbose_name='纬度')
    name = models.CharField(max_length=500, verbose_name='name', default='')
    address = models.CharField(max_length=500, verbose_name='address', default='')
# 视频信息
class Video(models.Model):
    permission = models.CharField(choices=(('private', u'仅对自己可见'), ('common', u'全部可见'), ('part_visual', '部分可见')),
                                  max_length=20, default='private', verbose_name='权限')
    video_url = models.CharField(max_length=2000, default='', verbose_name='视频地址')
    image_url = models.CharField(max_length=1000, default='', verbose_name='头像地址')
    send_time = models.IntegerField(default=1530080945, verbose_name='上传时间')
    user = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE, null=True, )
    category = models.CharField(max_length=20, verbose_name='标签', default='')
    fav_num = models.IntegerField(verbose_name='点赞数', default=0)
    comment_num = models.IntegerField(verbose_name='评论数', default=0)
    forwarding_num = models.IntegerField(verbose_name='转发数', default=0)
    desc = models.CharField(max_length=500, verbose_name='描述', default='')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, default='')
    travelsnote = models.ForeignKey(TravelsNote, on_delete=models.CASCADE, null=True)
    this_user_fav_or_not = models.CharField(max_length=20, verbose_name=u'位置', default='0')
    this_user_attention_or_not= models.CharField(max_length=20, verbose_name=u'位置', default='0')
    position = models.ForeignKey(Position, verbose_name='Position', on_delete=models.CASCADE, null=True, )
    video_file = models.FileField(max_length=200, default='', upload_to='media/video')
    image_file = models.FileField(max_length=1000, default='', upload_to='media/img')
    food = models.CharField(max_length=500, verbose_name='美食', default='')
    traffic = models.CharField(max_length=500, verbose_name='交通', default='')
    docm = models.CharField(max_length=500, verbose_name='住宿', default='')




# 视频评论
class Comment(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video,on_delete=models.CASCADE,null=True)
    travels_note = models.ForeignKey(TravelsNote,on_delete=models.CASCADE,null=True)
    comment = models.CharField(max_length=500, verbose_name='评论', default='')
    fav_num = models.IntegerField(default=0, verbose_name='评论点击数')
    created_time = models.IntegerField(default=1530080945)   #时间戳

#点赞关系表
class Video_Fav_user(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='video_fav_user_self')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_fav_user',null=True)
    travels_note = models.ForeignKey(TravelsNote,on_delete=models.CASCADE,null=True)
    music = models.ForeignKey(Music,on_delete=models.CASCADE,null=True)

#关注表
class Friends(models.Model):
    self_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='self_user',null=True)
    my_friend = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='my_friend',null=True)


# 用户群
class Group(models.Model):
    name = models.CharField(max_length=20,null=False)
    desc = models.CharField(max_length=500,null=False)
    img_url = models.ImageField(upload_to='media/group_header_img')
    img_name = models.ImageField(max_length=500,null=False,default='')

#用户群关系表
class UserGroup(models.Model):
    user = models.ForeignKey(UserInfo,null=False,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,null=False,on_delete=models.CASCADE)
    cancan = models.IntegerField(default=2,null=False) #0为群主，1为管理员，2为普通成员


#通知消息
class Notice(models.Model):
    content = models.CharField(max_length=500,null=True)
    send_user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,related_name='send_user')
    receive_user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,related_name='receive_user')
    notice_type = models.CharField(max_length=20,null=False)
    video = models.ForeignKey(Video,on_delete=models.CASCADE,null=True)
    travels_note = models.ForeignKey(TravelsNote,on_delete=models.CASCADE,null=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,null=True)
    music = models.ForeignKey(Music,on_delete=models.CASCADE,null=True)
    group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True)
    status = models.IntegerField(null=False,default=0) #0为未读，1为已读
    created_time = models.IntegerField(null=True,default=1530080945)
    updated_time = models.IntegerField(null=True,default=1530080945)
    #评论还没做，之后改了评论在开始

class Strategy(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE,null=False)
    food = models.CharField(max_length=1000,null=True)
    traffic = models.CharField(max_length=1000,null=True)
    stay = models.CharField(max_length=1000,null=True)
    other = models.CharField(max_length=1000,null=True)
    index = models.IntegerField(default=0,null=True)
