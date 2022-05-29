from datetime import datetime, timedelta
from address.models import Address
import jdatetime
import string, random
from django.db import models
from market.models import Market
from product.models import Product, ProductTemplate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, mail_admins
from django.contrib import messages
from django.db.models import Count
# from config.models import SaleConfiguration
# from brands.models import Brand
# from sms.core import send_authentication_required_for_purchase_sms, send_purchaced_but_no_cards_sms, send_purchased_cards_sms
# import requests
# from sms.views import send_sms, send_sms_order_pending
# from config.models import SMSConfiguration

User = get_user_model()


class Discount(models.Model):
    # brand_id = models.ForeignKey(Brand, verbose_name="دسته بندی مربوطه", on_delete=models.CASCADE)
    amount  = models.IntegerField(verbose_name="مقدار به درصد")
    expire = models.PositiveSmallIntegerField(verbose_name="اعتبار به روز") 
    uid = models.CharField(max_length=10, verbose_name="کد", default=''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تایرخ بروزرسانی")

    def __str__(self):
        return  str(self.amount)

    class Meta:
        verbose_name="کد تخفیف"
        verbose_name_plural="کدهای تخفیف"



STATUS_LIST = [
    ("draft", "سبد خرید"),
    ("cancel", "لغو شده"),
    ("decomposed", "تفکیک شده"),
    ("pending", "در حال آماده سازی"),
    ("done", "موفق"),
]
class Order(models.Model):
    status = models.CharField(max_length=30, choices=STATUS_LIST, verbose_name="وضعیت")
    is_satisfied = models.BooleanField(default=True,  verbose_name="آماده فروش")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    order_code = models.CharField(max_length=10, verbose_name="شماره سفارش", blank=True, null=True, help_text="اتوماتیک")
    purchased_date = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ انجام پرداخت ")  
    delivery_date = models.DateTimeField(blank=True, null=True, verbose_name="مهلت ارسال")  
    points = models.IntegerField(verbose_name="امتیاز", help_text="امتیاز کسب شده از خرید", default=0)
    points_converted = models.BooleanField(verbose_name="امتیازات به کیف پول انتقال یافته", default=False)
    discount_id = models.ForeignKey(Discount, verbose_name="کد تخفیف اعمال شده", null=True, blank=True, on_delete=models.CASCADE)
    original_order_id = models.ForeignKey('self', verbose_name="سفارش مادر", related_name="sub_orders", on_delete=models.CASCADE, null=True, blank=True)
    address_id = models.ForeignKey(Address, verbose_name="آدرس انتخابی", null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    # ip = models.CharField(max_length=50, verbose_name="IP کاربر", null=True, blank=True)
    # ip_location = models.CharField(max_length=100, verbose_name="موقعیت کاربر", null=True, blank=True)
    
    @property
    def lines(self):
        if self.original_order_id:
            return self.original_lines
        return self.orderline_set


    def apply_discount(self, discount_obj):
        self.discount_id = discount_obj
        DiscountUsage.objects.get_or_create(discount_id=discount_obj, user_id=self.user_id)
        self.save()
        return True

    def remove_discount(self):
        if not self.discount_id: return
        try: 
            d = DiscountUsage.objects.get(discount_id=self.discount_id, user_id=self.user_id)
            self.discount_id = None
            d.delete()
            self.save()
        except Exception as e :
            print(e)
            return True

    def cancel(self):
        if self.status == "pending": 
            self.status = "cancel"


    def get_total(self):
        p = sum([x.get_price() for x in self.lines.iterator()])

        return p

    def get_discount(self):
        dis = 0
        for line in self.lines.all():
            if line.template_id :
                dis += line.template_id.get_discount()
        
        return dis

    

    def get_final_price(self):
        return self.get_total() - self.get_discount()


    def get_discount_code_amount(self):
        if self.discount_id:
            return self.get_final_price() / 100 * (self.discount_id.amount)
        return 0


    def __str__(self):
        return self.order_code or ""
    
    def save(self, *args, **kwargs):
        if self and self.id and not self.order_code:
            self.order_code = "SO"+str(1000 + self.id)

        
        super().save(*args, **kwargs)
    class Meta:
        verbose_name="سفارش"
        verbose_name_plural="سفارش ها"

    def update_is_satisfied(self):
        # cards = len(Card.objects.filter(orderline__isnull=True))
        # null_lines = len(self.orderline_set.filter(card_id__isnull=True))
        # valid = (cards) >= (null_lines)
        # self.is_satisfied = valid
        self.save()

    def generate_email_template(self):
        x = "ضمن قدردانی بابت خرید شما از وبسایت گیفت استاپ"
        x += "\n"
        for line in self.lines.all():
            x+= str(line.template_id) +" : \n\tPIN:"+  str(line.card_id.pin) + (" \n\tPIN2: " + str(line.card_id.pin2) if  line.card_id.pin2 else " ")
            x+='\n'
          
        x += "با تشکر "
        x += "\n"

        x += "https://giftstop.org"
        return x

    def get_jalali_payment_date(self):
        if not self.purchased_date:
            return "پرداخت انجام نشده"
        return jdatetime.datetime.fromgregorian(datetime=self.purchased_date + timedelta(hours=4, minutes=30)).strftime("%H:%M:%S %Y-%m-%d")

    def get_products_count(self):
        return sum([x.count for  x in self.lines.all()])
         

    def get_status_text(self):
        return dict(STATUS_LIST).get(self.status)
        
    def get_jalali_order_date(self):
        return jdatetime.datetime.fromgregorian(datetime=self.created + timedelta(hours=4, minutes=30)).strftime("%H:%M:%S %Y-%m-%d")

    def assign_delivery_date(self):
        if self.purchased_date and not self.delivery_date:
            if self.lines.count():
                days = max([x.product_id.preperation_time for x in self.lines.iterator()])
                self.delivery_date = self.purchased_date + timedelta(days=days) 
        self.save()

    

    def purchase(self, request=None):
        # If payment is done purchase it
        try:
            now = datetime.now()
            lines = self.orderline_set
            subs = set([x.market_id.id for x in lines.all()])
            groups = [list(lines.filter(market_id__id=x)) for x in subs]
            self.purchased_date = now
            self.status = "decomposed"
            self.assign_delivery_date()
            for idx, group in enumerate(groups):
                order_code = str(self.order_code) + chr(65 + idx)

                sub_order = self.sub_orders.create(
                    order_code=order_code,
                    purchased_date=now,
                    user_id=self.user_id,
                    status="pending",
                    address_id=self.address_id,
                )
                
                for line in group: 
                    line.sub_order_id = sub_order
                    line.save()
                sub_order.save()
                sub_order.assign_delivery_date()
            self.save()
        except Exception as e: 
            print(e, "order purchase model")
        
    

    
    
    @receiver(post_save, sender=Product)
    def aftercreate(sender, instance, created, **kwargs):
        if created:
            for order in Order.objects.filter(status="pending"):
                order.update_is_satisfied()
                order.save()
       


class OrderLine(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="سفارش مربوطه ")
    sub_order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='original_lines', verbose_name="زیر سفارش مربوطه ", null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول", null=True, blank=True)
    template_id = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE, verbose_name="قالب محصول", null=True, blank=True)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE, verbose_name="فروشگاه", null=True, blank=True)
    count = models.IntegerField(verbose_name="تعداد")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تایرخ بروزرسانی")

    def __str__(self):
        return  str(self.id) 

    def get_status_text(self):
        return dict(STATUS_LIST).get(self.order_id.status)
    

    def get_price(self):
        return self.product_id.price * self.count


    class Meta:
        verbose_name="خط سفارش"
        verbose_name_plural="خط سفارش ها"
        



    

class DiscountUsage(models.Model):
    user_id = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.CASCADE)
    discount_id = models.ForeignKey(Discount, verbose_name="کد تخفیف", on_delete=models.CASCADE)
   
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return  str(self.id)

    

    class Meta:
        verbose_name="استفاده کننده کد تخفیف "
        verbose_name_plural="استفاده کننده های کد تخفیف"

