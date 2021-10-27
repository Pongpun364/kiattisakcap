from django.urls import path,register_converter
from django.conf.urls import url

from .views.htmx_views import *
from .views.order_views import *
from .views.product_views import *
from .views.system import *
from .views.user_views import * 
from .views.utils import *
from .views.user_views import YoMamaBotView
from .views.linebot import *
from .views.mytils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
	path('', Home, name = 'home-page'),
	path('about/', About,name = 'about-page'),
	path('contact/', Contact, name='contact-page'),
	path('addproduct/', Addproduct, name='addproduct-page'),
	path('allproduct/', Product, name='allproduct-page'),
	path('register/', Register, name='register-page'),
	path('addtocart/<int:pid>/', AddtoCart, name='addtocart-page'),
	path('updatecart/', UpdateCart, name='updatecart'),
	path('mycart/', Mycart, name='mycart-page'),
	path('checkout/', Checkout, name='checkout-page'),
	path('allorderlist/', Allorderlistpage, name='allorderlist-page'),
	path('uploadslip/<hashid:orderid>/', UploadSlip, name='uploadslip-page'),
	path('updatestatus/<str:orderid>/<str:status>', updatepaid, name='updatestatus'),
	path('updatetracking/<str:orderid>/', Updatetracking, name='updatetracking-page'),
	path('myorderdetail/<hashid:orderid>/', Myorder_detail, name='myorderdetail-page'),
	path('editproduct/<int:productid>/', EditProduct, name='editproduct-page'),
	path('cartquan_htmx/', cartquan_htmx, name='cartquan_htmx'),
	path('product/<int:productid>/', ProductDetail, name='product-page'),
	path('delete_cart/<str:pid>', deleteMycart, name='delete_mycart'),
	path('checkout/', Checkout, name='checkout-page'),
	path('orderlist/', orderlistpage, name='orderlist-page'),
	path('processorder/', ProcessOrder, name='processorder'),
	path('checkemail', checkEmail, name='checkemail'),
	path('checkmodal', check_modal, name='checkmodal'),
	path('orderlist/', orderlistpage, name='orderlist-page'),
	path('order_tab1', order_tab1, name='order_tab1'),
	path('order_tab2', order_tab2, name='order_tab2'),
	path('order_tab3', order_tab3, name='order_tab3'),
	path('order_tab4', order_tab4, name='order_tab4'),
	path('order_tab5', order_tab5, name='order_tab5'),
	url(r'^4115cc2d1bf048f6d7796efd811d3efc45cec4cd9148f9bb57/?$', YoMamaBotView.as_view()),
	path('receipt/<hashid:oid>/<hashid:mid>/', return_session, name='return_session'),
	path('kiattisakcapshop/<hashid:encrypted_id>/', messenger_cus, name='kiattisakcapshop'),
	path('numvisit/', index, name='numvisit'),
	path('check_mes/', check_animate, name='check_mes'),
	path('post_facebook/', fetch_post_facebook, name='post_facebook'),
	path('dummy', dummyendpoint, name='dummy'),
	###### mobile admin #####
	path("callback",callback),
	path('allorderlist_mobile/', AllorderlistpageMobile, name='allorderlist_mobile'),
	path('Updatetrackingmobile/<hashid:orderid>/', Updatetrackingmobile, name='Updatetrackingmobile'),
	path('slipview/<hashid:orderid>/', slipview, name='slipview'),
	path('updatepaidmobile/<hashid:orderid>/<str:status>', updatepaidmobile, name='updatepaidmobile'),
	path('commentmodal/<hashid:orderid>/', comment, name='commentmodal'),
	path('intent/<str:intent>/<int:kanit>/', intenturl, name='intent'),
	# path("lifftest/",lifftest),
	# path("sayhi/<str:name>",lifftestsayhi)
	path('category/<int:code>/', ProductCat, name='category-page')


	]