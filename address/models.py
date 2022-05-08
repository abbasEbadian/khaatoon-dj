from django.db import models
from state.models import City, Province

from django.contrib.auth import get_user_model
User = get_user_model()

class Address(models.Model):
    user_id = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name="آدرس منتخب", default=False)
    province_id = models.ForeignKey(Province, verbose_name="استان", on_delete=models.SET_NULL, null=True, blank=True)
    city_id = models.ForeignKey(City, verbose_name="شهر", on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(verbose_name="آدرس")    
    mobile = models.CharField(verbose_name="شماره همراه", max_length=11)
    phone = models.CharField(verbose_name="شماره ثابت", max_length=12)
    postal = models.CharField(verbose_name="کدپستی", max_length=10)
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return   str(self.id)

    

    class Meta:
        verbose_name="آدرس"
        verbose_name_plural="آدرس ها"



