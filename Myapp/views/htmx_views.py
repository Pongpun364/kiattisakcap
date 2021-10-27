from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .. models import *
from django.contrib.auth.models import User
import json
from .htmx_views import *
from .order_views import *
from .product_views import *
from .system import *
from .user_views import *
from .utils import *



def Checkout_htmx(request):

	context = {}
	data = cartData(request)
	context['mycart'] = data['mycart']
	context['Sum_total'] = data['Sum_total']
	context['Sum_quantity'] = data['Sum_quantity']

	return render(request,'Myapp/checkout_htmx.html',context)

def ProcessOrder(request):

	data = json.loads(request.body)
	saveOrdertodB(request,data)

	return JsonResponse('Payments submitted...',safe=False)

def cartquan_htmx(request):
	context={}
	if request.user.is_authenticated:
		pass
	else:
		data = cookieCart(request)
		Sum_quantity  = data['Sum_quantity']
		print("print from cartquan_htmx",type(Sum_quantity))

	context['Sum_quantity']= Sum_quantity

	return render(request,"Myapp/htmx/cartquan.html",context)

def check_modal(request):
	return render(request,"Myapp/htmx/checkout_modal.html")

def check_animate(request):
	return render(request,"Myapp/htmx/checkout_mes.html")

def dummyendpoint(request):
	return HttpResponse("")