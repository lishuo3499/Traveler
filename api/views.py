from django.shortcuts import render
from django.http import HttpResponse
from api.models import *
from userInfo.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import *
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import time
import os
import shutil
import random
import urllib.request
import urllib
class MyPageNumberPagination(PageNumberPagination):
	#每页显示多少个
	page_size = 10
	#默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
	page_size_query_param = "size"
	#最大页数不超过10
	max_page_size = 10
	#获取页码数的
	page_query_param = "page"


# 首页数据
@api_view(["GET",'POST'])
def index(request):
	user_id = request.GET.get("id")
	v = Video.objects.filter(permission=1)
	pg = MyPageNumberPagination()
	page_roles = pg.paginate_queryset(queryset=v,request=request)
	v = VideoSerializer(page_roles, many=True)
	return Response(v.data,status=status.HTTP_201_CREATED)


#添加好友
@api_view(["POST"])
def add_friend(request):
	delete_or_add = request.POST.get("delete_or_add")    #如果为0就是删除  为1就是添加
	user_id = request.POST.get("user_id")
	friend_id = request.POST.get("friend_id")
	print(delete_or_add,user_id,friend_id)
	if int(delete_or_add)==1:
		Friends.objects.create(self_user=UserInfo.objects.get(id=user_id),my_friend=UserInfo.objects.get(id=friend_id))
		send_notice(user_id,friend_id,"1",friend_id)
		return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)
	else:
		Friends.objects.filter(self_user=user_id,my_friend=friend_id).delete()
		Notice.objects.filter(
			receive_user=friend_id,
			send_user=user_id,
			notice_type="1",
			user_id = friend_id,
		).delete()
		return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)




# 添加赞（视频）
@api_view(["POST"])
def del_like(request):
	video_id = request.POST.get("id")
	user_id = request.POST.get("user_id")
	send_user_id = Video.objects.get(id=video_id).user_id
	del_bool = request.POST.get("del_like")
	v = Video.objects.get(id=video_id)
	if del_bool == '0':
		v.fav_num -= 1
		Video_Fav_user.objects.filter(video =video_id,user=user_id).delete()
		if int(user_id) != int(send_user_id):
			Notice.objects.filter(
				receive_user_id=send_user_id,
				send_user_id=user_id,
				notice_type="01",
				video_id=video_id,
			).delete()
	else:
		if len(Video_Fav_user.objects.filter(video=Video.objects.get(id=video_id),user=UserInfo.objects.get(id=user_id)))>0:  #已经点赞
			return Response({"msg":"已经点赞！"},status=status.HTTP_201_CREATED)
		v.fav_num += 1
		Video_Fav_user.objects.create(video=Video.objects.get(id=video_id),user=UserInfo.objects.get(id=user_id))
		if int(user_id) != int(send_user_id):
			send_notice(user_id,send_user_id,"01",video_id)
	v.save()
	return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)

@api_view(["POST"])
def share_num(request):
	video_id = request.POST.get("id")
	user_id = request.POST.get("user_id")
	send_user_id = Video.objects.get(id=video_id).user_id
	v = Video.objects.get(id=video_id)
	v.forwarding_num += 1
	if int(user_id) != int(send_user_id):
		send_notice(user_id,send_user_id,"03",video_id)
	v.save()
	return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)






#提交评论,评论数据（视频）
@api_view(["GET",'POST'])
def video_comment(request):
	if request.method == 'POST':
		video_id = request.POST.get("video_id")
		user_id = request.POST.get("user_id")
		comment = request.POST.get("comment")
		video_data =Video.objects.filter(id=video_id)
		video_data.update(comment_num=video_data[0].comment_num+1)  #评论数加1
		c = Comment.objects.create(video_id=video_id,user_id=user_id,comment=comment,created_time=time.time())
		admin_id = video_data[0].user_id
		print(admin_id)
		send_notice(user_id,admin_id,"4",c.id,video_id,content=comment)
		return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)
	elif request.method == 'GET':
		video_id_p = request.GET.get("video_id")
		page_p = int(request.GET.get("page"))
		comment = Comment.objects.filter(video_id=video_id_p)
		if page_p>len(comment)/6 and page_p!=1 :
			print('超出页数')
			return Response({'status':'last'},status=status.HTTP_201_CREATED)
		pg = MyPageNumberPagination()
		page_roles = pg.paginate_queryset(queryset=comment,request=request)
		comment = CommentSerializer(page_roles, many=True)
		return Response(comment.data,status=status.HTTP_201_CREATED)
	



