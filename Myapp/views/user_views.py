
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .. models import *

from django.contrib.auth.models import User

from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json
from django.views import generic
import requests
from . htmx_views import *
from . order_views import *
from . product_views import *
from . system import *
from . user_views import *
from . utils import *
import random
from . mytils import *










def UpdateCart(request):
	#  Ex.   localhost:8000/addproduct/3
	# {% url "addtocart-page" pd.id  %}
	username = request.user.username
	user = User.objects.get(username = username)

	data = request.POST.copy()

	pid = data.get('pid')
	print("pid",type(pid))

	# data = request.POST.copy()
	# pid = data.get('productid')
	check = Allproduct.objects.get(id=pid)	

	try:
		# มีในตะกร้าอยู่เเล้ว
		newcart = Cart.objects.get(user = user,productid = pid)
		print("SUCCESS")

		# กดมาจากหน้า mycart
		quantity= data.get('quantity')
		if(quantity !=None):
			if(quantity == "0"):
				newcart.delete()
			else:
				newcart.quantity = quantity
				print("quantity",quantity)
				calculate = int(newcart.price) * int(quantity)
				print("calculate",calculate)
				newcart.total = calculate
				newcart.save()
			# อัปเดตจำนวนของตะกร้าสินค้า ณ ตอนนี้
			count = Cart.objects.filter(user = user)
			countall = sum([ c.quantity for c in count ])
			updatequan = Profile.objects.get(user = user)
			updatequan.cartquan = countall
			updatequan.save()

			return redirect("mycart-page")
		# กดมาจากหน้า allproduct
		else:
			newcart.quantity += 1
			calculate = int(newcart.price) * newcart.quantity
			newcart.total = calculate
			newcart.save()

			# อัปเดตจำนวนของตะกร้าสินค้า ณ ตอนนี้
			count = Cart.objects.filter(user = user)
			countall = sum([ c.quantity for c in count ])
			updatequan = Profile.objects.get(user = user)
			updatequan.cartquan = countall
			updatequan.save()

			return render(request,"Myapp/htmx/cartquan.html")	
	
	except:
			print("ERROR")
		# ยังไม่มีอยู่ในตะกร้า เเน่นอนว่ากดมาจากหน้า allproduct
			newcart = Cart()
			newcart.user = user
			newcart.productid = pid
			newcart.productname = check.name
			newcart.price = int(check.price)
			newcart.quantity = 1
			calculate = int(check.price) * 1
			newcart.total = calculate
			newcart.save()

			# อัปเดตจำนวนของตะกร้าสินค้า ณ ตอนนี้
			count = Cart.objects.filter(user = user)
			countall = sum([ c.quantity for c in count ])
			updatequan = Profile.objects.get(user = user)
			updatequan.cartquan = countall
			updatequan.save()

			
			return render(request,"Myapp/htmx/cartquan.html")	



def index(request):


	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	print(request.session)
	context = {
		'num_visits': num_visits,
	}

	# Render the HTML template index.html with the data in the context variable.
	return render(request, 'Myapp/visit_count.html', context)



def Mycart(request):


	context = {}
	data = cartData(request)
	context['mycart'] = data['mycart']
	# anonymous ใช้เป็น id เเต่ user เป็น productid 
	context['Sum_total'] = data['Sum_total']
	context['Sum_quantity'] = data['Sum_quantity']
	######## check user device ########
	keywords = ['Mobile','Opera Mini','Android']
	user_agent = request.META['HTTP_USER_AGENT']
	if any(word in user_agent for word in keywords):
		print('Visitor is on mobile device')
		return render(request,'Myapp/mobile/mycart_mobile.html',context)
	else:
		print('Visitor is on desktop')
		return render(request,'Myapp/mycart.html',context)

 ### เหมียนกันเลย เชี่ย !!!

