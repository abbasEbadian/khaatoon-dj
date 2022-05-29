import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from state.models import Province
import uuid
from django.db.models import Q

auth_status = [
    ('unauthorized', 'احراز نشده'),
    ('pending', 'در حال بررسی مدارک'),
    ('authorized', "احراز هویت شده")
]
def get_file_path_for_birth(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/national_cards/%s.%s" % (uuid.uuid4(), ext)
    return  filename
def get_file_path_for_national(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/birth_cards/%s.%s" % (uuid.uuid4(), ext)
    return filename
def get_file_path_for_avatar(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/avatars/%s.%s" % (uuid.uuid4(), ext)
    return  filename

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name="شماره همراه")
    authentication_status = models.CharField(max_length=20, choices=auth_status, verbose_name="وضعیت احراز هویت", default="unauthorized")
    national_code =  models.CharField(max_length=10, verbose_name="کد ملی", null=True, blank=True)
    gender = models.CharField(max_length=10, verbose_name="جنسیت", choices=[("male", 'آقا'), ('female', 'خانم')], null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ تولد")
    national_card_image =  models.ImageField(verbose_name='تصویر کارت ملی',upload_to=get_file_path_for_birth,null=True, blank=True,)
    birth_card_image =  models.ImageField(verbose_name='تصویر شناسنامه',upload_to=get_file_path_for_national,null=True, blank=True,)
    avatar_image =  models.ImageField(verbose_name='تصویر کاربری',upload_to=get_file_path_for_avatar,null=True, blank=True,)
    is_vendor = models.BooleanField(verbose_name='غرفه دار', default=False, blank=True, null=True)
    province_id = models.ForeignKey(Province, verbose_name='استان محل سکونت', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.first_name and (self.first_name +" " + self.last_name +"(" +self.username +")") or self.username

    class Meta:
        app_label= "users"
        verbose_name ="کاربر"
        verbose_name_plural ="کاربرها"
        

    @property
    def has_national_card_image(self):
        return self.national_card_image and True or False
    @property
    def has_birth_card_image(self):
        return self.birth_card_image and True or False
    @property
    def has_avatar_image(self):
        return self.avatar_image and True or False
    # @property
    # def image_tag(self):
    #     if self.birth_card_image != '':
    #         return mark_safe('<img src="%s%s" width="150" height="150" />' % (f'{settings.MEDIA_URL}images/birth_cards', self.birth_card_image))

    def get_orders(self):
        # return self.order_set.filter(~Q(status= "draft")).all()
        return self.order_set.filter(original_order_id__isnull=True).exclude(status= "draft")

    def get_unread_messages_count(self):
        c = 0
        for chat in self.chat_set.iterator():
            for message in chat.message_set.iterator():
                if message.sender == "market" and  not message.seen:
                    c += 1
        return c 