from django.contrib import admin
from .models import Address
# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
   
    list_display = ('user_id', "province_id", 'city_id', 'address', 'mobile', 'phone', 'postal')
    search_fields = ('user_id', "province_id", 'city_id', 'address', 'mobile', 'phone', 'postal')


