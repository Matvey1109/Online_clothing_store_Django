from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    fio = models.CharField(max_length=255)
    adress = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)


class Product(models.Model):

    AVAILABILITY =(
        ('Y', 'В наличии'),
        ('N', 'Нет в наличии'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    photo = models.ImageField(upload_to="photos/")
    size = models.CharField(max_length=255)
    availability = models.CharField(max_length=1,choices = AVAILABILITY,default = '')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    gender = models.ForeignKey('Gender', on_delete=models.PROTECT)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('', kwargs={'product_slug': self.slug})#добавить путь /gender/category
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('', kwargs={'category_slug': self.slug})#добавить путь /gender

class Gender(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('', kwargs={'gender_slug': self.slug})
class Order(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.PROTECT)
    price_order = models.IntegerField()
    product_id = models.ManyToManyField('Product')
    time_create = models.DateTimeField(auto_now_add=True)