def Checkout(request):

	context = {}
	# ### check ว่ามาจาก messenger รึเปล่า
	mes_id = request.session.get('mes_id')
	user_match = "False"
	if mes_id == None:
		request.session['mes_id'] = rand_for_me(12)
	else:
		mes = messenger_user.objects.filter(mid=mes_id)
		if mes.exists():
			user_match = "True"
		else:
			pass
	print("user_match",user_match)
	# print("mes_id",request.session['mes_id'])

	data = cartData(request)
	context['mycart'] = data['mycart']
	context['Sum_total'] = data['Sum_total']
	context['Sum_quantity'] = data['Sum_quantity']
	context['user_match'] = user_match

	return render(request,'Myapp/checkout.html',context)




def AddtoCart(request,pid):
	#  Ex.   localhost:8000/addproduct/3
	# {% url "addtocart-page" pd.id  %}
	print("Request User: ", request.user)

	username = request.user.username
	user = User.objects.get(username = username)
	check = Allproduct.objects.get(id=pid)	
	dataa = request.POST.copy()
	quantity = dataa.get("quantity")
	print("quantity type ",type(quantity))

	try:
		# กรณีที่ตัวสินค้ามีซ้ำ
		newcart = Cart.objects.get(user = user,productid = str(pid)) # ถ้าใช้ filter จะไม่ได้ เพราะจะไม่หลุดลูปตัว try
		newquan = newcart.quantity + int(quantity)
		newcart.quantity = newquan
		calculate = int(newcart.price) * newquan
		newcart.total = calculate
		newcart.save()

		# อัปเดตจำนวนของตะกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user = user)
		countall = sum([ c.quantity for c in count ])
		updatequan = Profile.objects.get(user = user)
		updatequan.cartquan = countall
		updatequan.save()
		return render(request,"Myapp/htmx/cartquan.html")
		
	
	except:
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity =  newcart.quantity + int(quantity)
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()

		# อัปเดตจำนวนของตะกร้าสินค้า ณ ตอนนี้
		count = Cart.objects.filter(user = user)
		countall = sum([ c.quantity for c in count ])
		updatequan = Profile.objects.get(user = user)
		updatequan.cartquan = countall
		updatequan.save()

		return render(request,"Myapp/htmx/cartquan.html")

def deleteMycart(request,pid):
	
	username = request.user.username
	user = User.objects.get(username = username)

	Items = Cart.objects.filter(user = user,productid = pid)
	Items.delete()
	
	# อัปเดตโปรไฟล์ ตามข้อมูลใน cart model
	count = Cart.objects.filter(user = user)
	countall = sum([ c.quantity for c in count ])
	updatequan = Profile.objects.get(user = user)
	updatequan.cartquan = countall
	updatequan.save()

	# อัปเดตหลังจากที่มีการ delete
	context = {}

	mycart = Cart.objects.filter(user = user)
	## เก็บค่า Image ไว้
	for ig in mycart: # ที่ทำเเบบนี้ได้ เพราะ Cart มันถูกเรียกที่นี่
		allpro = Allproduct.objects.get(id = int(ig.productid))
		ig.Image = allpro.Image.url
	Sum_quantity = sum([ c.quantity for c in mycart ])
	Sum_total = sum([ c.total for c in mycart ])

	context['mycart'] = mycart
	context['Sum_quantity'] = Sum_quantity
	context['Sum_total'] = Sum_total

	######## check user device ########
	keywords = ['Mobile','Opera Mini','Android']
	user_agent = request.META['HTTP_USER_AGENT']
	if any(word in user_agent for word in keywords):
		print('Visitor is on mobile device')
		return render(request,'Myapp/mobile/mycart_mobile.html',context)
	else:
		print('Visitor is on desktop')
		return render(request,'Myapp/mycart.html',context)



#เรียกจาก ajax ทั้ง anonymous เเละ user ปกติ
def ProcessOrder(request):

	data = json.loads(request.body)
	oid = saveOrdertodB(request,data)
	print("oid from ProcessOrder",oid)

	oid = h_encode(oid)
	return JsonResponse(oid,safe=False)



