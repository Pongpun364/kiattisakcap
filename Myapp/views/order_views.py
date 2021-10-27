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
from django.db.models import Q
from . mytils import *

def Myorder_detail(request,orderid):

	context = {}
	if request.user.is_authenticated:

		username = request.user.username
		admin_auth = request.user.profile.usertype
		user = User.objects.get(username = username)
		# usertype = Profile.objects.filter(usertype = username)
		order = Orderpending.objects.get(orderid=orderid)

		if  admin_auth != 'admin' and user != order.user:
			return redirect('allproduct-page')

		
		odlist = Orderlist.objects.filter(orderid = orderid)
		for img in odlist:
			product = Allproduct.objects.get(id=int(img.productid))
			img.Image = product.Image.url
		
		
		Sum_total = sum([ c.total for c in odlist ])

		## shipcost calculated
		order.total = Sum_total	

		# คิดค่าจัดส่งวินค้าตามจำนวนชิ้น 
		count = sum([ i.quantity for i in odlist])
		# คำนวณค่าส่งตามประเภทการส่ง
		
		if order.shipping == 'ems':
			shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
			# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
		else:
			shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
			# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
		
		if order.payment == 'cod':
			shipcost +=20
		order.shipcost = shipcost

		context = {'order':order,'odlist':odlist,'count':count}
	else:
		
		mes_id = request.session.get('mes_id')
		print("mes_id  ",mes_id)
		order = Orderpending.objects.get(orderid=orderid)
		# print("orderlistpage",csrftoken)
			
		if mes_id == order.mid:
			pass
		else:
			return redirect('allproduct-page')



		odlist = Orderlist.objects.filter(orderid = orderid)
		for img in odlist:
			product = Allproduct.objects.get(id=int(img.productid))
			img.Image = product.Image.url
		
		
		Sum_total = sum([ c.total for c in odlist ])

		## shipcost calculated
		order.total = Sum_total	

		# คิดค่าจัดส่งวินค้าตามจำนวนชิ้น 
		count = sum([ i.quantity for i in odlist])
		# คำนวณค่าส่งตามประเภทการส่ง
		
		if order.shipping == 'ems':
			shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
			# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
		else:
			shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
			# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
		
		if order.payment == 'cod':
			shipcost +=20
		order.shipcost = shipcost

		context = {'order':order,'odlist':odlist,'count':count}


	return render(request, 'Myapp/myorderdetail.html',context)



