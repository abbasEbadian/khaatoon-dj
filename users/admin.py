from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from django.core.mail import send_mail

import jdatetime
from datetime import timedelta 


class CustomUserAdmin(UserAdmin):    
    ordering =["-id"]  
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['id','first_name', 'last_name' ,'email', 'username', 'authentication_status', "reg_date", "is_vendor"]
    list_display_links = ['username', ]
    search_fields = ('username', )
    list_filter = ('is_vendor', )
    fieldsets = (
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name','username', 'email', 'national_code','gender','birth_date','password')}),
        ('احراز هویت', {
            'fields': ('authentication_status', 'national_card_image', 'birth_card_image', 'avatar_image', ),
            'classes': ('wide', 'extrapretty'),
            }),
        ('دسترسی ها', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups'),
            'classes': ('wide', 'extrapretty'),
            }),

    )

    
    # def render_change_form(self, request, context, *args, **kwargs):
    #     """We need to update the context to show the button."""
    #     context.update({'accept_authentication': True})
    #     context.update({'reject_authentication': True})
    #     return super().render_change_form(request, context, *args, **kwargs)

    # def response_post_save_change(self, request, obj):
    #     """This method is called by `self.changeform_view()` when the form
    #     was submitted successfully and should return an HttpResponse.
    #     """
        # Check that you clicked the button `_save_and_copy`
        # if 'accept_authentication' in request.POST:
        #     obj.authentication_status = "authorized"
        #     send_mail(" تایید حساب کاربری"
        #     , "کاربر گرامی احراز هویت حساب شما با موفقیت انجام شد. \n با تشکر \n https://GiftStop.org", None, [obj.email])

        #     obj.save()
        #     conf = SMSConfiguration.objects.get()
        #     send_sms(obj.username, conf.auth_accepted_sms_code)



        # return super().response_post_save_change(request, obj)
            


    

   

    @admin.display(description='تاریخ ثبت نام')
    def reg_date(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.date_joined + timedelta(hours=4, minutes=30)).strftime('%H:%M:%S %Y/%m/%d')


admin.site.register(CustomUser, CustomUserAdmin)

