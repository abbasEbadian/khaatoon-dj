from django.db import models

class Province(models.Model):
    name = models.CharField(max_length= 255, verbose_name="نام استان")
    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):      
        return self.name

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_city_count(self):
        return self.city_set.count()

    class Meta: 
        verbose_name = "استان"
        verbose_name_plural = "استان ها"

class City(models.Model):
    name = models.CharField(max_length= 255, verbose_name="نام شهر")
    province_id = models.ForeignKey(Province, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="استان مربوطه")

    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):      
        return self.name
    
    

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    class Meta: 
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"