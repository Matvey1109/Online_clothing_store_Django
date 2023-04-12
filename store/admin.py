from django.contrib import admin
from .models import *

class GenderAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name", )}

class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name", )}

class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name',\
                    'middle_name', 'email', 'date_joined','adress','phone_number')
    list_display = ('username','first_name', 'last_name',\
                    'middle_name', 'email', 'date_joined','adress','phone_number')

admin.site.register(User ,UserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gender,GenderAdmin)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OrderProduct)

