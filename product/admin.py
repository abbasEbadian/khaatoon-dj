from attribute.models import ProductAttribute
from .models import Product, ProductTemplate
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

class UnitInline(admin.TabularInline):
    model = ProductAttribute
    extra = 0  
    # exclude = ('user_id', )
    fields = ['product_id', 'attribute_id', 'value_id']

    @admin.display(description='محصول')
    def address_report(self, instance):
        
        return str(instance.product_id.name)
    
    
@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    
    summernote_fields = ['description']
    date_hierarchy = 'created'
    list_display = [ 'id', "name", 'price', "category_id"]

    inlines = [
        UnitInline
    ]
    
   
class UnitInline2(admin.TabularInline):
    model = ProductAttribute
    extra = 0  
    # exclude = ('user_id', )
    fields = ['product_id', 'attribute_id', 'value_id']

    @admin.display(description='محصول')
    def address_report(self, instance):
        
        return str(instance.product_template_id.price)
    
    
@admin.register(ProductTemplate)
class ProductTemplateAdmin(SummernoteModelAdmin):
    
    list_display = [ 'id', "count", 'price', 'product_id']

    inlines = [
        UnitInline2
    ]
    
   