def Updatetracking(request,orderid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	if request.method == 'POST' :
		order = Orderpending.objects.get(orderid = orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		order.save()
		return redirect('allorderlist-page')
	
	

	order = Orderpending.objects.get(orderid=orderid)
	odlist = Orderlist.objects.filter(orderid = orderid)

	Sum_total = sum([ c.total for c in odlist ])

	## shipcost calculated
	order.total = Sum_total	

	# คิดค่าจัดส่งวินค้าตามจำนวนชิ้น 
	count = sum([ i.quantity for i in odlist])
	# คำนวณค่าส่งตามประเภทการส่ง
	
	if order.shipping == 'ems':
		shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
		# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
	else:
		shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
		# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
	
	if order.payment == 'cod':
		shipcost +=20
	order.shipcost = shipcost

	context = {'orderid': orderid ,'order':order,'odlist':odlist,'count':count}
		
	return render(request, 'Myapp/updatetracking.html',context)


def updatepaid(request,orderid,status):
	
	order = Orderpending.objects.get(orderid = orderid)

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	if order.payment == "transfer":
		
		if status== 'confirm':	
			order.paid = True
		elif status== 'cancel':	
			order.paid = False
			
		else:
			pass
	elif order.payment == "cod":
		if status== 'confirm':	
			order.approved = True
		elif status== 'cancel':	
			order.approved = False
		else:
			pass
	else:
		pass
	order.save()
	return redirect('allorderlist-page')



# def UploadSlip(request,orderid):
	

# 	if request.method == 'POST' and request.FILES['slip']:
# 		data = request.POST.copy()
# 		sliptime = data.get('sliptime')
		

# 		update = Orderpending.objects.get(orderid=orderid)
# 		update.sliptime = sliptime
# 		image_file = request.FILES['slip']
# 		image_file_name = request.FILES['slip'].name.replace(' ','')
# 		print('FILE_IMAGE : ',image_file)
# 		print('FILE_IMAGE_NAME : ',image_file_name)
# 		fs = FileSystemStorage()
# 		filename = fs.save(image_file_name,image_file)
# 		upload_file_url = fs.url(filename)
# 		update.slip= upload_file_url[6:]
		
# 		update.save()	

# 	odlist = Orderlist.objects.filter(orderid = orderid)
# 	Sum_total = sum([ c.total for c in odlist ])
# 	oddetail = Orderpending.objects.get(orderid=orderid)

# 	count = sum([ i.quantity for i in odlist])
# 	# คำนวณค่าส่งตามประเภทการส่ง
# 	if oddetail.shipping == 'ems':
# 		shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
# 		# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
# 	else:
# 		shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
# 		# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
	
# 	if oddetail.payment == 'cod':
# 		shipcost +=20
	
# 	context =  {'orderid':orderid,
# 				'total':Sum_total,
# 				'shipcost':shipcost,
# 				'grandtotal':Sum_total+shipcost,
# 				'oddetail':oddetail,
# 				'count':count
# 				}

		

# 	return render(request,'Myapp/uploadslip.html',context)

def UploadSlip(request,orderid):
	# data = request.POST.copy()
	# file = data.get("slip")
	# print("FILES ########",file["name"])
	## เเก้ปัญหาอัพโหลดไฟล์จากเดิมเอาไว้หน้า UploadSlip

	if request.method == "POST":
		data = request.POST.copy()
		sliptime = data.get('sliptime')
		update = Orderpending.objects.get(orderid=orderid)
		update.sliptime = sliptime
		# image_file = request.FILES['slip']
		# image_file_name = request.FILES['slip'].name.replace(' ','')
		# print('FILE_IMAGE : ',image_file)
		# print('FILE_IMAGE_NAME : ',image_file_name)
		# fs = FileSystemStorage()
		# filename = fs.save(image_file_name,image_file)
		# upload_file_url = fs.url(filename)
		# update.slip= upload_file_url[6:]
		if "slip" in request.FILES:
			update.slip = request.FILES['slip']

			############### SEND LINE NOTIFY ####################
			link_foradmin = "https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/makeorder/{}/".format(orderid)
			texttoline = 'คุณ {} \nเลข order : {}\nได้อัพโหลดสลิป\n------------\nดูออเดอร์เลย:{}'.format(update.customername,orderid,link_foradmin)
			messenger.sendtext(texttoline)
		else:
			pass
		update.save()	



	odlist = Orderlist.objects.filter(orderid = orderid)
	Sum_total = sum([ c.total for c in odlist ])
	oddetail = Orderpending.objects.get(orderid=orderid)

	count = sum([ i.quantity for i in odlist])
	# คำนวณค่าส่งตามประเภทการส่ง
	if oddetail.shipping == 'ems':
		shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
		# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
	else:
		shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
		# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
	
	if oddetail.payment == 'cod':
		shipcost +=20
	
	context =  {'orderid':orderid,
				'total':Sum_total,
				'shipcost':shipcost,
				'grandtotal':Sum_total+shipcost,
				'oddetail':oddetail,
				'count':count
				}

		

	return render(request,'Myapp/uploadslip.html',context)


def Allorderlistpage(request):


	context = {}
	order = Orderpending.objects.all()

	for od in order:
		orderID = od.orderid

		odlist = Orderlist.objects.filter(orderid = orderID)
		Sum_total = sum([ c.total for c in odlist ])
		od.total = Sum_total

		# คิดค่าจัดส่งวินค้าตามจำนวนชิ้น 
		count = sum([ i.quantity for i in odlist])
		# คำนวณค่าส่งตามประเภทการส่ง
		
		if od.shipping == 'ems':
			shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
			# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
		else:
			shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
			# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
		
		if od.payment == 'cod':
			shipcost +=20
		od.shipcost = shipcost

	paginator = Paginator(order,17) # หนึ่งหน้าโชว์เเค่ 17 ชิ้นเท่านั้น
	page = request.GET.get('page') # http://127.0.0.1:8000/allproduct/?page=2
	order = paginator.get_page(page)

	context['allorder'] = order

	return render(request,'Myapp/allorderlist.html',context)


def orderlistpage(request):
	# initial tabs
	context = {}
	if request.user.is_authenticated:
		username = request.user.username
		user = User.objects.get(username = username)
		order = Orderpending.objects.filter(user=user).order_by("id").reverse() 
		if  order.exists(): 
			order = order[0] #latest 
		else:
			pass
		if order in Orderpending.objects.filter(Q(user=user),Q(payment="transfer"),Q(slip__isnull=True) | Q(slip__exact='')):
			context["tabs"] = 1
		elif order in Orderpending.objects.filter(Q(user=user),Q(payment="cod")| ~(Q(slip__isnull=True) | Q(slip__exact='')),Q(approved=False)):
			context["tabs"] = 2
		elif order in Orderpending.objects.filter(Q(user=user),Q(approved=True),Q(trackingnumber__isnull=True) | Q(trackingnumber__exact='')):
			context["tabs"] = 3
		elif order in Orderpending.objects.filter(Q(user=user),~(Q(trackingnumber__isnull=True) | Q(trackingnumber__exact=''))):
			context["tabs"] = 4
		elif order in Orderpending.objects.filter(Q(user=user),Q(customer_confirm=True)):
			context["tabs"] = 5
		else:
			context["tabs"] = 1
		print("tab = ",context["tabs"])
	else:
		mes_id = request.session.get('mes_id')
		print("mes from orderlist  ",mes_id)
		# # just in case anonymous's email is "" (blank)
		# if mes_id == "":
		# 	order = Orderpending.objects.filter(email = mes_id)
		# else:
		order = Orderpending.objects.filter(mid = mes_id).order_by("id").reverse() 
		if  order.exists(): 
			order = order[0] #latest 
		else:
			pass 
		if order in Orderpending.objects.filter(Q(mid = mes_id),Q(payment="transfer"),Q(slip__isnull=True) | Q(slip__exact='')):
			context["tabs"] = 1
		elif order in Orderpending.objects.filter(Q(mid = mes_id),Q(payment="cod")| ~(Q(slip__isnull=True) | Q(slip__exact='')),Q(approved=False)):
			context["tabs"] = 2
		elif order in Orderpending.objects.filter(Q(mid = mes_id),Q(approved=True),Q(trackingnumber__isnull=True) | Q(trackingnumber__exact='')):
			context["tabs"] = 3
		elif order in Orderpending.objects.filter(Q(mid = mes_id),~(Q(trackingnumber__isnull=True) | Q(trackingnumber__exact=''))):
			context["tabs"] = 4
		elif order in Orderpending.objects.filter(Q(mid = mes_id),Q(customer_confirm=True)):
			context["tabs"] = 5
		else:
			context["tabs"] = 1
		print("tab = ",context["tabs"])


	return render(request,'Myapp/orderlist.html',context)

def order_tab1(request):
	context = {}
	if request.user.is_authenticated:
		username = request.user.username
		user = User.objects.get(username = username)
		order = Orderpending.objects.filter(Q(user=user),Q(payment="transfer"),Q(slip__isnull=True) | Q(slip__exact='')).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]
		

	else:
		mes_id = request.session.get('mes_id')
		request.session['mes_id'] = mes_id
		order = Orderpending.objects.filter(Q(mid = mes_id),Q(payment="transfer"),Q(slip__isnull=True) | Q(slip__exact='')).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]

	context["allorder"] = order


	return render(request,'Myapp/tab_order/order_tab1.html',context)