# Create your views here.
class YoMamaBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == '5465165652':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	# Post function to handle Facebook messages
	def post(self, request, *args, **kwargs):
		# Converts the text payload into a python dictionary
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		print("incoming_message",incoming_message)
		# Facebook recommends going through every entry since they might send
		# multiple messages in a single call during high load
		# flag = False
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				# Check to make sure the received call is a message call
				# This might be delivery, optin, postback for other events
				if 'message' in message:
					fb_user_id = message['sender']['id'] # sweet!
					fb_user_txt = message['message'].get('text')
					if fb_user_id == "104950065273237":
						if fb_user_txt == "เว็บ":
							fb_user_id = message['recipient']['id']
							print("fb_user_id",fb_user_id)
							post_facebook_link(fb_user_id)
						else: 
							pass
					else:
						if fb_user_txt:
							define_umid(fb_user_id)

		return HttpResponse("Success", status=200)




############################### step 1 #############################
def define_umid(fb_user_id):
	data = messenger_user.objects.filter(mid = fb_user_id)
	if data.exists():
		pass
	else:
		
		data = messenger_user()
		data.mid = fb_user_id
		data.save()
		post_facebook_link(fb_user_id)

	return None


############################### step 2 #############################
# ส่ง link ไปหา user คนนั้นๆ 
def post_facebook_link(fb_user_id):
	data = messenger_user.objects.get(mid=fb_user_id)
	append = data.get_hashid()
	# print("appeend",append)
	# print("appeend",type(append))
	cur_host = "https://7fdf-2001-44c8-45cb-76e3-f1cf-4031-f44-a9da.ngrok.io/" + 'kiattisakcapshop/'+append + "/"
	print('current host',cur_host)
	page_token = "EAANDfsxI83YBAEqbYn5dslmYIhmHz3MKNNwINLa9RwY0B7D8Uke6VtctW4No6tNUm0mFjDFQ7X4n31uZAif046wqXxJ3i2btO6cShpm1kPyz7Q412b4VtWlQd6L3A7X5yVgyfU4FI77bdVuqfXjFZBH60vlXgXexyjN6xChedcNUww7zZCS"  
	msg = {
	"recipient": {
	"id": fb_user_id
	},
	"message": {
		"attachment": {
		"type": "template",
		"payload": {
			"template_type": "generic",
			"elements": [
			{
				"title": "ยินดีต้อนรับ",
				"image_url": "https://kiattisakcap.com/media/products/Captur55e.PNG",
				"subtitle": "เราเชื่อว่าทุกคน จะมีหมวกที่ใช้ของตัวเองเสมอ !!!",
				"default_action": {
				"type": "web_url",
				"url": cur_host,
				"messenger_extensions": "false",
				"webview_height_ratio": "tall"
				},
				"buttons": [
				{
					"type": "web_url",
					"url": cur_host,
					"title": "เลือกชมสินค้าเลย !"
				}
				]
			}
			]
		}
		}
	}
}

	response_msg = json.dumps(msg)
	post_message_url = 'https://graph.facebook.com/v12.0/me/messages?access_token=' + page_token
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print("after post link ",status.json())
	return status.json()
	# return HttpResponse("Success", status=200)


############################### step 3 #############################
# สร้าง endpoint รอ user ที่มี mid นั้นๆกดมาหา
#encrypted_id คือ messenger_user id
def messenger_cus(request,encrypted_id):
	print("encrypted_mid",encrypted_id)
	stamp = messenger_user.objects.get(id=encrypted_id)

	# mes_id = request.session.get('mes_id')
	# if mes_id == None:
	# 	request.session['mes_id'] = stamp.mid
	# else:
	# 	pass
	request.session['mes_id'] = stamp.mid
	print(request.session['mes_id'])

################################# hard code ##################################################
	product = Allproduct.objects.all().order_by("id").reverse() # ดึงข้อมูลออกมาทั้งหมด
	paginator = Paginator(product,6) # หนึ่งหน้าโชว์เเค่ 3 ชิ้นเท่านั้น
	page = request.GET.get('page') # http://127.0.0.1:8000/allproduct/?page=2
	product = paginator.get_page(page)
	# currentpath = (request.path).replace('/','_')
	context = {'product':product}

