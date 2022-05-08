from django.contrib import admin
from .models import City, Province


# Register your models here.
@admin.register(Province)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = [ 'id', "name", "city_count"]
    search_fields = ["name"]
    @admin.display(description="تعداد شهر ها")
    def city_count(self, obj):
        return obj.get_city_count()


@admin.register(City)
class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'id', "name", "province_id"]
    autocomplete_fields = ["province_id"]


    