def order_tab2(request):
	context = {}
	if request.user.is_authenticated:
		username = request.user.username
		user = User.objects.get(username = username)
		order = Orderpending.objects.filter(Q(user=user),
		Q(payment="cod")| ~(Q(slip__isnull=True) | Q(slip__exact='')),
		Q(approved=False)).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]
		

	else:
		mes_id = request.session.get('mes_id')
		print("orderlistpage",mes_id)
		order = Orderpending.objects.filter(Q(mid = mes_id),
		Q(payment="cod") | ~(Q(slip__isnull=True) | Q(slip__exact='')),
		Q(approved=False)).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]

	context["allorder"] = order


	return render(request,'Myapp/tab_order/order_tab2.html',context)

def order_tab3(request):
	context = {}
	if request.user.is_authenticated:
		username = request.user.username
		user = User.objects.get(username = username)
		order = Orderpending.objects.filter(Q(user=user),
		Q(approved=True),
		Q(trackingnumber__isnull=True) | Q(trackingnumber__exact='')).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]
		

	else:
		mes_id = request.session.get('mes_id')
		print("orderlistpage",mes_id)
		order = Orderpending.objects.filter(Q(mid = mes_id),
		Q(approved=True),
		Q(trackingnumber__isnull=True) | Q(trackingnumber__exact='')).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]

	context["allorder"] = order

	return render(request,'Myapp/tab_order/order_tab3.html',context)

