from rest_framework import serializers
from api.models import *
from userInfo.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserInfo
		fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Position
		fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()
	position =	PositionSerializer()		
	class Meta:
		model = Video
		fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()
	class Meta:
		model = Comment
		fields = '__all__'



# 个人中心个人收藏序列化器
class Video_User_center_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Video
		fields = '__all__'

class Video_Fav_userSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()
	video = Video_User_center_Serializer()
	class Meta:
		model = Video_Fav_user
		fields = '__all__'


class FriendsSerializer(serializers.ModelSerializer):
	# self_user = UserInfoSerializer()
	my_friend = UserInfoSerializer()
	class Meta:
		model = Friends
		fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer()
	class Meta:
		model = UserGroup
		fields = '__all__'

class Notice_CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
class NoticeSerializer(serializers.ModelSerializer):
	send_user = UserInfoSerializer()
	video = VideoSerializer()
	# travels_note
	user = UserInfoSerializer()
	# music
	group = GroupSerializer()
	class Meta:
		model = Notice
		fields = '__all__'