##############################################################################################
 
	return render(request, 'Myapp/allproduct.html', context)



def response_to_chatplugin(user_ref):
	page_token = "EAANDfsxI83YBAEqbYn5dslmYIhmHz3MKNNwINLa9RwY0B7D8Uke6VtctW4No6tNUm0mFjDFQ7X4n31uZAif046wqXxJ3i2btO6cShpm1kPyz7Q412b4VtWlQd6L3A7X5yVgyfU4FI77bdVuqfXjFZBH60vlXgXexyjN6xChedcNUww7zZCS"  

	response_msg = json.dumps({"recipient":{"user_ref":user_ref}, "message":{"text":"hello world"}})
	post_message_url = 'https://graph.facebook.com/v12.0/me/messages?access_token=' + page_token
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print(status.json())
	return None

#   "recipient": {
#     "user_ref":"<UNIQUE_REF_PARAM>"
#   }, 
#   "message": {
#     "text":"hello, world!"
#   }
# }' "https://graph.facebook.com/v2.6/me/messages?access_token=<PAGE_ACCESS_TOKEN>" 


# this can be devided in to two scenario 1.) messenger user finishes order and 2.) Anonymous lost their session 
def return_session(request,oid,mid):
	# 1.) messenger user finishes order
	mid = str(mid)
	request.session['mes_id'] = mid
	# เซตค่า mid ตามข้อมูล orderid ใน orderpending
	order = Orderpending.objects.get(orderid=oid)
	order.mid = mid
	order.save()
	# Manually set the value you'll use for rendering


	# ไปยังหน้า myorderdetail
	odlist = Orderlist.objects.filter(orderid = oid)
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
	# response = HttpResponse()
	# response.set_cookie(key='csrftoken', value=val)
	# template = loader.get_template('Myapp/myorderdetail.html')
	# response.write(template.render(context,request))

	# response.set_cookie(key='kanom', value=val,max_age= 365 * 24 * 60 * 60,samesite='Lax')
	return render(request, 'Myapp/myorderdetail.html', context)



def post_facebook_message(fbid, recevied_message):  
	page_token = "EAANDfsxI83YBAEqbYn5dslmYIhmHz3MKNNwINLa9RwY0B7D8Uke6VtctW4No6tNUm0mFjDFQ7X4n31uZAif046wqXxJ3i2btO6cShpm1kPyz7Q412b4VtWlQd6L3A7X5yVgyfU4FI77bdVuqfXjFZBH60vlXgXexyjN6xChedcNUww7zZCS"  

	user_details_url = "https://graph.facebook.com/v12.0/%s"%(fbid)
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'%s'%(page_token)}
	user_details = requests.get(user_details_url, user_details_params).json()
	recevied_message += user_details['first_name']
	
	post_message_url = 'https://graph.facebook.com/v12.0/me/messages?access_token=' + page_token
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print(status.json())
	return None

def fetch_post_facebook(request):
	############### SEND RECEIPT TO MESSENGER ####################
	mes_id = request.session.get('mes_id')
	print("fetch_post_facebook",mes_id)
	response = {}
	try:
		int(mes_id)
		# messenger user
		print("unload json data",request.body)
		data = json.loads(request.body)
		oid = h_decode(data["data"])
		print("data = ",data)
		response = post_facebook_receipt(mes_id,oid)
	except:
		print("I have done nothing !!!")
	return JsonResponse(response)

