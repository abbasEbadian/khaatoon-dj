from django.contrib import admin
from .models import Ticket, TicketMessage, ContactUs
# Register your models here.
from django.contrib.auth import get_user_model
User = get_user_model()



class UnitInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    readonly_fields = ('address_report',)   
    # exclude = ('user_id', )
    
    
    @admin.display(description='فرستنده')
    def address_report(self, instance):
        
        return str(instance.user_id)
    
    address_report.short_description = "فرستنده"
    def get_formset(self, request, obj=None, **kwargs):
        q = super(UnitInline, self).get_formset(request, obj, fields=["user_id", "message"])
        if obj:
            q.form.base_fields["user_id"].queryset = User.objects.filter(pk__in=[request.user.id, obj.user_id.id])
        
        return q



    
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # readonly_fields = ('user_id', )
    list_display = ('id', 'user_id', 'title', 'status', 'priority', 'section','created' )
    list_display_links = ('user_id', )
    
    inlines = [
        UnitInline
    ]
    def save_model(self, request, obj, form, change):
        for o in obj.ticketmessage_set.all():
            if o.user_id is None:
                o.user_id = request.user
                o.save()
        obj.seen_by_user = True
        obj.save()
        super().save_model(request, obj, form, change)


    def render_change_form(self, request, context, *args, **kwargs):
        
        context.update({'save_text': True})
        return super().render_change_form(request, context, *args, **kwargs)

@admin.register(ContactUs)
class TicketAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name', 'email', 'message')
    list_display_links = ( 'name',  )
    