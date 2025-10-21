from django.db import models
from django.conf import settings
import datetime


# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.FloatField()
    image=models.CharField(max_length=800)
    category=models.CharField(max_length=200)
    stock_quantity=models.IntegerField()



    def __str__(self):
        return self.name 
    
def today():
    return datetime.datetime.now()
    
 

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)
    created_at=models.DateTimeField(default=today,null=True,blank=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order.name

