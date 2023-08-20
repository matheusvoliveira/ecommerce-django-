from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    product = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(max_length=600)
    image = models.ImageField()

    def __str__(self):
        return f'{self.product} ${self.price}'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)