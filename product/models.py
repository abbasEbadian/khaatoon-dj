from django.db import models
from category.models import Category
from state.models import City
import uuid


class ImageAlbum(models.Model):
    def default(self):
        return self.images.filter(default=True).first()
   

class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)


def get_file_path_for_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/products/%s-%s.%s" % (instance.id, uuid.uuid4(), ext)
    return  filename


class Product(models.Model):
    name            = models.CharField(max_length= 255, verbose_name="نام محصول")
    category_id     = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="دسته بندی",null=True)
    city_id         = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name="شهر",null=True)
    rate            = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="میانگین امتیاز", default=1)
    sales_amount    = models.IntegerField( verbose_name="مجموع فروش", default=0, help_text="اتوماتیک")
    sales_count     = models.IntegerField( verbose_name="تعداد فروش", default=0, help_text="اتوماتیک")
    count           = models.IntegerField( verbose_name="تعداد موجود ", default=1 )
    price           = models.DecimalField(max_digits=9, decimal_places=0, verbose_name="قیمت به تومان", null=True, blank=True)
    active          = models.BooleanField(default=True, verbose_name="نمایش در وبسایت")
    description     = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    image           = models.ImageField(verbose_name="َتصویر شاخص", upload_to=get_file_path_for_image, null=True, blank=True) 
    image_1         = models.ImageField(verbose_name="َتصویر 1", upload_to=get_file_path_for_image, null=True, blank=True) 
    image_2         = models.ImageField(verbose_name="َتصویر 2", upload_to=get_file_path_for_image, null=True, blank=True) 
    image_3         = models.ImageField(verbose_name="َتصویر 3", upload_to=get_file_path_for_image, null=True, blank=True) 
    image_4         = models.ImageField(verbose_name="َتصویر 4", upload_to=get_file_path_for_image, null=True, blank=True) 
    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    meta_title      = models.CharField(max_length=100, verbose_name=" تایتل", null=True, blank=True)
    meta_description= models.TextField(verbose_name=" متا دسکریپشن", null=True, blank=True)
    meta_keywords   = models.TextField(verbose_name=" متا کیوردز", null=True, blank=True)
    meta_canonical   = models.TextField(verbose_name=" کنونیکال", null=True, blank=True)
    image_alt       = models.CharField(max_length=100,verbose_name="alt تصویر", null=True, blank=True)

  
    def __str__(self):      
        return self.name
    
    

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta: 
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    @property
    def url(self):
        name = self.name.strip().replace(" ", "-")
        return f"{self.id}-{name}" 
    # def get_price(self):
    #     return self.price_forced or self.price
    
    # def get_discount(self):
    #     dis = 0
    #     for off in self.offcard_set.all():
    #         dis += self.get_price()/100*off.amount
    #     return dis
    
    # def get_discounted_price(self):
    #     return self.get_price() - self.get_discount()
        
    
    # @property
    # def reviews_count(self):
    #     return len(self.review_set.all()) or 1

