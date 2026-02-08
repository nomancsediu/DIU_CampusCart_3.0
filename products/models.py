from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    CONDITION_CHOICES = (
       ('NEW', 'New'),
       ('USED', 'Used'),
    )

    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'products')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null = True, blank=True, related_name ='products')
    title = models.CharField(max_length = 255)
    description = models.TextField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    condition = models.CharField(max_length=10,choices = CONDITION_CHOICES, default = 'USED')
    image = models.ImageField(upload_to='products/', null = True,blank = True)

    is_available = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.title
        