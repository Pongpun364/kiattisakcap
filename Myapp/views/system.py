from typing import ItemsView
from django.db.models.fields import Field
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import random
from .htmx_views import *
from .order_views import *
from .product_views import *
from .system import *
from .user_views import *
from .utils import *



# HttpRespond คือฟังก์ชัน สำหรับโชว์ข้อความหน้าเว็บได้
def Home(request):
	product = Allproduct.objects.all().order_by("id").reverse()[:6] # ดึงข้อมูลออกมาทั้งหมด
	# preorder = Allproduct.objects.filter(quantity__lte=0)

	context = {'product':product}

				
	return render(request,'Myapp/home.html',context)
	# return HttpResponse('สวัสดีจร้าา <h1>HEllo World: </h1> <p>สบายดีมั้ยย </p>')

def About(request):
	return render(request,'Myapp/about.html')

def Contact(request):
	return render(request,'Myapp/contact.html')



def Register(request):
	context = {}
	if request.method == 'POST' :
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')
		# ยังไม่ได้ใส่ try except
		# alert ว่าอีเมลนี้เคยสมัครเเล้ว
		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		try:
			newuser.save()
			# สร้างโปรไฟล์อัตโนมัติ
			profile = Profile()
			profile.user = User.objects.get(username = email)
			profile.save()

			#from django.contrib.auth import authenticate, login   (ทำการ auto login)
			user = authenticate(username=email, password = password)
			login(request,user)

			return redirect('allproduct-page')
		except:
			context["user_fail"] = "true"
			return render(request, 'Myapp/register.html',context)

	return render(request, 'Myapp/register.html')

def checkEmail(request):
	context={}
	data = request.POST.copy().get("email")
	try:
		email = User.objects.get(username = data)
		context["checkMail"] = "False"

	except:
		context["checkMail"] = "Pass"
	
	context["return_email"] = data

	return render(request,"Myapp/htmx/email_register.html",context)
