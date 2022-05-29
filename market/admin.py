from django.contrib import admin
from .models import Bank, BusinessType, Market, ShippingMethods

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created')
admin.site.register(Bank)
admin.site.register(BusinessType)
admin.site.register(ShippingMethods)