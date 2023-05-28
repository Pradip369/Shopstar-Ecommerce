from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Order,OrderItem,MyOrder,LikeProduct
from django.utils.html import format_html
from django.urls.base import reverse

class OrderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","customer","orderd_date","complete","reference_Id","payment_status"]
    search_fields = ["id","customer__username","orderd_date","reference_Id","complete","order_complete_id","payment_status"]
    list_filter = ["id","customer","complete","orderd_date","payment_status"]
    readonly_fields = ('id',"reference_Id","order_complete_id","customer","complete")
    autocomplete_fields = ["customer"]
    list_display_links = list_display

admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","product","quantity","order","add_date"]
    search_fields = ["id","product__product_name","order__customer__username","add_date"]
    list_filter = ["product","order","add_date"]
    readonly_fields = ("quantity","product","order")
    autocomplete_fields = ["product","order"]
    list_display_links = list_display

    
admin.site.register(OrderItem,OrderItemAdmin)

class MyOrderAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","username","quantity","payment_status","reference_id","order_complete_id","order_status","orderd_date","Generate_Order_PDF"]
    search_fields = ["id","order_id","username","item","payment_status","order_complete","reference_id","category","order_complete_id","orderd_date","orderd_date"]
    list_filter = ["id","payment_status","reference_id","orderd_date"]
    readonly_fields = ('id',"username","item","price","quantity","total","category","reference_id","order_id","order_complete_id","customer_detail","order_complete","Generate_Order_PDF",)
    list_display_links = list_display
    
    def Generate_Order_PDF(self,obj):
        try:
            link = reverse('order_to_pdf',args = [obj.id])
            return format_html(f'<a style = "color : red;" href = {link} download = "{obj.username}__{obj.id}">Save as PDF</a>')
        except Exception:
            return None
admin.site.register(MyOrder,MyOrderAdmin)

class LikeProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","product","liked_by","cr_date"]
    search_fields = ["id","product__product_name","liked_by__username"]
    list_filter = ["product","liked_by"]
    autocomplete_fields = ["product","liked_by"]
    readonly_fields = ('liked_by','product')
    list_display_links = list_display
    
admin.site.register(LikeProduct,LikeProductAdmin)