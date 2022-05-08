from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()


class Favorite(models.Model):
    product_id = models.ForeignKey(Product, verbose_name="محصول", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تایرخ بروزرسانی")

    def __str__(self):
        return   str(self.id)

    

    class Meta:
        verbose_name="علاقه مندی"
        verbose_name_plural="علاقه مندی ها"


