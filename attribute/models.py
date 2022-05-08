from django.db import models
from product.models import Product
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
User = get_user_model()


class Attribute(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام ویژگی")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تایرخ بروزرسانی")

    def __str__(self):
        return   str(self.name)

    class Meta:
        verbose_name="ویژگی"
        verbose_name_plural=" ویژگی ها"
    
    
class AttributeValue(models.Model):
    name = models.CharField(max_length=255, verbose_name="مقدار ویژگی")
    attribute_id = models.ForeignKey(Attribute, verbose_name="مشخصه", on_delete=models.CASCADE, null=True)
    color = ColorField(verbose_name="مقدار رنگ", blank=True, null=True, help_text="اگر از نوع رنگ است ، رنگ دقیق آن را نیز انتخاب نمایید")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تایرخ بروزرسانی")

    def __str__(self):
        return   str(self.name)

    class Meta:
        verbose_name="ویژگی"
        verbose_name_plural="مقادیر ویژگی"
    
class ProductAttribute(models.Model):

    product_id = models.ForeignKey(Product, verbose_name="محصول", on_delete=models.CASCADE, null=True)
    attribute_id = models.ForeignKey(Attribute, verbose_name="مشخصه", on_delete=models.CASCADE, null=True)
    value_id = models.ForeignKey(AttributeValue, verbose_name="مقدار مشخصه", on_delete=models.CASCADE, null=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return   str(self.id)

    class Meta:
        verbose_name="ویژگی محصول"
        verbose_name_plural="ویژگی محصولات"



