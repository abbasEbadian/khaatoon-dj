from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model
from order.models import Order
User = get_user_model()


class Ticket(models.Model):
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE,  verbose_name="کاربر",)
    status           = models.CharField(max_length=255, verbose_name="وضعیت", choices=[
        ("pending", "در انتظار پاسخ"),
        ("answered", "پاسخ داده شده"),
        ("closed", "بسته شده")
    ])
    title           = models.CharField(max_length=255, verbose_name="عنوان")
    section         = models.CharField(max_length=128, verbose_name="بخش مربوطه") 
    priority        = models.CharField(max_length=128, verbose_name="اولویت")
    order_id        = models.ForeignKey(Order,on_delete=models.CASCADE, verbose_name="سفارش مربوطه", null=True, blank=True)

    seen_by_user    = models.BooleanField(verbose_name="سین شده توسط کاربر", default=False)
    seen_by_admin   = models.BooleanField(verbose_name="سین شده توسط ادمین", default=False)
    
    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")   

    def __str__(self):
        return  str(self.id) 


    def save(self, *args, **kwargs):
        last_ticket =  self.ticketmessage_set.order_by('-id').first()
        if self and last_ticket  and self.status !="closed":
            if last_ticket.user_id and last_ticket.user_id.is_superuser :
                self.status = "answered"
            else:
                self.status = "pending"

        super(Ticket, self).save(*args, **kwargs)
    class Meta:
        verbose_name="تیکت"
        verbose_name_plural="تیکت ها"

    

class TicketMessage(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE )
    message = models.TextField(verbose_name="پیام")
    

    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")  
    def __str__(self):
        return str(self.id)
    
   
    class Meta:
        verbose_name="پیام تیکت"
        verbose_name_plural="پیام های تیکت"


from django.dispatch import receiver
from django.db.models.signals import post_save
@receiver(post_save, sender=TicketMessage)
def aftercreate(sender, instance, created, **kwargs):
    if created and instance.ticket_id and instance.ticket_id.status !="closed":
        if instance.user_id and (instance.user_id.is_superuser or instance.user_id.is_staff):
            instance.ticket_id.status = "answered"
        else:
            instance.ticket_id.status = "pending"
    
    instance.ticket_id.save()




class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی", null=True, blank=True)
    email = models.CharField(max_length=100, verbose_name="ایمیل", null=True, blank=True)
    message = models.TextField(verbose_name="پیام",  null=True, blank=True)
    

    created         = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated         = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")  
    def __str__(self):
        return str(self.id)
    
   
    class Meta:
        verbose_name="تماس با ما"
        verbose_name_plural="تماس با ما"