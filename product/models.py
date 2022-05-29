from tabnanny import verbose
from django.db import models
from category.models import Category
from state.models import City
from market.models import Market
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

def get_file_path_for_template_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/products/product%s_template-%s.%s" % (instance.product_id.id, uuid.uuid4(), ext)
    return  filename

STATUS_LIST = [
    ("pending", "در انتظار تایید"),
    ("rejected", "مشکل در تایید"),
    ("confirmed", "تایید شده"),
    ("hidden", "مخفی شده"),
]

class ProductManager(models.Manager):
    def confirmed(self):
        return self.filter(status="confirmed")

class Product(models.Model):
    name            = models.CharField(max_length= 255, verbose_name="نام محصول")
    category_id     = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="دسته بندی",null=True)
    rate            = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="میانگین امتیاز", default=1)
    sales_amount    = models.IntegerField( verbose_name="مجموع فروش", default=0, help_text="اتوماتیک")
    sales_count     = models.IntegerField( verbose_name="تعداد فروش", default=0, help_text="اتوماتیک")
    count           = models.IntegerField( verbose_name="تعداد موجود ", default=1 )
    price           = models.DecimalField(max_digits=9, decimal_places=0, verbose_name="قیمت به تومان", null=True, blank=True)
    active          = models.BooleanField(default=True, verbose_name="نمایش در وبسایت")
    description     = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    image           = models.ImageField(verbose_name="َتصویر شاخص", upload_to=get_file_path_for_image) 
    image_1         = models.ImageField(verbose_name="َتصویر 1", upload_to=get_file_path_for_image, null=True, blank=True) 
    image_2         = models.ImageField(verbose_name="َتصویر 2", upload_to=get_file_path_for_image, null=True, blank=True) 
    image_3         = models.ImageField(verbose_name="َتصویر 3", upload_to=get_file_path_for_image, null=True, blank=True) 
    image_4         = models.ImageField(verbose_name="َتصویر 4", upload_to=get_file_path_for_image, null=True, blank=True) 
    
    extra_description = models.CharField(max_length=255,blank=True,null=True, verbose_name="در صورتی که نیاز به دریافت اطلاعات بیشتر از سمت خریدار را دارید ، عنوان درخواست را اینجا وارد نمایید")
    status          = models.CharField(verbose_name="وضعیت", max_length=255, default="pending", choices=STATUS_LIST)
    published = models.BooleanField(verbose_name="نمایش در وبسایت", default=False)
    reject_reason   = models.TextField(verbose_name='دلیل رد اطلاعات', null=True, blank=True, help_text="در صورت رد تایید ، دلیل را در اینجا بنویسید تا برای کاربر نمایش داده شود.")
    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    meta_title      = models.CharField(max_length=100, verbose_name=" تایتل", null=True, blank=True)
    meta_description= models.TextField(verbose_name=" متا دسکریپشن", null=True, blank=True)
    meta_keywords   = models.TextField(verbose_name=" متا کیوردز", null=True, blank=True)
    meta_canonical   = models.TextField(verbose_name=" کنونیکال", null=True, blank=True)
    image_alt       = models.CharField(max_length=100,verbose_name="alt تصویر", null=True, blank=True)

    market_id = models.ForeignKey(Market, on_delete=models.CASCADE, verbose_name="غرفه")
    preperation_time = models.PositiveIntegerField(default=1, verbose_name="زمان آماده سازی", help_text="روز کاری مورد نیاز برای آماده سازی و ارسال")
    
    objects = ProductManager()

    def __str__(self):      
        return self.name
    
    

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta: 
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    @property
    def available_count(self):
        if self.productattribute_set.count():
            return sum([x.count for x in self.productattribute_set.all()])
        return self.count
        
    @property
    def url(self):
        name = self.name.strip().replace(" ", "-")
        return f"{self.id}-{name}" 
        
    def status_text(self):
        return dict(STATUS_LIST).get(self.status)


class ProductTemplate(models.Model):
    rate            = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="میانگین امتیاز", default=1)
    sales_amount    = models.IntegerField( verbose_name="مجموع فروش", default=0, help_text="اتوماتیک")
    sales_count     = models.IntegerField( verbose_name="تعداد فروش", default=0, help_text="اتوماتیک")
    count           = models.IntegerField( verbose_name="تعداد موجود ", default=1 )
    price           = models.DecimalField(max_digits=9, decimal_places=0, verbose_name="قیمت به تومان", null=True, blank=True)
    active          = models.BooleanField(default=True, verbose_name="نمایش در وبسایت")
    description     = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    image_1         = models.ImageField(verbose_name="َتصویر 1", upload_to=get_file_path_for_template_image, null=True, blank=True) 
    image_2         = models.ImageField(verbose_name="َتصویر 2", upload_to=get_file_path_for_template_image, null=True, blank=True) 
   
    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    default         = models.BooleanField(default=False, verbose_name="قالب اصلی", help_text="در صورتی که انتخاب شوندگی نداشته باشد") 
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
  
    def __str__(self):      
        return self.product_id and self.product_id.name or self.id
    
    

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta: 
        verbose_name = "قالب محصول"
        verbose_name_plural = "قالب محصولات"


class OffCard(models.Model):
    template_id     = models.ForeignKey(ProductTemplate, verbose_name="قالب کارت مربوطه", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(verbose_name="مقدار به درصد")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return str(self.amount)
    
    class Meta: 
        verbose_name = "تخفیف محصول"
        verbose_name_plural = "تخفیف محصول"