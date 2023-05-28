from django.db import models
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField


class Contact(models.Model):
    email369 = models.EmailField(max_length=50,null=True,verbose_name='Email')
    mobile_no = models.BigIntegerField(validators= [RegexValidator("^0?[5-9]{1}\d{9}$")],blank=True,null=True,help_text='Optional: (Phone No. Field!!)')
    name = models.CharField(max_length=15)
    feedback = models.TextField(max_length=600)    
    cr_date = models.DateTimeField(auto_now_add=True)
    f_type = models.CharField(default='Feedback',max_length=25,verbose_name='Form Type:',choices=(('Feedback',"Feedback"),("Help","Help"),("Contact us","Contact us")))
    captcha = models.TextField(verbose_name='Recaptcha',default=False,help_text="Hidden Recaptcha Applied..")
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Contact Us'
    
class Bugreport(models.Model):
    name = models.CharField(default='no',max_length=20)
    email = models.EmailField(max_length=40)
    bug_detail = models.TextField(verbose_name='Bug Detail') 
    cr_date = models.DateTimeField(auto_now_add=True)
    
class TermandCondition(models.Model):
    terms_and_condition = RichTextField(default='No Data Found!!',null = True,blank=True,help_text="Enter Site's Terms and Condition")
    privacy_and_policy = RichTextField(default='No Data Found!!',null = True,blank=True,help_text="Enter Site's Privacy Policy")
    disclaimer = RichTextField(default='No Data Found!!',null = True,blank=True,help_text='Enter Disclaimer')
    cr_date = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = 'Term & Condition,Privacy_Policy,Disclaimer'
