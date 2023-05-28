from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import settings
from decorator_include import decorator_include
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.mail.message import EmailMessage
from datetime import datetime
from django.views.generic.base import RedirectView
from django.conf.urls.static import static


def only_user():
    def check(user):
        if user.is_authenticated and user.is_superuser or user.is_staff:
            return True
        
        time = datetime.now()
        message = f'----------------------------------\nName: {user.username}\nEmail: {user.email}\nTime: {time}.\n----------------------------------\n • {user.username} is not a staff user or admin.For some security reasons..Please block this user from your admin panel(Blacklist).'
        
        email = EmailMessage(
                            f'📛📛📛Alert!! {user.username} is try to accessing your admin panel!!', 
                            message,
                            settings.EMAIL_HOST_USER,
                            [settings.EMAIL_HOST_USER], 
                            )
        email.fail_silently = False
        email.send()
        
        raise PermissionDenied
    return user_passes_test(check)

urlpatterns = [  
                 
    path('', include('product.urls')),
    
    path('user/', include('user_registration.urls')),
    
    path('change_email/', include('email_change.urls')),
    
    path('read_doc/', include('website_detail.urls')),
    
    #Fake admin urls
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('site/admin/',RedirectView.as_view(url='/admin')),
    path('user/admin/',RedirectView.as_view(url='/admin')),
    path('secure/admin/',RedirectView.as_view(url='/admin')),
    path('mysite/admin/',RedirectView.as_view(url='/admin')),
    path('admin/secure',RedirectView.as_view(url='/admin')),
    path('real/admin/',RedirectView.as_view(url='/admin')),
    
    #Real admin urls
    path('mom/shreeji/maharaj/369/', decorator_include([login_required, only_user()], admin.site.urls)),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root = settings.DEFAULT_FILE_STORAGE)
