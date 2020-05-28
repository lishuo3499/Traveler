from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request,'admin/index.html')

def p_manage(request):

    return render(request,'admin/p_manage.html')

def r_manage(request):

    return render(request,'admin/r_manage.html')

def u_manage(request):

    return render(request,'admin/u_manage.html')

def c_manage(request):
	print('ssss')
	return render(request,'admin/c_manage.html')

def e_manage(request):
	print('ssss')
	return render(request,'admin/e_manage.html')

def video_manage(request):
	print('ssss')
	return render(request,'admin/video_manage.html')

def music_manage(request):
	print('ssss')
	return render(request,'admin/music_manage.html')