from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from user_detail.models import Profile
from django.contrib.auth.models import User
from .models import Product,HomePageCarouselOffer,HomePageOffer
from django.http.response import Http404

@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kw):
    if created:
        Profile.objects.create(user_name=instance)

@receiver(pre_save, sender=Product)
def delete_product_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = Product.objects.get(pk=instance.pk)
            if pr_inst.image.url != instance.image.url:
                pr_inst.image.delete(save=False)
            if pr_inst.image1 != instance.image1:
                pr_inst.image1.delete(save=False)
            if pr_inst.image2 != instance.image2:
                pr_inst.image2.delete(save=False)
            if pr_inst.image3 != instance.image3:
                pr_inst.image3.delete(save=False)
        except Product.DoesNotExist:
            return Http404

@receiver(pre_delete, sender=Product)
def delete_old_product(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = Product.objects.get(pk=instance.pk)
            pr_inst.image.delete(save=False)
            pr_inst.image1.delete(save=False)
            pr_inst.image2.delete(save=False)
            pr_inst.image3.delete(save=False)
        except Product.DoesNotExist:
            return Http404
        
@receiver(pre_save, sender=HomePageCarouselOffer)
def delete_carousel_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = HomePageCarouselOffer.objects.get(pk=instance.pk)
            if pr_inst.other_offer_image != instance.other_offer_image:
                pr_inst.other_offer_image.delete(save=False)
        except HomePageCarouselOffer.DoesNotExist:
            return Http404

@receiver(pre_delete, sender=HomePageCarouselOffer)
def delete_old_carousel(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = HomePageCarouselOffer.objects.get(pk=instance.pk)
            pr_inst.other_offer_image.delete(save=False)
        except HomePageCarouselOffer.DoesNotExist:
            return Http404
        
@receiver(pre_save, sender=HomePageOffer)
def delete_HomePage_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = HomePageOffer.objects.get(pk=instance.pk)
            if pr_inst.home_offer_image != instance.home_offer_image:
                pr_inst.home_offer_image.delete(save=False)
        except Product.DoesNotExist:
            return Http404

@receiver(pre_delete, sender=HomePageOffer)
def delete_old_HomePage(sender, instance, **kwargs):
    if instance.pk:
        try:
            pr_inst = HomePageOffer.objects.get(pk=instance.pk)
            pr_inst.home_offer_image.delete(save=False)
        except Product.DoesNotExist:
            return Http404