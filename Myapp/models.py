from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.contrib.auth.models import User
from django.db.models.enums import IntegerChoices
from django.db.models.fields import BooleanField, CharField, IntegerField
from django.db.models.lookups import FieldGetDbPrepValueIterableMixin
from django.urls import reverse
from .views.mytils import h_encode



class VerifyingEmail(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	token = models.CharField(max_length=100)
	approved = models.BooleanField(default= False)


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	photo = models.ImageField(upload_to = 'photoprofile',null =True,blank=True , default = 'default_profile.jpg') # ถ้าจะเรียกใช้ต้องเป็น url
	usertype = models.CharField(max_length=100,default= 'member')
	cartquan = models.IntegerField(default=0)

	def __str__(self):
		return self.user.first_name

class Category(models.Model):
	catname = models.CharField(max_length=200,default="สินค้าทั่วไป")
	detail = models.TextField(null=True,blank=True)
	def __str__(self):
		return self.catname	

class Allproduct(models.Model):
	catname = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True) # ถ้าเป็น  FeriegnKey จะเอามาเป็น ID เสมอ
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=100) #ข้อความสั้นๆ
	detail = models.TextField(null = True,blank=True) #สำหรับกรอกข้อความเยอะๆ
	Imageurl = models.CharField(max_length= 200,null =True,blank=True)
	instock = models.BooleanField(default=True)
	Image = models.ImageField(upload_to='products/',default="SD-default-image.png") # ถ้าจะเรียกใช้ต้องเป็น url
	Image2 = models.ImageField(upload_to='products/',default="SD-default-image.png") # ถ้าจะเรียกใช้ต้องเป็น url
	Image3 = models.ImageField(upload_to='products/',default="SD-default-image.png") # ถ้าจะเรียกใช้ต้องเป็น url
	Image4 = models.ImageField(upload_to='products/',default="SD-default-image.png") # ถ้าจะเรียกใช้ต้องเป็น url
	Image5 = models.ImageField(upload_to='products/',default="SD-default-image.png") # ถ้าจะเรียกใช้ต้องเป็น url
	quantity = models.IntegerField(default=1,null =True,blank=True)
	unit = models.CharField(max_length=200,default = '-')
	def __str__(self):
		return self.name

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	productid = models.CharField(max_length=200)
	productname = models.CharField(max_length=200)
	price = models.CharField(max_length=100)
	quantity = models.IntegerField(default=0)
	total = models.IntegerField()
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	def __str__(self):
		return self.productname

class Orderlist(models.Model):
	orderid = models.CharField(max_length=100)
	productid = models.CharField(max_length=200)
	productname = models.CharField(max_length=200)
	price = models.CharField(max_length=100)
	quantity = models.IntegerField()
	total = models.IntegerField()


class Orderpending(models.Model):
	orderid = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
	address = models.TextField()
	customername = models.CharField(max_length=100)
	tel = models.CharField(max_length=100)
	shipping = models.CharField(max_length=100,null =True,blank=True)
	payment = models.CharField(max_length=100) # bank, prompt pay
	other = models.TextField(null =True,blank=True)
	stamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	paid = models.BooleanField(default = False) # เเบบโอนผ่านธนาคาร
	approved = models.BooleanField(default = False) # เเบบจ่ายปลายทาง
	slip = models.ImageField(upload_to = 'slip',null =True,blank=True )
	sliptime = models.CharField(max_length=100, null =True,blank=True) # มาเพิ่มเป็นประเภท date time พร้อมกับปฏิทินใน html
	paymentid = models.CharField(max_length=100,null=True,blank=True)
	trackingnumber = models.CharField(max_length=100,null=True,blank=True)
	zipcode = models.CharField(max_length=100,null=True,blank=True)
	email = models.EmailField(max_length = 100,null=True,blank=True)
	customer_confirm = models.BooleanField(default=False)
	mid = models.CharField( max_length=25,blank=True,default="")
	comment = models.TextField(max_length=400,blank=True,default="")

	
	def __str__(self):
		return self.customername



class messenger_user(models.Model):
	mid = models.CharField( max_length=25,blank=True,default="")

	def __str__(self):
		return self.mid
		
	def get_hashid(self):
		return h_encode(self.id)

	def get_absolute_url(self):
		return reverse("kiattisakcapshop", args=[self.id])