def order_tab4(request):
	context = {}
	if request.user.is_authenticated:
		username = request.user.username
		user = User.objects.get(username = username)
		order = Orderpending.objects.filter(Q(user=user),
		~(Q(trackingnumber__isnull=True) | Q(trackingnumber__exact=''))).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]
		

	else:
		mes_id = request.session.get('mes_id')
		print("orderlistpage",mes_id)
		order = Orderpending.objects.filter(Q(mid = mes_id),
		~(Q(trackingnumber__isnull=True) | Q(trackingnumber__exact=''))).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]

	context["allorder"] = order

	return render(request,'Myapp/tab_order/order_tab4.html',context)

def order_tab5(request):
	context = {}
	if request.user.is_authenticated:
		username = request.user.username
		user = User.objects.get(username = username)
		order = Orderpending.objects.filter(Q(user=user),
		Q(customer_confirm=True)).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]
		

	else:
		mes_id = request.session.get('mes_id')
		print("orderlistpage",mes_id)
		order = Orderpending.objects.filter(Q(mid = mes_id),
		Q(customer_confirm=True)).order_by("id").reverse()
		shipcosts = calShipCost(order)
		for i,od in enumerate(order):
			od.shipcost = shipcosts[i]

	context["allorder"] = order


	return render(request,'Myapp/tab_order/order_tab5.html',context)




# redundant

# def orderlistpage(request):
# 	context = {}
	
# 	if request.user.is_authenticated:

# 		username = request.user.username
# 		user = User.objects.get(username = username)

		
		
# 		order = Orderpending.objects.filter(user=user)

# 		## ทำการคำนวณค่าส่งของเเต่ละเลข orderID เเล้วเอามาเเสดงผลบนหน้า orderlist-page
		
# 		for od in order:
# 			orderID = od.orderid

# 			# หาค่าสินค้าโดยรวม ที่ยังไม่รวมค่าขนส่งสินค้า
# 			odlist = Orderlist.objects.filter(orderid = orderID).order_by("id").reverse()
# 			Sum_total = sum([ c.total for c in odlist ])
# 			od.total = Sum_total	

# 			# คิดค่าจัดส่งวินค้าตามจำนวนชิ้น 
# 			count = sum([ i.quantity for i in odlist])
# 			# คำนวณค่าส่งตามประเภทการส่ง
			
# 			if od.shipping == 'ems':
# 				shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
# 				# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
# 			else:
# 				shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
# 				# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
			
# 			if od.payment == 'cod':
# 				shipcost +=20
# 			od.shipcost = shipcost

# 		context['allorder'] = order

# 	else:
	
# 		mes_id = request.COOKIES['mid']
# 		print("orderlistpage",mes_id)
# 		order = Orderpending.objects.filter(email = csrftoken)
		
# 		for od in order:
# 			orderID = od.orderid

# 			# หาค่าสินค้าโดยรวม ที่ยังไม่รวมค่าขนส่งสินค้า
# 			odlist = Orderlist.objects.filter(orderid = orderID).order_by("id").reverse()
# 			Sum_total = sum([ c.total for c in odlist ])
# 			od.total = Sum_total	

# 			# คิดค่าจัดส่งวินค้าตามจำนวนชิ้น 
# 			count = sum([ i.quantity for i in odlist])
# 			# คำนวณค่าส่งตามประเภทการส่ง
			
# 			if od.shipping == 'ems':
# 				shipcost = sum([ 50 if i == 0 else 10 for i in range(count) ])
# 				# ship cost ชิ้นเเรกคิด 50 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
# 			else:
# 				shipcost = sum([ 20 if i == 0 else 10 for i in range(count) ])
# 				# ship cost ชิ้นเเรกคิด 20 บาท ชิ้นต่อไปบวกเพิ่มชิ้นละสิบบาท
			
# 			if od.payment == 'cod':
# 				shipcost +=20
# 			od.shipcost = shipcost

# 		context['allorder'] = order
		


# 	return render(request,'Myapp/orderlist.html',context)






















