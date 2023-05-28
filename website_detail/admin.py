from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Contact,Bugreport,TermandCondition


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","name","f_type","cr_date"]
    search_fields = ["f_type","name","mobile_no","email"]
    list_filter = ["name","f_type","cr_date"]
    list_display_links = list_display
    
class BugreportrAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","name","email","cr_date"]
    search_fields = ["name","email"]
    list_filter = ["name","cr_date"]
    list_display_links = list_display
    
admin.site.register(Bugreport,BugreportrAdmin)

class TermandConditionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","cr_date"]
    search_fields = ["terms_and_condition","privacy_and_policy","disclaimer","cr_date"]
    list_filter = ["cr_date"]
    list_display_links = list_display
    
admin.site.register(TermandCondition,TermandConditionAdmin)