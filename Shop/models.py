from django.contrib.auth.models import User
from django.db import models
from MyShop.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.shortcuts import reverse
# Create your models here.
CAT_CHOICES = (('A', 'Accessories'),('S','Stationary'))

class Product(models.Model):
    
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, null=True, blank=True)
    full_name = models.CharField(max_length=80)
    product_image = models.ImageField(upload_to='Product_img', null=False)
    price = models.FloatField()
    category = models.CharField(choices=CAT_CHOICES, max_length=20)
    product_desc = models.CharField(max_length=200)
    featured = models.BooleanField(default=False)
    latest = models.BooleanField(default=False)

    def __str__(self):
        return str(self.full_name)  


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def total_item_price(self):
        return self.quantity * self.item.price

    
class Order(models.Model):    
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    total_amount = models.FloatField(default=0)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    adress = models.ForeignKey('Adress',on_delete=models.SET_NULL, null=True, blank=True )
    ordered_date = models.DateTimeField()


    def __str__(self):
        return str(self.user)
    
    def total_price(self):
        total_price = 0
        for i in self.items.all():
            total_price = total_price + i.total_item_price()
        return total_price 

class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    first_adress = models.CharField(max_length=300)
    email = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=30)
    pin_code = models.IntegerField()
    contact =  models.IntegerField()
   
    def __str__(self):
        return str(self.user)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=200)   
    email = models.CharField(max_length=30)   
    phone =  models.IntegerField()
    text = models.TextField(max_length=1000)   

    def __str__(self):
        return str(self.full_name) 

def slug_generator(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=Product)
        

