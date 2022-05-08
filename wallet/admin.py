from .models import  Wallet, Transaction
from django.contrib import admin
# Register your models here.


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    read_only_fields = ('user_id', )
    list_display = ('user_id', "balance")
    list_display_links = ('user_id',)
    search_fields = ('user_id__username', 'user_id__first_name', 'user_id__last_name')

@admin.register(Transaction)
class WalletAdmin(admin.ModelAdmin):
    read_only_fields = ('wallet_id', )
    list_display = ('id', 'wallet_id', "amount", "type", "status")

 