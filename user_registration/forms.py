from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UsernameField, AuthenticationForm,\
    PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import password_validation

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django.core.exceptions import ValidationError

class Loginform(AuthenticationForm):
    username = UsernameField(label= _("Username or Email"),
                             widget=forms.TextInput(attrs={'placeholder':'Username or Email','autofocus':True,'class':'text-success  mt-2 form-control'}),
                             error_messages={"required":"Please Enter Valid Username or Email"})
    password = forms.CharField(
        label= _("Password"),
        strip = False,
        widget=forms.PasswordInput(attrs={'placeholder':'Password','autocomplete':'curent-password','class':'login_pass mt-2  text-danger form-control'}),
        error_messages={"required":"Please Enter Password"}
    )
    # captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    
    
class Passwordresetform(PasswordResetForm):
    email = forms.EmailField(
    label=_("Email ID"),
    max_length=100,
    widget=forms.EmailInput(attrs={'placeholder':'Email Address','autofocus':True,'autocomplete': 'email','class':'form-control mt-2 font-weight-bold text-success'}),
    error_messages={"required":"Please Enter Email"}
    )

class PasswordchangeForm(PasswordChangeForm,SetPasswordForm):
    error_messages = {
    'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'placeholder':'Password','autocomplete': 'new-password','class':'form-control text-success text-weight-bold my-2',}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','autocomplete': 'new-password','class':'form-control text-success text-weight-bold my-2',}),
    )
    
    
    error_messages = {
    **SetPasswordForm.error_messages,
    'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Old Password','autocomplete': 'current-password','class':'form-control my-2 text-danger text-weight-bold','autofocus':True}),
    )
    
    field_order = ['old_password', 'new_password1', 'new_password2']
    

class SetpasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'placeholder':'Password','autocomplete': 'new-password','class':'form-control text-success text-weight-bold my-2'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','autocomplete': 'new-password','class':'form-control text-success text-weight-bold my-2'}),
    )

# =================================== Registration form =============================


from django.contrib.auth.forms import UserCreationForm

from .users import UserModel
from .users import UsernameField
User = UserModel()

class RegistrationForm(UserCreationForm):

    required_css_class = 'required'
    email = forms.EmailField(label=_("E-mail"),
                            widget=forms.EmailInput(attrs={'placeholder':'Email Address','class':'text-bold form-control text-success text-weight-bold my-2'}),
                             )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'my-2 form-control text-weight-bold text-danger','placeholder':'Password','autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'my-2 form-control text-weight-bold text-success','placeholder':'Confirm Password','autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    # captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    class Meta:
        model = User
        widgets = {"username":forms.TextInput(attrs={'placeholder':'Enter Your Name','class':'form-control text-success text-weight-bold my-2'})
                  }        
        fields = ("username","email",)
        help_texts = {
            "username":None,
            "email":None,
        }

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 4:
            raise ValidationError("Username must greater than 4 characters!!")
        if " " in data:
            data = data.replace(" ","_")
        return data
        
class RegistrationFormUsernameLowercase(RegistrationForm):
 
    def clean_username(self):
        username = self.cleaned_data.get('username', '').lower()
        if User.objects.filter(**{UsernameField(): username}).exists():
            raise forms.ValidationError(_('A user with that username already exists.'))
        return username


class RegistrationFormTermsOfService(RegistrationForm):

    tos = forms.BooleanField(widget=forms.CheckboxInput(),
                             label=_('I have read and agree to the Terms of Service'),
                             error_messages={'required': _("You must agree to the terms and conditions for this site!!")})

class RegistrationFormNoFreeEmail(RegistrationForm):

    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com', 'outlook.com']

    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.

        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_("Registration using free email addresses is prohibited. Please supply a different email address."))
        return self.cleaned_data['email']

class ResendActivationForm(forms.Form):
    required_css_class = 'required'
    email = forms.EmailField(
                widget=forms.EmailInput(attrs={'placeholder':'Enter Email ID','class':'text-bold form-control text-success text-weight-bold my-2'}),
                label=_("E-mail"),
)

class RegistrationFormUniqueEmail(ResendActivationForm,RegistrationFormNoFreeEmail,RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.

    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("A user with that Email Address already exists!!"))
        return self.cleaned_data['email']
