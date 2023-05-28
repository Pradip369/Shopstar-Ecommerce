from django.contrib import admin
# from django.db.models.loading import cache
from django.apps import apps

class EmailChangeRequestAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ['email','date_created']
    search_fields = ['email','date_created']
    list_display_links = list_display

admin.site.register(apps.get_model('email_change', 'EmailChangeRequest'), EmailChangeRequestAdmin)