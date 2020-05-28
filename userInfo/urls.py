from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns  #api文档生成
from django.urls import path
from userInfo import views as user_views


urlpatterns = [
    url(r'^my_center_data/$',user_views.my_center_data,name="my_center_data"),

]


urlpatterns = format_suffix_patterns(urlpatterns)  #api文档生成
