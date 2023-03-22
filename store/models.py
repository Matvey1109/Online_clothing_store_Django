from django.db import models

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
