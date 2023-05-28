from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import product

class Order(models.Model):
    id = models.AutoField(unique=True,primary_key=True,auto_created=True,verbose_name='Order Id')
    customer = models.ForeignKey(User,on_delete=CASCADE,null=True)
    orderd_date = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False,verbose_name='Order Complete')
    reference_Id = models.CharField(max_length=100,null=True,blank=True)
    order_complete_id = models.CharField(max_length=101,null=True,blank=True)
    payment_status = models.CharField(max_length=80,null=True,blank=True)
    
    def __str__(self):
        return "%s(%s)" %(self.customer,self.complete)
    
    @property
    def get_total_price(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total
    
    @property
    def get_total_item(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(to = 'product.Product',on_delete = CASCADE,null=True)
    order = models.ForeignKey(to = Order,on_delete=CASCADE,null=True)
    quantity = models.IntegerField(default = 0,null=True,blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return "%s(%s)" %(self.product,self.quantity)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    class Meta:
        verbose_name_plural = "OrderItem(Add to cart)"

status = (('Pending',"Pending"),
        ('Accepted',"Accepted"),
        ("Packed","Packed"),
        ('On The Way','On The Way'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'))
class MyOrder(models.Model):
    username = models.CharField(max_length=50)
    item = models.CharField(max_length=250)
    image = models.ImageField(verbose_name='Item Image',upload_to = 'myorder_pic')
    price = models.FloatField()
    quantity = models.IntegerField()
    total = models.FloatField()
    payment_status = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    order_complete = models.BooleanField(default = False)
    reference_id = models.CharField(max_length=90)
    order_id = models.CharField(max_length=89)
    order_complete_id = models.CharField(max_length=88)
    customer_detail = models.TextField()
    order_status = models.CharField(default="Pending",choices = status,blank=True,max_length=40)
    orderd_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s(%s)' %(self.username,self.reference_id)
    
    class Meta:
        verbose_name_plural = "User Order Completed"

class LikeProduct(models.Model):
    product = models.ForeignKey(to='product.Product',on_delete=CASCADE)
    liked_by = models.ForeignKey(to=User,on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return '%s(%s)' %(self.product,self.liked_by)
    
    class Meta:
        verbose_name_plural = "User Wish List"