from tkinter.tix import Tree
from django.contrib import admin
from .models import Order, OrderLine, Discount,DiscountUsage
from django.contrib import messages
from django.utils.html import format_html
# from django.contrib.auth import get_user_model
# User = get_user_model()
# Register your models here.
import jdatetime
from datetime import timedelta


class UnitInline(admin.TabularInline):
    model = OrderLine
    fk_name = "order_id"
    raw_id_fields = ("template_id",)
    extra = 0


class UnitInline2(admin.TabularInline):
    model = OrderLine
    fk_name = "sub_order_id"
    raw_id_fields = ("template_id",)
    extra = 0

    
        # return qs.filter(author=request.user)

# @admin.action(description='بررسی وضعیت وجود کد برای سفارش')
# def update_is_satisfied(modeladmin, request, queryset):
#     for q in queryset:
#         q.update_is_satisfied()
#         if q.is_satisfied:
#             messages.add_message(request, messages.SUCCESS,  f"سفارش {q.order_code or q.id} آماده تایید می باشد.")
#         else:
#             messages.add_message(request, messages.WARNING,  f"سفارش {q.order_code or q.id} دارای نواقص میباشد.")



@admin.action(description='ارسال کد ها')
def send_cards(modeladmin, request, queryset):
    for q in queryset:
        q.purchase(request)
        # q.update_is_satisfied()
        # if q.status.find("pending") > -1  and q.is_satisfied :
            
        # elif not q.is_satisfied:
        #     messages.add_message(request, messages.WARNING,  f"سفارش {q.order_code or q.id} دارای نواقص میباشد.")



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # date_hierarchy = 'created'
    list_display = ("order_code", "user_id", "is_satisfied", "status", "get_pdate")
    list_display_links = ("order_code", "user_id",)
    list_filter = ( 'is_satisfied', 'status')
    actions = [ send_cards ]
    search_fields = ('order_code', 'user_id__username', 'user_id__first_name')
    # inlines = [
    #     UnitInline,
    #     UnitInline2,
    # ]
    def get_inlines(self, request, obj=None):
        if not obj.original_order_id:
            return [UnitInline]
        else:
            return [UnitInline2]

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(status__in=["cancel", "pending", "pending_auth", "done"])

    @admin.display(description='تاریخ')
    def get_pdate(self, obj):
        if obj.purchased_date:
            return jdatetime.datetime.fromgregorian(datetime=obj.purchased_date + timedelta(hours=4, minutes=30)).strftime('%H:%M:%S %Y/%m/%d')
        
        return "-"



   
    def render_change_form(self, request, context, *args, **kwargs):
        """We need to update the context to show the button."""
        # if self.status.find("pending") > -1 :
        if kwargs['obj'] and kwargs['obj'].status.find("pending") > -1 :
            context.update({'send_codes': True})
        return super().render_change_form(request, context, *args, **kwargs)


    def response_post_save_change(self, request, obj):
        """This method is called by `self.changeform_view()` when the form
        was submitted successfully and should return an HttpResponse.
        """
        # Check that you clicked the button `_save_and_copy`
        if 'send_codes' in request.POST:
            obj.update_is_satisfied()
            if obj.status.find("pending") > -1  and obj.is_satisfied :
                obj.purchase(request)
            elif not obj.is_satisfied:
                messages.add_message(request, messages.WARNING,  f"سفارش {obj.order_code or obj.id} دارای نواقص میباشد.")

       


        return super().response_post_save_change(request, obj)

@admin.register(OrderLine)
class OrderAdmin(admin.ModelAdmin):
    # readonly_fields  =  ("", )

    # date_hierarchy = 'created'
    list_display = ("order_id", 'product_id')
    list_display_links = ("order_id", 'product_id')
    # list_filter = ( 'brand_id__name', 'country_id__name')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    
    list_display = ("uid", 'amount', 'expire')
    list_display_links = ("uid", )


@admin.register(DiscountUsage)
class DiscountUsageAdmin(admin.ModelAdmin):
    
    list_display = ("user_id", 'discount_id')
    list_display_links = ("user_id", )


