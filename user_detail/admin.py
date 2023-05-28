from django.contrib import admin
from .models import Profile,ShippingAddress
from import_export.admin import ImportExportModelAdmin

class ProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","user_name","full_name","age","gender"]
    search_fields = ["id","user_name__username","full_name","age","gender"]
    list_filter = ["user_name","age"]
    readonly_fields = ('full_name',)
    list_display_links = list_display

admin.site.register(Profile,ProfileAdmin)


class ShippingAddressAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","customer","order","city","add_date","zipcode"]
    search_fields = ["id","customer__username","city","add_date","zipcode"]
    list_filter = ["customer","order","add_date","city"]
    autocomplete_fields = ["customer","order"]
    list_display_links = list_display
    
admin.site.register(ShippingAddress,ShippingAddressAdmin)