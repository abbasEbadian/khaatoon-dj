from django.contrib import admin
from .models import Category
# Register your models here.
@admin.register(Category)
class BrandAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    ordering = ("name", )
    list_display = ('persian_name','name', 'parent_id', "slug_name", "created")
    search_fields= ('name', 'persian_name')
    autocomplete_fields = ['parent_id']

