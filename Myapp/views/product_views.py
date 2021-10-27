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

from .htmx_views import *
from .order_views import *
from .product_views import *
from .system import *
from .user_views import *
from .utils import *


def Addproduct(request):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')



	if request.method == 'POST' and request.FILES['Imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		Imageurl = data.get('Imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')
		# Image = data.get('Image')

		new = Allproduct()
		new.name = name
		new.price = price
		new.detail = detail
		new.Imageurl = Imageurl
		new.quantity = quantity
		new.unit = unit
		###########################################
		image_file = request.FILES['Imageupload']
		image_file_name = request.FILES['Imageupload'].name.replace(' ','')
		print('FILE_IMAGE : ',image_file)
		print('FILE_IMAGE_NAME : ',image_file_name)
		fs = FileSystemStorage()
		filename = fs.save(image_file_name,image_file)
		upload_file_url = fs.url(filename)
		new.Image = upload_file_url[6:]
		###########################################
		new.save()

	return render(request,'Myapp/addproduct.html')


def Product(request):

	print("messenger is coming to town",request.session.get('mes_id'))
	product = Allproduct.objects.all().order_by("id").reverse() # ดึงข้อมูลออกมาทั้งหมด
	paginator = Paginator(product,6) # หนึ่งหน้าโชว์เเค่ 3 ชิ้นเท่านั้น
	page = request.GET.get('page') # http://127.0.0.1:8000/allproduct/?page=2
	product = paginator.get_page(page)
	# currentpath = (request.path).replace('/','_')
	context = {'product':product}
	
	return render(request,'Myapp/allproduct.html',context)

def ProductDetail(request,productid):
	product = Allproduct.objects.get(id = productid)
	context = {'product':product}

	######## check user device ########
	keywords = ['Mobile','Opera Mini','Android']
	user_agent = request.META['HTTP_USER_AGENT']
	if any(word in user_agent for word in keywords):
		print('Visitor is on mobile device')
		return render(request,'Myapp/mobile/productdetail_mobile.html',context)
	else:
		print('Visitor is on desktop')
		return render(request,'Myapp/productdetail.html',context)



@login_required
def EditProduct(request,productid):
	
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	
	product = Allproduct.objects.get(id = productid)
	category = Category.objects.all()
	if request.method == 'POST' :
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		Imageurl = data.get('Imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')
		cat = data.get('category')
		catt = Category.objects.get(catname = cat)  #### เราไม่สามารถเซฟ catname ในขณะที่ยังใช้ instance เป็น Allproduct อยู่ !!!!!
		instock = data.get('instock')				### Foreignkey ต้องกลับไปหาเจ้าของมันก่อนนนน !!!

		# Image = data.get('Image')

	
		product.name = name
		product.price = price
		product.detail = detail
		product.Imageurl = Imageurl
		product.quantity = quantity
		product.unit = unit
		product.catname = catt
		if instock == 'instock_True':
			product.instock = True
		else:
			product.instock = False


		######################################## SAVE IMAGE ###################################
		if 'Imageupload' in request.FILES:
			# image_file = request.FILES['Imageupload']
			# image_file_name = request.FILES['Imageupload'].name.replace(' ','')
			# print('FILE_IMAGE : ',image_file)
			# print('FILE_IMAGE_NAME : ',image_file_name)
			# fs = FileSystemStorage()
			# filename = fs.save(image_file_name,image_file)
			# upload_file_url = fs.url(filename)
		
			# product.Image = upload_file_url[6:]
			
			product.Image = request.FILES['Imageupload']
		else:
			print("No fucking file !!!")
		#######################################################################################
		product.save()


	product = Allproduct.objects.get(id = productid)
	context = {'product':product,'category':category}

	return render(request,'Myapp/editproduct.html',context)

def ProductCat(request,code):
	### เป็นเเค่ฟังก์ชัน ที่รองรับลิงก์ที่กดมาจากหน้า allcategory.html
	select = Category.objects.get(id=code)
	product = Allproduct.objects.filter(catname=select).order_by("id").reverse() # ดึงข้อมูลออกมาทั้งหมด
	paginator = Paginator(product,6) # หนึ่งหน้าโชว์เเค่ 3 ชิ้นเท่านั้น
	page = request.GET.get('page') # http://127.0.0.1:8000/allproduct/?page=2
	product = paginator.get_page(page)

	# path = str(currentpath.split('/'))

	# page = path.split('/')[1]
	# number = path.split('/')[2]
	
	context = {'product':product,"catname":select.catname}
	# context = {'product':product,"catname":select.catname}
	return render(request,'Myapp/allproductcat.html',context)


