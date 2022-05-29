from django.db import models
from market.models import Market
from django.contrib.auth import get_user_model
User = get_user_model()


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    market = models.ForeignKey(Market, on_delete=models.CASCADE, verbose_name="غرفه ")
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return   "چت بین [ " + str(self.user) + " ] -> [ " + str(self.market) + " ]"

    class Meta:
        verbose_name="چت"
        verbose_name_plural="چت ها"


class Message(models.Model):
    text = models.TextField(verbose_name="متن پیام")
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name="چت مربوطه")
    sender = models.CharField(max_length=255, verbose_name="فرستنده", choices=[
        ["user", "کاربر"],
        ["market", "غرفه"]
    ])
    seen = models.BooleanField(default=False, verbose_name="دیده شده توسط مخاطب")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return   str(self.text[:30])

    @property
    def _direction(self):
        return 0
    class Meta:
        verbose_name="پیام"
        verbose_name_plural="پیام ها"

