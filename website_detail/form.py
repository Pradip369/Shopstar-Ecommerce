from django.core import validators
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django import forms

class Bug_report(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    bug_detail = forms.CharField(widget=forms.Textarea,validators=[validators.MinLengthValidator(100,'Write Minimum 100 words...')])
    Recaptcha = ReCaptchaField(widget=ReCaptchaV2Invisible)