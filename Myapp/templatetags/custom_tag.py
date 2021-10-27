#custom_tag.py
# เอาไปใช้กับข้อมูลที่ต้องมีอิสระในการใช้งานทุกหน้า
from django import template
from ..models import *
from django.contrib.auth.models import User
import json
from django.shortcuts import render,redirect
from ..views.htmx_views import *
from ..views.order_views import *
from ..views.product_views import *
from ..views.system import *
from ..views.user_views import *
from ..views.utils import *

register = template.Library()

@register.simple_tag
def hello_tag():
	return "############################## Hello Tag ###############################"

@register.simple_tag
def showAllproduct():
	count = Allproduct.objects.count()
	return count

@register.inclusion_tag('Myapp/allcategory.html')  #เอาไว้ไปทำ html เเยกกับหน้า html ที่มีอยู่เดิม เพื่อที่จะเพิ่มความอิสระ
def all_cat():                                     # ในการเรียกใช้ข้อมูลจากโมเดลๆ เดียว ในหน้า html ทั้งหมด 
	cats = Category.objects.all()
	return {"allcats":cats}


@register.inclusion_tag('Myapp/htmx/cartquan.html', takes_context=True)
def showCartquan(context):
	request = context['request']
	Sum_quantity = 0
	if request.user.is_authenticated:
		# username = request.user.username
		# user = User.objects.get(username = username)
		# pf = Profile.objects.get(user=user)
		# cartquan = pf.cartquan

	
		return context
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
			
			for i in cart:
				Sum_quantity += cart[i]['quantity']
			# print('cart',cart)
		except:
			cart = {}
		
		context.update({"Sum_quantity":Sum_quantity})
		
		return context

	# request = context['request']
	# # print('request.COOKIES email',request.COOKIES['email'])
	# cartquan = 0
	# try:
	#     cart = json.loads(request.COOKIES['cart'])
		
	#     for i in cart:
	#         cartquan += cart[i]['quantity']
	#     # print('cart',cart)
	# except:
	#     cart = {}
	
	# return cartquan

#     @register.simple_tag(takes_context=True)
# def showCartquan(context):
	
#     return redirect("cartquan_htmx")
	# request = context['request']
	# # print('request.COOKIES email',request.COOKIES['email'])
	# cartquan = 0
	# try:
	#     cart = json.loads(request.COOKIES['cart'])
		
	#     for i in cart:
	#         cartquan += cart[i]['quantity']
	#     # print('cart',cart)
	# except:
	#     cart = {}
	
	# return cartquan