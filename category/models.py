from importlib.metadata import requires
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, help_text="انگلیسی", verbose_name="نام")
    persian_name = models.CharField(max_length=80, help_text="فارسی", verbose_name="نام")
    slug_name = models.CharField(max_length=50, help_text="خودکار پر میشود", verbose_name="اسلاگ", blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تایرخ بروزرسانی")
    parent_id = models.ForeignKey('self', verbose_name="دسته بندی مادر", blank=True, null=True, on_delete=models.SET_NULL)
    meta_title      = models.CharField(max_length=100, verbose_name=" تایتل", null=True, blank=True)
    meta_description= models.TextField(verbose_name=" متا دسکریپشن", null=True, blank=True)
    meta_keywords   = models.TextField(verbose_name=" متا کیوردز", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = str(self.name).lower().replace(" ", '-')
        # if not self.meta_title:
        #     self.meta_title =  "گیفت کارت " + self.persian_name 
        # if not self.meta_description: 
        #     self.meta_description = " ".join(
        #         f"""خرید گیفت کارت {self.persian_name or ""},
        #         خرید انواع گیفت کارت {self.persian_name or ""} از چند کشور مختلف همراه با اسکن معتبر و دریافت آنی در مبالغ متنوع,
        #         گیفت کارت {self.persian_name or ""} را ارزان بخرید,
        #         """.split()
        #     )
        # if not self.meta_keywords:
        #     self.meta_keywords = " ".join(
        #         f"""خرید گیفت کارت {self.persian_name or ""},
        #         گیفت کارت ارزان {self.persian_name + " " +  self.name or ""},
        #         {self.__str__()},
        #         {self.persian_name}
        #         """.split()
        #     )
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.persian_name

    @property
    def url(self):
        name = self.persian_name.strip().replace(" ", "-")
        return f"{self.id}-{name}" 
        
    class Meta: 
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
    

