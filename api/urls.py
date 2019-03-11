from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns  #api文档生成
from django.urls import path
from api import views as api_views


urlpatterns = [
    # url(r'^videofav/(?P<pk>[0-9]+)$', views.VideoFavDetail.as_view()),
    url(r'^index/$',api_views.index,name="index"),
    url(r'^del_like/$',api_views.del_like,name="del_like"),
    url(r'^video_comment/$',api_views.video_comment,name="video_comment"),
    # url(r'^attention_video_list/$',api_views.attention_video_list,name="attention_video_list"),
    url(r'^my_center_timeline/$',api_views.my_center_timeline,name="my_center_timeline"),   #个人中心时间轴
    url(r'^center_fav/$',api_views.center_fav,name="center_fav"),   #个人右边
    url(r'^friends_list/$',api_views.friends_list,name="friends_list"), 
    url(r'^all_center_fav/$',api_views.all_center_fav,name="all_center_fav"), 
    url(r'^add_friend/$',api_views.add_friend,name="add_friend"),   #添加好友
    url(r'^share_num/$',api_views.share_num,name="share_num"),
    url(r'^new_group/$',api_views.new_group,name="new_group"),
    url(r'^edit_group/$',api_views.edit_group,name="edit_group"),
    url(r'^delete_group/$',api_views.delete_group,name="delete_group"),
    url(r'^add_group/$',api_views.add_group,name="add_group"),
    url(r'^show_my_groups/$',api_views.show_my_groups,name="show__my_groups"),
    url(r'^add_or_not/$',api_views.add_or_not,name="add_or_not"),
    url(r'^show_one_group/$',api_views.show_one_group,name="show_one_group"),
    url(r'^show_one_group_user/$',api_views.show_one_group_user,name="show_one_group_user"),
    url(r'^delete_one_group_one_user/$',api_views.delete_one_group_one_user,name="delete_one_group_one_user"),
    url(r'^new_or_not/$',api_views.new_or_not,name="new_or_not"),
    url(r'^show_one_type_notice/$',api_views.show_one_type_notice,name="show_one_type_notice"),
    url(r'^set_new_to_old/$',api_views.set_new_to_old,name="set_new_to_old"),
    url(r'^show_notice_one/$',api_views.show_notice_one,name="show_notice_one"),
    url(r'^show_friend_video/$',api_views.show_friend_video,name="show_friend_video"),
    url(r'^upload_video/$',api_views.upload_video,name="upload_video"),
    url(r'^show_map_video/$',api_views.show_map_video,name="show_map_video"),

    url(r'^login_name/$',api_views.login_name,name="login_name"),
    
    url(r'^vali_code/$',api_views.vali_code,name="vali_code"),
    url(r'^getCode/$',api_views.getCode,name="getCode"),
    url(r'^set_user_info/$',api_views.set_user_info,name="set_user_info"),
    url(r'^change_user_info/$',api_views.change_user_info,name="change_user_info"),


     
]


urlpatterns = format_suffix_patterns(urlpatterns)  #api文档生成
