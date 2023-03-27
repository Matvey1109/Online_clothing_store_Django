from django.contrib import admin
from .models import *

class GenderAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name", )}

class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name", )}


admin.site.register(User)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gender,GenderAdmin)
admin.site.register(Order)

