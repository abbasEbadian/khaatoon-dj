from django.db import models
from solo.models import SingletonModel
# Create your models here.
import uuid
def get_file_path_for_avatar(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/index/%s.%s" % (uuid.uuid4(), ext)
    return  filename

class WebsiteConfiguration(SingletonModel):
    index_title = models.CharField(max_length=100, verbose_name="تایتل صفحه اصلی", null=True, blank=True)
    index_description = models.TextField(verbose_name="متا دسکریپشن صفحه صالی ", null=True, blank=True)
    index_keywords = models.TextField(verbose_name="متا کیوردز صفحه اصلی", null=True, blank=True)
    
    index_main_image = models.ImageField(verbose_name="عکس بزرگ صفحه اصلی ", upload_to=get_file_path_for_avatar )
    index_main_image_link = models.TextField(verbose_name="لینک عکس بزرگ صفحه اصلی")
    index_main_image_1 = models.ImageField(verbose_name="عکس کوچک اول صفحه اصلی", upload_to=get_file_path_for_avatar)
    index_main_image_1_link = models.TextField(verbose_name="لینک عکس کوچک اول صفحه اصلی")
    index_main_image_2 = models.ImageField(verbose_name="عکس کوچک دوم صفحه اصلی", upload_to=get_file_path_for_avatar)
    index_main_image_2_link = models.TextField(verbose_name="لینک عکس کوچک دوم صفحه اصلی")


    shop_title = models.CharField(max_length=100, verbose_name="تایتل صفحه اصلی فروشگاه", null=True, blank=True)
    shop_description = models.TextField(verbose_name="متا دسکریپشن صفحه اصلی فروشگاه ", null=True, blank=True)
    shop_keywords = models.TextField(verbose_name="متا کیوردز صفحه اصلی فروشگاه", null=True, blank=True)

    blog_title = models.CharField(max_length=100, verbose_name="تایتل صفحه اصلی بلاگ", null=True, blank=True)
    blog_description = models.TextField(verbose_name="متا دسکریپشن صفحه اصلی بلاگ ", null=True, blank=True)
    blog_keywords = models.TextField(verbose_name="متا کیوردز صفحه اصلی بلاگ", null=True, blank=True)

    

    def __str__(self):
        return "تنظیمات وبسایت"
    class Meta:
        verbose_name = "تنظیمات وبسایت"
        verbose_name_plural = "تنظیمات وبسایت"
