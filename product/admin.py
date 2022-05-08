from .models import Product
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    
    summernote_fields = ['description']
    date_hierarchy = 'created'
    list_display = [ 'id', "name", 'price', "category_id"]


    
   

    # @admin.display(description="نام کامل")
    # def _name(self, obj):
    #     return obj.__str__()