#关注页面请求数据	
@api_view(["GET",'POST'])
def attention_video_list(request):
	user_id = request.GET.get("id")
	v = Video.objects.all()
	pg = MyPageNumberPagination()
	page_roles = pg.paginate_queryset(queryset=v,request=request)
	v = VideoSerializer(page_roles, many=True)
	for x in v.data:
		this_user_fav_or_not = Video_Fav_user.objects.filter(is_attented =x['id'],self_user=user_id)
		this_user_attention_or_not = Attention.objects.filter(is_attented =x['user']['id'],self_user=user_id)
		if len(this_user_fav_or_not)>0:
			x['this_user_fav_or_not'] = '1'
		if len(this_user_attention_or_not)>0:
			x['this_user_attention_or_not'] = '1'
	return Response(v.data,status=status.HTTP_201_CREATED)




#时间轴和我的喜欢
@api_view(["GET"])
def my_center_timeline(request):
	user_id = request.GET.get("id")
	v = Video.objects.filter(user_id =	user_id ).order_by("-id")
	pg = MyPageNumberPagination()
	page_roles = pg.paginate_queryset(queryset=v,request=request)
	v = VideoSerializer(page_roles, many=True)
	return Response(v.data,status=status.HTTP_201_CREATED)




#个人中心点赞
@api_view(["GET"])
def center_fav(request):
	user_id = request.GET.get("user_id")
	v = Video_Fav_user.objects.filter(user_id =	user_id )
	pg = MyPageNumberPagination()
	page_roles = pg.paginate_queryset(queryset=v,request=request)
	v = Video_Fav_userSerializer(page_roles, many=True)
	return Response(v.data,status=status.HTTP_201_CREATED)



# 全局判断全部点赞数据和关注了所有好友的数据
@api_view(["GET"])
def all_center_fav(request):
	all_fav_friend = []
	user_id = request.GET.get("user_id")
	v = Video_Fav_user.objects.filter(user_id =	user_id )
	v = Video_Fav_userSerializer(v, many=True)
	friend = Friends.objects.filter(self_user =	user_id )
	friend = FriendsSerializer(friend, many=True)
	all_fav_friend.append(friend.data)
	all_fav_friend.append(v.data)
	return Response(all_fav_friend,status=status.HTTP_201_CREATED)




#好友列表
@api_view(["GET"])
def friends_list(request):
	user_id = request.GET.get("user_id")
	friend = Friends.objects.filter(self_user =	user_id )
	friend = FriendsSerializer(friend, many=True)
	return Response(friend.data,status=status.HTTP_201_CREATED)


#新建群
@api_view(["POST",'GET'])
def new_group(request):
	name = request.POST.get("name")
	desc = request.POST.get("desc")
	user_id = request.POST.get("user_id")
	user = UserInfo.objects.get(id=user_id)
	img_url =request.FILES.get('img_url')
	print()
	new_Group = Group(
	name=name,
	desc=desc,
	img_url =img_url,
	img_name = img_url.name
	)
	new_Group.save()
	# group = Group.objects.create(name=name,desc=desc,img_url=img_url)
	UserGroup.objects.create(user=user,group=new_Group,cancan=0)
	shutil.move("C:\\Users\\Administrator\\Desktop\\APP\\Traveler\\media\\media\\group_header_img\\%s"%(img_url.name),"C:\\nginx-1.14.0\\html\\html\\group_header_img\\media")
	print(img_url.name)
	return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)

