from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserInfo(AbstractUser):  # 用户信息
    header_url = models.CharField(max_length=200, default='')  # 头像地址
    nick_name = models.CharField(max_length=200, default='')  # 昵称
    code_num  = models.CharField(max_length=200, default='')
    phone_num  = models.IntegerField( default=0)
    fav_num = models.IntegerField( default=0)		#收藏数，点赞后就收藏了
    opus_num = models.IntegerField( default=0)    #作品数
  
    is_fav_num = models.IntegerField( default=0)    #获赞数
    attention_num = models.IntegerField( default=0)    #关注人数
    fs_num = models.IntegerField( default=0)    #粉丝数
    def __str__(self):
        return self.username



        