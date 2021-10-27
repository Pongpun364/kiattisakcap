from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .htmx_views import *
from .order_views import *
from .. models import *
from .product_views import *
from .system import *
from .user_views import *
from .utils import *
from django.db.models import Q
from . mytils import *
# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from linebot import LineBotApi,WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ButtonsTemplate, TemplateSendMessage
from linebot.models.actions import URIAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
	# if request.method == 'POST':
	#     signature = request.META['HTTP_X_LINE_SIGNATURE']
	#     body = request.body.decode('utf-8')
	#     print("message is coming from line")
	#     try:
	#         events = parser.parse(body, signature)
	#     except InvalidSignatureError:
	#         return HttpResponseForbidden()
	#     except LineBotApiError:
	#         return HttpResponseBadRequest()

	#     for event in events:
	#         if isinstance(event, MessageEvent):
	#             mtext=event.message.text
	#             message=[]
	#             message.append(TextSendMessage(text=mtext))
	#             line_bot_api.reply_message(event.reply_token,message)

	#     return HttpResponse()
	# else:
	#     return HttpResponseBadRequest()
	body = request.body.decode('utf-8')
	# print(body)
	req = json.loads(request.body)
	# print(req)
	# req = request.get_json(silent=True, force=True)
	intent = req["queryResult"]["intent"]["displayName"] # ชื่อ intent ใน dialog flow
	text = req['originalDetectIntentRequest']['payload']['data']['message']['text'] # ข้อความที่ผู้ใช้ส่งมา
	reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken'] # token เอาไว้ตอบกลับ
	id = req['originalDetectIntentRequest']['payload']['data']['source']['userId'] # id ของผู้ใช้งาน
	disname = line_bot_api.get_profile(id).display_name # ชื่อใน line ของผู้ใช้งาน
	
	print('id = ' + id)
	print('name = ' + disname)
	print('text = ' + text)
	print('intent = ' + intent)
	print('reply_token = ' + reply_token)

	if reply(intent,text,reply_token,id,req):
		return HttpResponse()
	else:
		return HttpResponseBadRequest()


def reply(intent,text,reply_token,id,req):
	if intent == 'intent5':
		text_message = TextSendMessage(text='ทดสอบสำเร็จ')
		line_bot_api.reply_message(reply_token,text_message)
		return True
	elif intent == "latest":
		buttons_template_message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='https://kiattisakcap.com/media/products/Captur55e.PNG',
				title='Menu',
				text='รายการออร์เดอร์ล่าสุด',
				actions=[
					URIAction(
						label='ดูรายการ',
						uri='https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/latest/1/'
					)
				]
			)
		)
		order = Orderpending.objects.all()
		if order.exists():
			line_bot_api.reply_message(reply_token,buttons_template_message)
		else:
			text_message = TextSendMessage(text='ไม่มีออเดอร์ในระบบเลย')
			line_bot_api.reply_message(reply_token,text_message)
		return True
	elif intent == "ordernumber":
		number = req["queryResult"]["outputContexts"][1]["parameters"]["amount"]
		number = int(number)
		buttons_template_message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='https://kiattisakcap.com/media/products/Captur55e.PNG',
				title='Menu',
				text='รายการออร์เดอร์ล่าสุด',
				actions=[
					URIAction(
						label='ดูรายการ',
						uri='https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/ordernumber/{}/'.format(number)
					)
				]
			)
		)
		order = Orderpending.objects.all()
		if order.exists():
			line_bot_api.reply_message(reply_token,buttons_template_message)
		else:
			text_message = TextSendMessage(text='ไม่มีออเดอร์ในระบบเลย')
			line_bot_api.reply_message(reply_token,text_message)
		return True
	elif intent == "codnumber":
		codnum = req["queryResult"]["outputContexts"][1]["parameters"]["codnum"]
		codnum = int(codnum)
		buttons_template_message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='https://kiattisakcap.com/media/products/Captur55e.PNG',
				title='Menu',
				text='รายการออร์เดอร์ล่าสุด (เก็บปลายทาง)',
				actions=[
					URIAction(
						label='ดูรายการ',
						uri='https://e879-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/codnumber/{}/'.format(codnum)
					)
				]
			)
		)
		order = Orderpending.objects.filter(payment="cod")
		if order.exists():
			line_bot_api.reply_message(reply_token,buttons_template_message)
		else:
			text_message = TextSendMessage(text='ไม่มีออเดอร์เเบบจ่ายปลายทางเลยครับ')
			line_bot_api.reply_message(reply_token,text_message)
		return True
	elif intent == "transfernum":
		transfernum = req["queryResult"]["outputContexts"][1]["parameters"]["transfernum"]
		transfernum = int(transfernum)
		buttons_template_message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='https://kiattisakcap.com/media/products/Captur55e.PNG',
				title='Menu',
				text='รายการออร์เดอร์ (โอนสลิป)',
				actions=[
					URIAction(
						label='ดูรายการ',
						uri='https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/transfernum/{}/'.format(transfernum)
					)
				]
			)
		)
		order = Orderpending.objects.filter(payment="transfer")
		if order.exists():
			line_bot_api.reply_message(reply_token,buttons_template_message)
		else:
			text_message = TextSendMessage(text='ไม่มีออเดอร์เเบบโอนเลยครับ')
			line_bot_api.reply_message(reply_token,text_message)
		return True
	elif intent == "unslip":
		buttons_template_message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='https://kiattisakcap.com/media/products/Captur55e.PNG',
				title='Menu',
				text='รายการออร์เดอร์ (ยังไม่ได้จ่ายสลิป)',
				actions=[
					URIAction(
						label='ดูรายการ',
						uri='https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/unslip/1/'
					)
				]
			)
		)
		order = Orderpending.objects.filter(Q(slip__isnull=True) | Q(slip__exact=''),payment="transfer")
		if order.exists():
			line_bot_api.reply_message(reply_token,buttons_template_message)
		else:
			text_message = TextSendMessage(text='ลูกค้าทุกคนอัพโหลดสลิปหมดเเล้วครับ')
			line_bot_api.reply_message(reply_token,text_message)
		return True
	elif intent == "unapproved":
		buttons_template_message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='https://kiattisakcap.com/media/products/Captur55e.PNG',
				title='Menu',
				text='รายการออร์เดอร์ (ยังไม่ได้อนุมัติ)',
				actions=[
					URIAction(
						label='ดูรายการ',
						uri='https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/unapproved/1/'
					)
				]
			)
		)
		order = Orderpending.objects.filter(approved = False)
		if order.exists():
			line_bot_api.reply_message(reply_token,buttons_template_message)
		else:
			text_message = TextSendMessage(text='คุณกดยืนยันลูกค้าทุกคนหมดเเล้ว')
			line_bot_api.reply_message(reply_token,text_message)
		return True
	elif intent == "untracking":
		buttons_template_message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='https://kiattisakcap.com/media/products/Captur55e.PNG',
				title='Menu',
				text='รายการออร์เดอร์ (ยังไม่ได้กรอกเลขติดตามพัสดุ)',
				actions=[
					URIAction(
						label='ดูรายการ',
						uri='https://5557-2001-44c8-45d7-a7b4-c0fd-7516-b19a-42a5.ngrok.io/intent/untracking/1/'
					)
				]
			)
		)
		order = Orderpending.objects.filter(Q(trackingnumber__isnull=True) | Q(trackingnumber__exact=''))
		if order.exists():
			line_bot_api.reply_message(reply_token,buttons_template_message)
		else:
			text_message = TextSendMessage(text='คุณกรอกเลขติดตามลูกค้าทุกคนหมดเเล้ว')
			line_bot_api.reply_message(reply_token,text_message)
		return True
	else:
		return False



