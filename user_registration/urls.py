from django.urls import path
from . import views
from django.urls.conf import include
from django.contrib.auth import views as auth_view
from .forms import Loginform,Passwordresetform,PasswordchangeForm,SetpasswordForm,ResendActivationForm
from django.urls.base import reverse_lazy

from registration.backends.default import views as re

from django.conf import settings
from .views import RegistrationView
from django.conf.urls import url

urlpatterns = [
  
    path('accounts/login/',auth_view.LoginView.as_view(redirect_authenticated_user=True,template_name='registration/login.html',authentication_form=Loginform),name='login_user'),
    path('accounts/logout/',auth_view.LogoutView.as_view(template_name='registration/logout.html'),name='auth_logout'),

    path('accounts/password/change/',auth_view.PasswordChangeView.as_view(success_url=reverse_lazy('passdone'),template_name='registration/password_change.html',form_class=PasswordchangeForm),name='pass_change'),
    path('accounts/password/change/done/',auth_view.PasswordChangeDoneView.as_view(template_name='registration/password_done.html'),name='passdone'),
    path('accounts/password/reset/',auth_view.PasswordResetView.as_view(template_name='registration/password_reset.html',form_class=Passwordresetform,success_url = reverse_lazy('reset_send'),email_template_name = 'registration/password_resetemail.html'),name='reset_password'),
    path('accounts/password/reset/done/',auth_view.PasswordResetCompleteView.as_view(template_name='registration/password_reset_send.html'),name='reset_send'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='registration/password_resetform.html',form_class=SetpasswordForm,success_url = reverse_lazy('reset_done')),name='password_reset'),
    path('accounts/password_reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='registration/password_resetdone.html'),name='reset_done'),
  
    path('accounts/activate/resend/',re.ResendActivationView.as_view(template_name='registration/resend_activation_form.html',form_class=ResendActivationForm,),name='resend_pass'),  
]
if getattr(settings, 'INCLUDE_REGISTER_URL', True):
    urlpatterns += [
        url(r'^accounts/register/$',
            RegistrationView.as_view(success_url = reverse_lazy('registration_complete')),
            name='registration_register'),
    ] 

urlpatterns += [
    path('accounts/',include('registration.backends.default.urls')),
]    