#修改群信息
@api_view(["POST"])
def edit_group(request):
	user_id = request.POST.get("user_id")
	group_id = request.POST.get("group_id")
	user_group = UserGroup.objects.filter(user_id=user_id,group_id=group_id,cancan=0)
	if user_group.exists():
		name = request.POST.get("name")
		desc = request.POST.get("desc")
		img_url = request.POST.get("img_url")
		group = Group.objects.filter(id=group_id)
		group.update(name=name,desc=desc,img_url=img_url)
		return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)
	else:
		return Response({"msg":"无权访问！"})

#删除群
@api_view(["POST"])
def delete_group(request):
	user_id = request.POST.get("user_id")
	group_id = request.POST.get("group_id")
	user_group = UserGroup.objects.filter(user_id=user_id,group_id=group_id,cancan=0)
	if user_group.exists():
		Group.objects.filter(id=group_id).delete()
		return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)
	else:
		return Response({"msg":"无权访问！"})

#申请加群
@api_view(["POST"])
def add_group(request):
	group_id = request.POST.get("group_id")
	user_id = request.POST.get("user_id")
	content = request.POST.get("content")
	user_group = Group.objects.filter(id=group_id)
	if user_group.exists():
		send_notice(user_id,UserGroup.objects.get(group_id=group_id,cancan=0).user_id,"2",group_id,content=content)
		return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)
	else:
		return Response({"msg":"群不存在！"})

#群主是否同意加群
@api_view(["POST"])
def add_or_not(request):
	notice_id = request.POST.get("notice_id")
	user_id = request.POST.get("user_id")
	notice = Notice.objects.get(id=notice_id)
	if int(notice.receive_user_id) == int(user_id):
		add_bool = request.POST.get("add_bool")
		if int(add_bool) == 1:
			UserGroup.objects.create(group_id=notice.other_id,user_id=notice.send_user_id)
			return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)
		else:
			send_notice(user_id,notice.send_user_id,"5",notice.group_id)
			return Response({"msg":"通过失败！"})

# 展示用户所有的群
@api_view(["GET"])
def show_my_groups(request):
	user_id = request.GET.get("user_id")
	group = UserGroup.objects.filter(user_id=user_id)
	group_list = []
	for i in group:
		group_list.append(i.group)
	group_list = GroupSerializer(group_list,many=True)
	return Response(group_list.data,status=status.HTTP_201_CREATED)

# 展示某一个群
@api_view(["GET"])
def show_one_group(request):
	group_id = request.GET.get("group_id")
	group = Group.objects.get(id=group_id)
	group = GroupSerializer(group)
	return Response(group.data,status=status.HTTP_201_CREATED)

# 展示一个群所有的用户
@api_view(["GET"])
def show_one_group_user(request):
	group_id = request.GET.get("group_id")
	user_list = UserGroup.objects.filter(group_id=group_id)
	new_user_list = []
	for i in user_list:
		new_user_list.append(i.user)
	new_user_list = UserInfoSerializer(new_user_list,many=True)
	return Response(new_user_list.data,status=status.HTTP_201_CREATED)

# 群主删除某个用户
@api_view(["POST"])
def delete_one_group_one_user(request):
	admin_id = request.POST.get("admin_id")
	user_id = request.POST.get("user_id")
	group_id = request.POST.get("group_id")
	user_group = UserGroup.objects.filter(group_id=group_id,user_id=admin_id,cancan=0)
	if user_group.exists():
		UserGroup.objects.get(user_id=user_id,group_id=group_id).delete()
		return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)
	else:
		return Response({"msg":"无权操作！"})