############################### step 4 (messenger user) #############################
def post_facebook_receipt(mid,oid):
 #############################  hard code #################################
	print("mid that i has sent",mid)
	order = Orderpending.objects.get(orderid=oid)
	odlist = Orderlist.objects.filter(orderid = oid)
	for img in odlist:
		product = Allproduct.objects.get(id=int(img.productid))
		img.Image = product.Image.url

	## shipcost calculated
	Sum_total = sum([ c.total for c in odlist ])
	
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

	################## done hard code ##################################

	oid = h_encode(oid)
	# print("appeend",append)
	# print("appeend",type(append))
	cur_host = "https://7fdf-2001-44c8-45cb-76e3-f1cf-4031-f44-a9da.ngrok.io/" + 'receipt/'+oid + "/" + h_encode(int(mid)) + "/"
	print('current host',cur_host)
	page_token = "EAANDfsxI83YBAEqbYn5dslmYIhmHz3MKNNwINLa9RwY0B7D8Uke6VtctW4No6tNUm0mFjDFQ7X4n31uZAif046wqXxJ3i2btO6cShpm1kPyz7Q412b4VtWlQd6L3A7X5yVgyfU4FI77bdVuqfXjFZBH60vlXgXexyjN6xChedcNUww7zZCS" 
	payment_method = "ชำระปลายทาง" if order.payment == "cod" else "อัปโหลดรูปสลิป"
	total = Sum_total + shipcost
	msg={
			"recipient":{
			"id":mid
			},
			"message":{
				"attachment":{
				"type":"template",
				"payload":{
					"template_type":"button",
					"text":"ลูกค้าสามารถดูคำสั่งซื้อได้ตรงนี้เลย",
					"buttons":[
					{
						"type":"web_url",
						"url":cur_host,
						"title":"ดูคำสั่งซื้อ"
					}
					]
				}
				}
			}
	}

	# msg = {
	# 	"recipient":{
	# 		"id":mid
	# 	},
	# 	"message":{
	# 		"attachment":{
	# 		"type":"template",
	# 		"payload":{
	# 			"template_type":"receipt",
	# 			"recipient_name":order.customername,
	# 			"order_number":oid,
	# 			"currency":"USD",
	# 			"payment_method":payment_method,        
	# 			"order_url":cur_host,
	# 			"timestamp":"1428444852",         
	# 			"address":{
	# 			"street_1":order.address,
	# 			"street_2":"",
	# 			"city":"Chiang Mai",
	# 			"postal_code":order.zipcode,
	# 			"state":"Chiang Mai",
	# 			"country":"TH"
	# 			},
	# 			"summary":{
	# 			"subtotal":Sum_total,
	# 			"shipping_cost":shipcost,
	# 			"total_cost":total
	# 			},

	# 			"elements":[]
	# 		}
	# 		}
	# 	}
	# 	}

# 	msg = {
# 	"recipient":{
# 		"id": mid
# 	},
# 	"message":{
# 		"attachment":{
# 			"type":"template",
# 			"payload":{
# 				"template_type":"receipt",
# 				"recipient_name":order.customername,
# 				"order_number":oid,
# 				"payment_method":payment_method,        
# 				"order_url":cur_host,
# 				"timestamp":"1428444852",         
# 				"address":{
# 					"street_1":order.address,
# 					"city":"_",
# 					"postal_code":order.zipcode,
# 					"state":"CA",
# 					"country":"US"
# 				},
# 				"summary":{
# 					"subtotal":Sum_total,
# 					"shipping_cost":shipcost,
# 					"total_cost":Sum_total + shipcost
# 				},
# 				"elements":[]
# 			}
# 		}
# 	}
# }

	# elements =[]
	# for ol in odlist:
	# 	dat = {}
	# 	dat['title'] = ol.productname
	# 	dat['quantity'] = ol.quantity
	# 	dat['price'] = ol.price
	# 	dat['image_url'] = "https://7fdf-2001-44c8-45cb-76e3-f1cf-4031-f44-a9da.ngrok.io"+ ol.Image
	# 	elements.append(dat)
	# msg['message']['attachment']['payload']['elements'] = elements
	print(msg)
	print(type(msg))
	print("before dumps")
	try:
		response_msg = json.dumps(msg, indent=4, sort_keys=True, default=str) # หลังจากดัมบ์ ก็จะกลายเป็น json ทันที ###
		print("response_msg",response_msg)
	except Exception as e:
		print("why not telling me fuckkkk ",e)
	print("after dumps")
	post_message_url = 'https://graph.facebook.com/v12.0/me/messages?access_token=' + page_token
	print("initial status = ")
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print("end status = ")
	print(status.json())
	print("end status 2 = ")
	return status.json()
