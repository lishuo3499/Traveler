from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter #api文档
from api import views, urls as apiurls   #导入api的url
from userInfo import views, urls as userurls   #导入api的url
from backstage import views, urls as backstage
router = DefaultRouter()






urlpatterns = [
    path('admin/', admin.site.urls),
 	path('', include(router.urls)),
 	path('api/',include(apiurls)),  #include api app下面的url.py
 	path('user/',include(userurls)),  #include api app下面的url.py
	path('backstage/',include(backstage)),
]
