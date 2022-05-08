from django.contrib import admin
from .models import Reminder
# Register your models here.
    
@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'created'
    list_display = ('product_id', 'created', 'user_id')
    list_display_links = ('product_id', 'user_id')
