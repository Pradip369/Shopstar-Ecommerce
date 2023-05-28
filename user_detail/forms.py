from .models import ShippingAddress
from django import forms
from django_countries.widgets import CountrySelectWidget


class Shippingaddress(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['country',"house_no","full_address","nearest_landmark","city","state","zipcode","phone_no"]
        labels = {'phone_no':"Contact Number"}
        
        error_messages = {
            'country':{'required':"Select country"},
            'house_no':{'required':"Enter house number"},
            'full_address':{'required':"Enter full address"},
            'nearest_landmark':{'required':"Enter nearest landmark"},
            'city':{'required':"Enter city"},
            'state':{'required':"Enter state"},
            'city':{'required':"Enter city"},
            'zipcode':{'required':"Enter zipcode"},
            'phone_no':{'required':"Enter phone no"}
                  }
        widgets = { 
                   'country': CountrySelectWidget(),
                   'house_no':forms.TextInput(attrs={'placeholder':"House number",'class':'my-2'}),
                   'full_address':forms.Textarea(attrs={'rows':4, 'cols':40,'placeholder':"soc. or apt. no.,name,area,nr.",'class':'my-2'}),
                   'nearest_landmark':forms.TextInput(attrs={'placeholder':"Enter Nearest Landmark",'class':'my-2'}),
                   'city':forms.TextInput(attrs={'placeholder':"Enter City",'class':'my-2'}),
                   'state':forms.TextInput(attrs={'placeholder':"Enter State",'class':'my-2'}),
                   'zipcode':forms.TextInput(attrs={'placeholder':"Enter Zipcode",'class':'my-2'}),
                   'phone_no':forms.NumberInput(attrs={'placeholder':"Enter Contact No.",'class':'my-2'}),
                   }