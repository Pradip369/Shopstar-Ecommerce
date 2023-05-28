from django import forms
# from django.db.models.loading import cache
from django.apps import apps
from django.contrib.auth import get_user_model

class EmailChangeForm(forms.Form):
    
    email = forms.EmailField(label='New E-mail', max_length=75,
                            widget=forms.EmailInput(
                            attrs={'class':'form-control mt-2','id':'c_mail','autofocus':'true','placeholder': 'Email Address'}
                            )
                            )
    
    def __init__(self, username=None, *args, **kwargs):
        """Constructor.
        
        **Mandatory arguments**
        
        ``username``
            The username of the user that requested the email change.
        
        """
        self.username = username
        super(EmailChangeForm, self).__init__(*args, **kwargs)
    
    def clean_email(self):
        """Checks whether the new email address differs from the user's current
        email address.
        
        """
        email = self.cleaned_data.get('email')
        
        # User = apps.get_model('auth', 'User')
        User = get_user_model()
        user = User.objects.get(username__exact=self.username)
        
        # Check if the new email address differs from the current email address.
        if user.email == email:
            raise forms.ValidationError('New email address cannot be the same \
                as your current email address')
        
        return email



