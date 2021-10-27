from django.contrib import admin
from .models import *

admin.site.site_header = 'หน้าจัดการ แอดมิน'
admin.site.index_title = 'Admin System'
admin.site.site_title = 'Cap Admin System'


class AllproductAdmin(admin.ModelAdmin):
    list_display = ['name','price','instock','id','quantity']
    list_editable = ['price','instock']

admin.site.register(Allproduct, AllproductAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(VerifyingEmail)

class OrderlistAdmin(admin.ModelAdmin):
    list_display = ['orderid','productid','total','productname']
    list_editable = ['productid','total','productname']
admin.site.register(Orderlist, OrderlistAdmin)

class OrderpendingAdmin(admin.ModelAdmin):
    list_display = ['orderid','payment','paid','tel']
    list_editable = ['payment','paid','tel']
admin.site.register(Orderpending, OrderpendingAdmin)