# def lifftest(request):
# 	return render(request,'Myapp/liff/lifftest.html')

# def lifftestsayhi(request,name):
# 	context = {}
# 	context['name'] = name
# 	return render(request,'Myapp/liff/lifftest_sayhi.html',context)

# ทำหน้าที่มาร์กคุ้กกี้ session ให้กับ admin
def intenturl(request,intent,kanit):
	if intent == "latest":
		request.session['intent'] = "latest"
	elif intent == "ordernumber":
		request.session['intent'] = "ordernumber"
		request.session['parameter'] = kanit
	elif intent == "codnumber":
		request.session['intent'] = "codnumber"
		request.session['parameter'] = kanit
	elif intent == "transfernum":
		request.session['intent'] = "transfernum"
		request.session['parameter'] = kanit
	elif intent == "unslip":
		request.session['intent'] = "unslip"
	elif intent == "unapproved":
		request.session['intent'] = "unapproved"
	elif intent == "untracking":
		request.session['intent'] = "untracking"
	elif intent == "makeorder":
		request.session['intent'] = "makeorder"
		request.session['parameter'] = kanit
	else:
		pass
	return redirect("allorderlist_mobile")

@login_required
def AllorderlistpageMobile(request):

	context = {}

	if request.user.profile.usertype != "admin":
		return HttpResponseForbidden()

	order = filterordermodel(request)
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


	context['allorder'] = order

	return render(request,'Myapp/mobile/allorderlist_mobile.html',context)

def Updatetrackingmobile(request,orderid):
	if request.user.profile.usertype != 'admin':
		return HttpResponseForbidden()

	if request.method == 'POST' :
		order = Orderpending.objects.get(orderid = orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		order.save()
	
	order = Orderpending.objects.get(orderid=orderid)

	context = {'order':order}
		
	return render(request, 'Myapp/mobile/tracking_modal.html',context)

def slipview(request,orderid):
	order = Orderpending.objects.get(orderid=orderid)
	image = order.slip.url
	context = {'image':image}
	return render(request, 'Myapp/mobile/slip_modal.html',context)

def updatepaidmobile(request,orderid,status):
	
	order = Orderpending.objects.get(orderid = orderid)

	if request.user.profile.usertype != 'admin':
		return HttpResponseForbidden()

	if status== 'confirm':	
		order.approved = True
	elif status== 'cancel':	
		order.approved = False
	else:
		pass

	order.save()

	return redirect('allorderlist_mobile')

def comment(request,orderid):
	if request.user.profile.usertype != 'admin':
		return HttpResponseForbidden()

	if request.method == 'POST' :
		order = Orderpending.objects.get(orderid = orderid)
		data = request.POST.copy()
		comment = data.get('comment')
		order.comment = comment
		order.save()

	order = Orderpending.objects.get(orderid=orderid)

	context = {'order':order}
	return render(request, 'Myapp/mobile/comment_modal.html',context)