def send_notice(send_user_id,receive_user_id,notice_type,other_id,obj_id=1,content=""):
	notice = Notice.objects.create(
				content=content,
				send_user=UserInfo.objects.get(id=send_user_id),
				receive_user=UserInfo.objects.get(id=receive_user_id),
				notice_type=notice_type,
				created_time=time.time(),
				updated_time=time.time(),
				status = 0,#0未读
			)
	if notice_type == "01" or notice_type == "31": #点赞视频或者分享视频
		notice.video = Video.objects.get(id=other_id)
	elif notice_type == "02" or notice_type == "32": #点赞游记或者分享游记
		notice.travels_note = TravelsNote.objects.get(id=other_id)
	elif notice_type == "1" or notice_type == "33": #关注或者分享某人
		notice.user = UserInfo.objects.get(id=other_id)
	elif notice_type == "2" or notice_type == "5": #申请加群或者拒绝加群
		notice.group = Group.objects.get(id=other_id)
	elif notice_type == "4":
		notice.comment = Comment.objects.get(id=other_id)
		notice.video = Video.objects.get(id=obj_id)
	notice.save()


#判断是否存在着新消息
@api_view(["GET"])
def new_or_not(request):
	user_id = request.GET.get("user_id")
	fav_num = Notice.objects.filter(receive_user_id=user_id,notice_type__startswith="0",status=0).count()
	attention_num = Notice.objects.filter(receive_user_id=user_id,notice_type="1",status=0).count()
	add_group_num = Notice.objects.filter(receive_user_id=user_id,notice_type="2",status=0).count()
	share_num = Notice.objects.filter(receive_user_id=user_id,notice_type__startswith="3",status=0).count()
	comment_num = Notice.objects.filter(receive_user_id=user_id,notice_type="4",status=0).count()
	not_accept_num = Notice.objects.filter(receive_user_id=user_id,notice_type="5",status=0).count()
	return Response({"点赞次数":fav_num,"关注次数":attention_num,"加群次数":add_group_num,"分享次数":share_num,"评论次数":comment_num,"拒绝次数":not_accept_num},status=status.HTTP_201_CREATED)

#展示某一类的通知信息
@api_view(["GET"])
def show_one_type_notice(request):
	user_id = request.GET.get("user_id")
	type_notice = request.GET.get("type_notice")
	notice = Notice.objects.filter(receive_user_id=user_id,notice_type__startswith=type_notice)
	data = notice.order_by("-updated_time")
	data = NoticeSerializer(data,many=True)
	return Response(data.data,status=status.HTTP_201_CREATED)

#设置消息为已读
@api_view(["POST"])
def set_new_to_old(request):
	user_id = request.POST.get("user_id")
	type_notice = request.POST.get("type_notice")
	notice = Notice.objects.filter(receive_user_id=user_id,notice_type__startswith=type_notice)
	notice.update(status=1,updated_time=time.time())
	return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)

#展示一个通知的详细信息
@api_view(["GET"])
def show_notice_one(request):
	notice_id = request.GET.get("notice_id")
	notice = Notice.objects.get(id=notice_id)
	notice = NoticeSerializer(notice)
	return Response(notice.data,status=status.HTTP_201_CREATED)

def new_strategy(video_id,food="",traffic="",stay="",other="",index=0):
	Strategy.objects.create(
		video = Video.objects.get(id=video_id),
		food = food,
		traffic = traffic,
		stay = stay,
		other = other,
		index = index
	)


#展示用户关注的人的视频
@api_view(["GET"])
def show_friend_video(request):
	user_id = request.GET.get("user_id")
	friends_array = []
	friends = Friends.objects.filter(self_user_id=user_id)
	for i in friends:
		friends_array.append(i.my_friend_id)
	videos = Video.objects.filter(user_id__in=friends_array).order_by("-send_time")
	videos = VideoSerializer(videos,many=True)
	# videos = videos.order_by("send_time")
	# return Response(videos,status=status.HTTP_201_CREATED)
	return Response(videos.data,status=status.HTTP_201_CREATED)

