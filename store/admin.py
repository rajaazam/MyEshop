from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order



class adminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class adminCategory(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.
admin.site.register(Product, adminProduct)
admin.site.register(Category, adminCategory)
admin.site.register(Customer)
admin.site.register(Order)

