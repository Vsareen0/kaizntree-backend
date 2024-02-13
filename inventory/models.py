from django.db import models
from users.models import User
from datetime import datetime

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Tags are created seperate
class Tags(models.Model):
    name = models.CharField(max_length=100)
    img = models.TextField()
    
    def __str__(self):
        return self.name


# Items in inventory
class Item(models.Model):
    sku = models.CharField(max_length = 100, unique=True)
    name = models.CharField(max_length = 100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_stock = models.IntegerField()
    available_stock = models.IntegerField()
    tags = models.ManyToManyField(Tags)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    