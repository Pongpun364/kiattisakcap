import json
from .. models import *
from datetime import datetime
from songline import Sendline
from django.db.models import Q
from .mytils import h_encode
import random

import requests
################### ส่งไลน์ #######################
token = 'fR6pJTnikFiQCxHhXw2Qo3l0mtUzKsp5PqA6vN2V1nf'
messenger = Sendline(token)

def rand_for_me(yao):
	allchar = [chr(i) for i in range(65,91) ]
	allchar.extend([chr(i) for i in range(97,123) ])
	allchar.extend([str(i) for i in range(10) ])
	data = ""
	for _ in range(yao):
		data += random.choice(allchar)
	return data


def cookieCart(request):
	#  ทำยังไงก็ได้ให้ส่งข้อมูล Cart เข้าไป render หน้าเพจให้ได้ .... Sum_quantity,Sum_total ด้วย !!!
	Sum_quantity = 0
	Sum_total = 0
	c=0
	try:
		cart = json.loads(request.COOKIES['cart'])
		print('cart',cart)
	except:
		cart = {}

	mycart_foranonymous = []

	for i in cart:

		try:
			Sum_quantity += cart[i]['quantity']
			product = Allproduct.objects.get(id=int(i)) #### ใช้ filter เเล้ว error เชี่ยไรวะเเมร่งงงงง !!! #############
			# print(type(i))
			# print("TEST: ",product.id)		
			Item = {'id':i,
					'productname': product.name,
					'price': product.price,
					'quantity': cart[i]['quantity'],
					'total': (int(product.price) * cart[i]['quantity']),
					'Image': product.Image.url ,
					}
			mycart_foranonymous.append(Item)		
			Sum_total += Item['total']

		except:
			pass



	return {'mycart_foranonymous':mycart_foranonymous,'Sum_total':Sum_total,'Sum_quantity':Sum_quantity}

def cartData(request):

	if request.user.is_authenticated:
		username = request.user.username
		user = User.objects.get(username = username)

		mycart = Cart.objects.filter(user = user).order_by('stamp').reverse()
		Sum_quantity = sum([ c.quantity for c in mycart ])
		Sum_total = sum([ c.total for c in mycart ])

		for ig in mycart: # ที่ทำเเบบนี้ได้ เพราะ Cart มันถูกเรียกที่นี่
			allpro = Allproduct.objects.get(id = int(ig.productid))
			ig.Image = allpro.Image.url

		
	else:
		data = cookieCart(request)
		mycart_foranonymous = data['mycart_foranonymous']
		Sum_quantity  = data['Sum_quantity']
		Sum_total = data['Sum_total']

		mycart = mycart_foranonymous




	return {'mycart':mycart,'Sum_quantity':Sum_quantity,'Sum_total':Sum_total}


