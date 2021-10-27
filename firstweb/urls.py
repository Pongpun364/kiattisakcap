"""firstweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include  #include คือการลิงก์โปรเจคกับเเอพเข้ากัน : path คือการทำให้เว็บเรามี url ย่อย
from . import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = [
	
	path('admin/', admin.site.urls), #localhost:8000/admin
	path('',include('Myapp.urls')), #localhost:8000
	path('login/', auth_views.LoginView.as_view(template_name = 'Myapp/login.html'), name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(template_name = 'Myapp/logout.html'), name = 'logout')
	# บรรทัดบนนี้เป็นการทำให้โปรเจคลิงก์กับ urls ของเเอป
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
