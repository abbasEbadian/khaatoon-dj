from django.contrib import admin
from .models import Bank, BusinessType, Market

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created')
admin.site.register(Bank)
admin.site.register(BusinessType)