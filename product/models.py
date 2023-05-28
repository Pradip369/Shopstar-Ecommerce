from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL    
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.safestring import mark_safe

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug_category = models.SlugField(default='',editable=False,max_length=250)   
     
    def __str__(self):
        return "%s" %(self.category_name)
    
    def save(self, *args, **kwargs):
        value = self.category_name[0:250]
        self.slug_category = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Add Category"
    

class Product(models.Model):
    product_name = models.CharField(verbose_name="Item Name",max_length=250)
    price = models.FloatField(help_text='Enter attractive price(eg : 999,499,1499)')
    old_price = models.FloatField(null=True,blank=True,help_text="This price is gratter than main price!!")
    
    image = models.ImageField(upload_to = 'product_image_main',verbose_name="Item's Main Image", help_text = "Atlist One item's image is required")
    image1 = models.ImageField(upload_to = 'product_image1',null=True,blank=True,help_text='Optional field')
    image2 = models.ImageField(upload_to = 'product_image2',null=True,blank=True,help_text='Optional field')
    image3 = models.ImageField(upload_to = 'product_image3',null=True,blank=True,help_text='Optional field')
    
    Product_description = RichTextField(verbose_name="Item's Features And Full Description",help_text="Describe item's features and full description above!!")
    category = models.ForeignKey(help_text='Select Category Related your product', to=Category,on_delete=SET_NULL,null=True)
    total_quantity = models.PositiveIntegerField(help_text = 'Enter Total available quantity of this product',verbose_name = 'stock')
    notification_email = models.EmailField(null=True,help_text='You will be notified immediately at this email when your customer buy this product')
    slug_product = models.SlugField(editable=False, default='',null=True,blank=True,max_length=250)
    cr_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "%s....($%s)" %(self.product_name[0 : 20],self.price)
    
    class Meta:
        verbose_name_plural = "Add Product"
    
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80px" height="80px" />' % (self.image.url))
    image_tag.short_description = 'Product Image.'    
    
    @property
    def total_saving(self):
        if self.old_price:
            t_save = (self.old_price - self.price)
        else:
            t_save = 0
        return t_save
    
    def save(self, *args, **kwargs):
        
        value = (self.product_name)[0:250]
        self.slug_product = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
        if self.old_price:
            if self.old_price <= self.price:
                self.old_price = 0
                super(Product, self).save(*args, **kwargs)
            else:
                super(Product, self).save(*args, **kwargs)
            

class CarouselOffer(models.Model):
    carousel_product = models.ForeignKey(to=Product,null=True,verbose_name='Select Product',on_delete=CASCADE,help_text='This product appear in home page first Carousel with image...')
    
    def __str__(self):
        return "%s" %(self.carousel_product)
    
    class Meta:
        verbose_name_plural = "Home Page CarouselOffer First"
    
class HomePageCarouselOffer(models.Model):
    other_offer = models.ForeignKey(verbose_name='Select Category',to=Category,on_delete=CASCADE,help_text='This category appear in home page second Carousel with image...')
    other_offer_image = models.ImageField(upload_to = "carousel_product",help_text = 'Upload attractive image(eg : Up to 50% Offer)')
    
    def __str__(self):
        return "%s" %(self.other_offer)
    
    class Meta:
        verbose_name_plural = "Home Page CarouselOffer Second"
    
class HomePageOffer(models.Model):
    product_offer = models.ForeignKey(verbose_name='Select Category',to=Category,on_delete=CASCADE,help_text='This category appear in home page with image...')
    home_offer_image = models.ImageField(verbose_name="Offer's Image",upload_to='home_offer_image',help_text = 'Upload attractive image(eg : Up to 50% Offer)')
    
    def __str__(self):
        return "%s" %(self.product_offer)