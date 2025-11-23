from django.contrib import admin

from stripe_api.models import Item, Order, OrderItem, Discount, Tax

models = [Item, Order, OrderItem, Discount, Tax]

admin.site.register(models)
