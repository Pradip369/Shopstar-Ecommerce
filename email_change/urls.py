from django.conf.urls import url
from django.views.generic import TemplateView
from email_change.views import email_change_view,email_verify_view
from django.urls.conf import path


urlpatterns = [
    path('email/change/',email_change_view, name='email_change'),
    path('email/verification/sent/',
        TemplateView.as_view(template_name='email_change/email_verification_sent.html'),
        name='email_verification_sent'),
    path('email/verify/(^?P<verification_key>\w+$)/',email_verify_view, name='email_verify'),
    path('email/change/complete/',
        TemplateView.as_view(template_name='email_change/email_change_complete.html'),
        name='email_change_complete'),
]