def saveOrdertodB(request,data):
	
	if request.user.is_authenticated:

		username = request.user.username
		user = User.objects.get(username = username)

		
		
		name = data['form']['name']
		tel = data['form']['tel']
		address = data['form']['address']
		zipcode = data['form']['zipcode']
		shipping = data['form']['shipping']
		payment = data['form']['payment']
		other = data['form']['other']


		# 	############# พอกดชำระเงิน เเล้วค่อยดำเนินการเกี่ยวกับ database ###################
		# 	print('Confirm : ')
		mycart = Cart.objects.filter(user = user) # [[],[],[],[]]

		#generate Order ID and save to Order model
		dt =datetime.now().strftime('%f')
		orderID = str(random.choice(range(1,10))) + dt

		# productorder = ''
		# producttotal = 0
		total = 0
		for pd in mycart:
			order = Orderlist()
			order.orderid = int(orderID)
			order.productid = pd.productid
			order.productname  = pd.productname
			order.price  = pd.price
			order.quantity  = pd.quantity
			order.total  = pd.total
			total += pd.total
			order.save()
		
		# assign value to orderpending model
		odp = Orderpending()
		odp.orderid = int(orderID)
		odp.user = user
		odp.customername = name
		odp.tel = tel
		odp.address = address
		odp.shipping = shipping
		odp.payment = payment
		odp.other = other
		odp.save()

		############### SEND LINE NOTIFY ####################
		order = Orderpending.objects.filter(orderid=int(orderID))
		shipcost = calShipCost(order)[0]
		total+=shipcost
		# do not for loop with get method query object
		link_foradmin = "https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/makeorder/{}/".format(orderID)
		texttoline = 'คุณ {} \nเลข order : {}\n----------\nค่าขนส่ง {} บาทฃ\n รวมทั้งหมด: {:,.2f} บาท \nดูออเดอร์เลย:{}'.format(name,orderID,shipcost,total,link_foradmin)
		messenger.sendtext(texttoline)


		# clear cart and profile
		Cart.objects.filter(user=user).delete()
		updatequan = Profile.objects.get(user = user)
		updatequan.cartquan = 0
		updatequan.save()

		oid = int(orderID)
		print("oid from saveordertodb user",oid)
		return oid
	else:
		print('User is not logged in ...')
		print('COOKIES',request.COOKIES)
		
		name = data['form']['name']
		email = data['form']['email']
		tel = data['form']['tel']
		address = data['form']['address']
		zipcode = data['form']['zipcode']
		shipping = data['form']['shipping']
		payment = data['form']['payment']
		other = data['form']['other']


		cookieData = cookieCart(request)
		mycart_foranonymous = cookieData['mycart_foranonymous']
		Sum_quantity  = cookieData['Sum_quantity']
		Sum_total = cookieData['Sum_total']

		#generate Order ID and save to Orderlist model
		# mid = '5'.zfill(4)
		dt =datetime.now().strftime('%f')
		orderID = str(random.choice(range(1,10))) + dt
		total = 0
		for pd in mycart_foranonymous:
			order = Orderlist()
			order.orderid = int(orderID)
			order.productid = pd['id']
			order.productname  = pd['productname']
			order.price  = pd['price']
			order.quantity  = pd['quantity']
			order.total  = pd['total']
			total += pd['total']
			order.save()
		# assign value to orderpending model
		odp = Orderpending()
		odp.orderid = int(orderID)
		odp.customername = name
		odp.email = email
		odp.tel = tel
		odp.address = address
		odp.zipcode = zipcode
		odp.shipping = shipping
		odp.payment = payment
		odp.other = other
		
		# เช็คดูว่าเคยสั่งเเล้วหรือยัง (messenger) อาจจะเช็คจาก messenger ID
		# check = Orderpending.objects.filter(Q(email = email),Q(kanom__isnull=False) , ~Q(kanom__exact = '')).order_by("id")
		# print(check)
		# if check.exists():
		# 	odp.kanom = check[0].kanom
		

		mes_id = request.session.get('mes_id')
		if mes_id == None:
			request.session['mes_id'] = rand_for_me(12)
		else:
			pass
			
		odp.mid = request.session['mes_id']
		odp.save()


		############### SEND LINE NOTIFY ####################
		order = Orderpending.objects.filter(orderid=orderID)
		# do not for loop with get method query object
		shipcost = calShipCost(order)[0]
		total+=shipcost
		link_foradmin = "https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/makeorder/{}/".format(orderID)
		texttoline = 'คุณ {} \nเลข order : {}\n----------\nค่าขนส่ง {} บาทฃ\n รวมทั้งหมด: {:,.2f} บาท \nดูออเดอร์เลย:{}'.format(name,orderID,shipcost,total,link_foradmin)
		messenger.sendtext(texttoline)

		oid = int(orderID)
		print("oid from saveordertodb",oid)
		return oid


def calShipCost(order):
	
	## ทำการคำนวณค่าส่งของเเต่ละเลข orderID เเล้วเอามาเเสดงผลบนหน้า orderlist-page
	shipcosts = []
	for od in order:
		orderID = od.orderid

		# หาค่าสินค้าโดยรวม ที่ยังไม่รวมค่าขนส่งสินค้า
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
		shipcosts.append(shipcost)
		# od.shipcost = shipcost  #ถ้าทำเเบบนี้ ตอนเอาไปใช้ในฟังก์ชันหลักจะไม่สามารถเรียกใช้ตัวนี้ได้ เพราะ order object มันไม่ได้ถูกเรียกที่นี่
	return shipcosts

def filterordermodel(request):
	if request.session["intent"] == "latest":
		orderi = []
		order = Orderpending.objects.all().order_by("id").reverse()[0]
		orderi.append(order)
		return orderi
	elif request.session['intent'] == "ordernumber":
		num = request.session['parameter']
		order = Orderpending.objects.all().order_by("id").reverse()[:num]
		return order
	elif request.session['intent'] == "codnumber":
		codnum = request.session['parameter']
		order = Orderpending.objects.filter(payment="cod").order_by("id").reverse()[:codnum]
		return order
	elif request.session['intent'] == "transfernum":
		transfernum = request.session['parameter']
		order = Orderpending.objects.filter(payment="transfer").order_by("id").reverse()[:transfernum]
		return order
	elif request.session['intent'] == "unslip":
		order = Orderpending.objects.filter(Q(slip__isnull=True) | Q(slip__exact=''),payment="transfer").order_by("id").reverse()
		return order
	elif request.session['intent'] == "unapproved":
		order = Orderpending.objects.filter(approved = False).order_by("id").reverse()
		return order
	elif request.session['intent'] == "untracking":
		order = Orderpending.objects.filter(Q(trackingnumber__isnull=True) | Q(trackingnumber__exact='')).order_by("id").reverse()
		return order
	elif request.session['intent'] == "makeorder":
		orderid = request.session['parameter']
		order = Orderpending.objects.get(orderid=orderid)
		orderi = []
		orderi.append(order)
		return orderi
	else:
		return None
	
	


	






