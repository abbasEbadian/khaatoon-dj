from django.db import models
from django.contrib.auth import get_user_model
from django.forms import IntegerField
# from order.models import Order
import random, string
User = get_user_model()


class Wallet(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE,related_name='wallet_id',  verbose_name="کاربر مربوطه")
    balance = models.IntegerField(default=0, verbose_name=" موجودی به تومان")

    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def deposit(self, amount):
        self.balance += amount
        self.save()
        

    # def withdraw(self, amount, order_id):
    #     self.balance -= amount
    #     self.transaction_set.create(amount=amount, type="purchase_withdraw", order_id=order_id, status="done", description=''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)))
    #     self.save()
        

    def __str__(self):
        return self.user_id.username

    class Meta: 
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول ها"

TRANSACTION_TYPES = [
    ('bank_deposit', 'واریز بانکی'),
    ('point_deposit', 'تبدیل امتیاز'),
    ('purchase_withdraw', 'خرید کارت')
]
TRANSACTION_STATUS = [
    ('pending', 'در انتظار پرداخت'),
    ('cancel', 'لغو شده'),
    ('done', 'پرداخت شده'),
]


class Transaction(models.Model):
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="کیف پول")
    # order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, verbose_name="شماره سفارش", help_text="زمانی که پرداخت مستقیم انتخاب شود ، غیر مستقیم کیف پول شارژ شده و ار آن کم می شود.")
    amount = models.IntegerField(default=0, verbose_name=" مقدار تراکنش")
    type =  models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name='نوع تراکنش ')
    status =  models.CharField(max_length=7, choices=TRANSACTION_STATUS, verbose_name='وضعیت')
    card_number =  models.CharField(max_length=16, verbose_name='شماره کارت انتخابی', null=True, blank=True)
    pay_card_number =  models.CharField(max_length=16, verbose_name='شماره کارت واریزی', null=True, blank=True)
    description =  models.CharField(max_length=200, verbose_name='توضیحات', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")    
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    @property
    def persian_type(self):
        if self.type == "bank_deposit": return "واریز بانکی"
        if self.type == "point_deposit": return "تبدیل امتیاز"

    @property
    def persian_status(self):
        if self.status == "pending": return "در انتظار پرداخت"
        if self.status == "cancel": return "لغو شده"
        if self.status == "done": return "پرداخت شده"

    # def confirm(self):
    #     if self.status == "pending":
    #         self.wallet_id.deposit(self.amount)
    #         self.status = "done"
    #     if self.order_id and self.order_id.status == "draft":
    #         self.order_id.purchase()

    #     self.save()

    # def cancel(self):
    #     self.status = "cancel"
    #     if self.order_id and self.order_id.status in ("pending", 'draft'):
    #         self.order_id.cancel()

        # self.save()
    def __str__(self):
        return str(self.id) +  ":" +str(self.amount)

    class Meta: 
        verbose_name = "تراکنش  کیف پول"
        verbose_name_plural = "تراکنش های کیف پول"
        ordering = ['-created']

