from django.contrib import admin
from .models import Message, Chat
import jdatetime


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'sender', '_date', "chat_id")


    @admin.display(description="تاریخ")
    def _date(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.created).strftime("%Y-%m-%d %H:%M:%S")

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'market', '_date')


    @admin.display(description="تاریخ")
    def _date(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.created).strftime("%Y-%m-%d %H:%M:%S")