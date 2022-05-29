from django.contrib import admin
from .models import Attribute, AttributeValue, ProductAttribute
# Register your models here.
    
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'created'
    list_display = ('id', 'name' )

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'created'
    list_display = ('id', 'name' , 'attribute_id' )

@admin.register(ProductAttribute)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'created'
    list_display = ('id', 'product_id', 'product_template_id' , 'attribute_id', 'value_id' )

    
