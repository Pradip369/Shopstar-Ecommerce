from django.urls.conf import path
from .views import PrivacyPolicy,Termandcondition,Disclaimer

urlpatterns = [
    path('privacy_policy/',PrivacyPolicy,name = 'privacy_policy'),
    path('term_and_condition/',Termandcondition,name = 'term_and_condition'),
    path('disclaimer/',Disclaimer,name = 'disclaimer'),
]