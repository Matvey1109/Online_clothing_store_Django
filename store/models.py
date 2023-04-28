from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    middle_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=13)


class Product(models.Model):

    AVAILABILITY =(
        ('Y', 'В наличии'),
        ('N', 'Нет в наличии'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    discount = models.BooleanField(default=False)
    price = models.IntegerField()
    price_discount = models.IntegerField(blank=True)
    photo = models.ImageField(upload_to="photos")
    size = models.CharField(max_length=255)
    availability = models.CharField(max_length=1,choices = AVAILABILITY,default = '')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    gender = models.ForeignKey('Gender', on_delete=models.PROTECT)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})
    def get_add_url(self):
        return reverse('add_to_cart',kwargs={'product_slug': self.slug})

    def get_add_favorite(self):
        return reverse('add_to_favorite', kwargs={'product_slug': self.slug})

    def get_delete_favorite(self):
        return reverse('delete_from_favorite', kwargs={'product_pk': self.pk})
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self, gender):
        return reverse('category', kwargs={'category_slug': self.slug, 'gender_slug': gender.slug})

class Gender(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    categories_id = models.ManyToManyField('Category')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('gender', kwargs={'gender_slug': self.slug})

class OrderProduct(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    def get_total_product_price(self):
        return self.quantity * self.product.price
class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    products = models.ManyToManyField('OrderProduct')
    time_create = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total_product_price()
        return total

    def get_total_quantity(self):
        quantity = 0
        for order_item in self.products.all():
            quantity += order_item.quantity
        return quantity
    def get_payment_url(self):
        return reverse('landing', kwargs={'order_id': self.pk})


class Address(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

class Favorite(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product')