#展示附近视频
@api_view(["GET"])
def show_map_video(request):
	s = float(request.GET.get("s"))
	e = float(request.GET.get("e"))
	video = Video.objects.filter(e__gte=e-1,s__gte=s-1,e__lte=e+1,s__lte=s+1)
	video = VideoSerializer(video,many=True)
	return  Response(video.data,status=status.HTTP_201_CREATED)
# @api_view(["GET"])
# def search_group(request):
# 	group_name =request.GET.get('group_name')
# 	print(group_name)
# 	search_data = Group.objects.filter(name__contains=group_name)
# 	search_datas = GroupSerializer(search_data,many=True)
# 	return Response(search_datas.data,status=status.HTTP_201_CREATED)

# @api_view(["GET"])
# def manager_id(request):
# 	group_id =request.GET.get('group_id')
# 	manager_data = UserGroup.objects.filter(group=group_id)
# 	manager_data = UserGroupSerializer(manager_data,many=True)
# 	return Response(manager_data.data,status=status.HTTP_201_CREATED)
# 	@api_view(["GET"])
# def search_group(request):
# 	search = {}
# 	usergroup = []
# 	all_data = []
# 	group_name =request.GET.get('group_name')
# 	search_data = Group.objects.filter(name__contains=group_name)
# 	for x in search_data:
# 		json_data = serializers.serialize('json', UserGroup.objects.filter(group_id=x.id))
# 		json_data = json.loads(json_data)
# 		usergroup.append(json_data)
# 	search_datas = GroupSerializer(search_data,many=True)
# 	search['group'] = search_datas.data
# 	search['user'] = usergroup
# 	return Response(search,status=status.HTTP_201_CREATED)

from django.views.decorators.csrf import csrf_exempt
@api_view(["POST"])
@csrf_exempt
def upload_video(request):
	file_name = int(time.time())
	random_num = random.randint(0, 10000)
	desc = request.POST.get("desc")
	lon = float(request.POST.get("lon"))
	lat = float(request.POST.get("lat"))
	name = request.POST.get("name")
	address = request.POST.get("address")
	permission = request.POST.get("permission")
	user_id = request.POST.get("user_id")
	music_id = request.POST.get("music_id")
	travelsnote_id = request.POST.get("travelsnote_id")
	food = request.POST.get("food")
	traffic = request.POST.get("traffic")
	docm = request.POST.get("docm")
	video = request.FILES.getlist('file')
	video[0].name = '%s%s.mp4'%(file_name,random_num)
	video[1].name = '%s%s.png'%(file_name,random_num)
	print(int(time.time()))
	position =Position.objects.create(
		lon = lon,
		lat = lat,
		name = name,
		address = address
		)
	new_img = Video(
		video_file=video[0],
		image_file = video[1]
	)
	new_img.video_url = 'http://linke.xtu.edu.cn/html/video/'+video[0].name
	new_img.image_url = 'http://linke.xtu.edu.cn/html/image/'+video[1].name
	new_img.desc = desc
	new_img.position = position
	new_img.send_time = time.time()
	new_img.permission = permission
	new_img.user_id = user_id
	new_img.music_id = music_id
	new_img.food = food
	new_img.traffic = traffic
	new_img.docm = docm
	new_img.travelsnote_id = travelsnote_id
	new_img.save()
	shutil.move("C:\\Users\\Administrator\\Desktop\\APP\\Traveler\\media\\media\\video\\%s"%(video[0].name),"C:\\nginx-1.14.0\\html\\html\\video")
	shutil.move("C:\\Users\\Administrator\\Desktop\\APP\\Traveler\\media\\media\\img\\%s"%(video[1].name),"C:\\nginx-1.14.0\\html\\html\\image")
	return Response({"msg":"操作成功！"},status=status.HTTP_201_CREATED)



