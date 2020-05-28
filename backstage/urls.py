from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns  #api文档生成
from django.urls import path
from backstage import views as backstage


urlpatterns = [
   url(r'^index/$',backstage.index,name="index"),
   url(r'^pmanage/$',backstage.p_manage,name="pmanage"),
   url(r'^rmanage/$',backstage.r_manage,name="rmanage"),
   url(r'^umanage/$',backstage.u_manage,name="umanage"),
   url(r'^cmanage/$',backstage.c_manage,name="cmanage"),
   url(r'^emanage/$',backstage.e_manage,name="emanage"),
   url(r'^musicmanage/$',backstage.music_manage,name="musicmanage"),
   url(r'^videomanage/$',backstage.video_manage,name="videomanage"),
]


