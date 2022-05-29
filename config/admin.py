from django.contrib import admin
from solo.admin import SingletonModelAdmin
from config.models import WebsiteConfiguration


# admin.site.register(HomeConfiguration, SingletonModelAdmin)
# admin.site.register(RulesConfiguration  , SingletonModelAdmin)
# admin.site.register(SMSConfiguration  , SingletonModelAdmin)
# admin.site.register(SaleConfiguration  , SingletonModelAdmin)
# admin.site.register(AboutConfiguration  , SingletonModelAdmin)
# admin.site.register(WebsiteConfiguration  , SingletonModelAdmin)


@admin.register(WebsiteConfiguration)
class WebsiteAdmin(SingletonModelAdmin):
    fieldsets = (
        ('سئو', {'fields': ('index_title', 'index_description','index_keywords', 'shop_title', 'shop_description','shop_keywords'
        ,'blog_title', 'blog_description','blog_keywords')}),
        ('تصاویر', {
            'fields': ('index_main_image', 'index_main_image_1','index_main_image_2'),
        }),
    )