from django.contrib.auth import authenticate, login, logout  # 用户
@api_view(["POST","GET"])
def login_name(request):
    username = request.GET['phone']
    password = request.GET['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        user_data = UserInfoSerializer(user).data
        return Response({'status':0,'msg':'登陆成功','user':user_data})
    else:
        return Response({'status':1,'msg':'登陆失败'})



# 发送验证码
@api_view(["POST","GET"])
def getCode(request):
    if request.method == 'GET':
        username = request.GET['username']
        code = random.randint(1000, 9000)  # 验证码
        url = 'http://118.24.53.130/SUBMAIL_PHP_SDK/SUBMAIL_PHP_SDK/demo/message_xsend_demo.php?phone=%s&code=%s' % (
            username, code)
        req = urllib.request.Request(url=url)
        res_data = urllib.request.urlopen(req)
        userinfo = UserInfo.objects.filter(username=request.GET['username'])
        if len(userinfo) == 0:  # 用户不存在时直接新建用户 发送验证码
            user = UserInfo.objects.create_user(
                username=username,
                code_num=code,
                password='pbkdf2_sha256$100000$go5krpSu9bOA$m2QgM1q0CuYTG7uPcGnJ6+OOTiQSLfX9VvKNSge7LiY='
            )
            return Response({'status':1,'msg':'发送成功'})
        else:  # 用户存在时直接修改验证码  并发送
            userinfo[0].code_num = code
            
            userinfo[0].save()
            return Response({'status':0,'msg':'发送成功'})




@api_view(["POST","GET"])
def vali_code(request):
    if request.method == 'GET':
        username = request.GET['phone']
        code = request.GET['code']
        userinfo = UserInfo.objects.filter(username=request.GET['phone'])
        if userinfo[0].code_num == code:  # 判断验证码是否正确
        	if  userinfo[0].nick_name=='' or userinfo[0].header_url==0:
        		return Response({'status':2,'msg':'验证码正确,头像昵称未设置'})
        	else:
        		user = authenticate(username=username,password=userinfo[0].first_name)
        		login(request, user)
        		user_data = UserInfoSerializer(user).data
        		return Response({'status':1,'msg':'验证码正确','user':user_data})
        else:
            return Response({'status':0,'msg':'验证码不正确'})
        return HttpResponse(random.randint(1000, 9000))


@api_view(["POST","GET"])
def set_user_info(request):
    if request.method == 'POST':
        username = request.POST['phone']
        password = request.POST['password']
        nicheng = request.POST['nicheng']
        header_url = request.POST['header_url']
        print(request.POST)
        userinfo = UserInfo.objects.filter(username=username)[0]
        userinfo.set_password(password)
        userinfo.nick_name = nicheng
        userinfo.header_url = header_url
        userinfo.first_name = password
        userinfo.save()
        user = authenticate(username=username,password=password)
        login(request, user)
        user_data = UserInfoSerializer(user).data
        return Response({'status':1,'msg':'修改完成','user':user_data})



@api_view(["POST","GET"])
def change_user_info(request):
    if request.method == 'POST':
        birth = request.POST['birth']
        user_id = request.POST['id']
        sex = request.POST['sex']
        nicheng = request.POST['nicheng']
        desc = request.POST['desc']
        header_url = request.POST['header_url']
        print(request.POST)
        userinfo = UserInfo.objects.filter(id=user_id)[0]
        userinfo.nick_name = nicheng
        userinfo.header_url = header_url
        userinfo.birth = birth
        userinfo.sex = sex
        userinfo.desc = desc
        userinfo.save()
        user = authenticate(username=userinfo.username,password=userinfo.first_name)
        login(request, user)
        user_data = UserInfoSerializer(user).data
        return Response({'status':1,'msg':'修改完成','user':user_data})
   



 # user = authenticate(username=username,
 #                                password='pbkdf2_sha256$100000$go5krpSu9bOA$m2QgM1q0CuYTG7uPcGnJ6+OOTiQSLfX9VvKNSge7LiY=')
 #            if user is not None:
 #                user.set_password(password1)
 #                user.save()









































