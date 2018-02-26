from django.contrib import admin
from .models import Order, OrderLine, OrderHistoryEntry, DeliveryGroup

admin.site.register(OrderHistoryEntry)
admin.site.register(OrderLine)

class DeliveryGroupInline(admin.TabularInline):
    model = DeliveryGroup
    raw_id_fields = ['order']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 
    'address', 'city', 'paid',
    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [DeliveryGroupInline]

admin.site.register(Order, OrderAdmin)
