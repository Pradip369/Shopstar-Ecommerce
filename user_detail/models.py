from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from PIL import Image
from django.core.files.storage import default_storage as storage
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save, pre_delete
from django.http.response import Http404
from django_countries.fields import CountryField

class Profile(models.Model):
    user_name = models.OneToOneField(to= User,on_delete=CASCADE,related_name='profile')
    profile_pic = models.ImageField(upload_to = 'profile_pic',null=True,blank=True)
    full_name = models.CharField(max_length=25,null=True,blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    gender = models.CharField(max_length=10,default="Male",choices=(('Male',"Male"),("Female","Female")))
    phone_no = models.CharField(max_length=15,null = True,blank = True)
    cr_date = models.DateTimeField(auto_now_add=True)
      
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        # if self.profile_pic:
        #     imag = Image.open(self.profile_pic)
        #     output_size = (300, 300)
        #     imag.thumbnail(output_size,Image.ANTIALIAS)
        #     fh = storage.open(self.profile_pic.name, "w")
        #     format = 'png'
        #     imag.save(fh,format)
        #     fh.close()

@receiver(pre_save, sender=Profile)
def delete_HomePage_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = Profile.objects.get(pk=instance.pk)
            if pr_inst.profile_pic != instance.profile_pic:
                pr_inst.profile_pic.delete(save=False)
        except Profile.DoesNotExist:
            return Http404

@receiver(pre_delete, sender=Profile)
def delete_old_HomePage(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = Profile.objects.get(pk=instance.pk)
            pr_inst.profile_pic.delete(save=False)
        except Profile.DoesNotExist:
            return Http404
            
                
class ShippingAddress(models.Model):
    customer = models.ForeignKey(to = User,on_delete=SET_NULL,null=True)
    order = models.ForeignKey(to = 'order_detail.Order',on_delete=SET_NULL,null=True)
    country = CountryField(blank_label='select country',null=True)
    house_no = models.CharField(max_length=100)
    full_address = models.TextField()
    nearest_landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=25)
    phone_no = models.PositiveIntegerField()
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s(%s)" %(self.customer,self.city)