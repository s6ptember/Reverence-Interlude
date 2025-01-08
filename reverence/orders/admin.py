from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 
                    'created_at', 'tracking_number')
    search_fields = ('first_name', 'last_name', 'city',
                     'street', 'postal_code', 'tracking_number')
    list_filter = ('created_at',)
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name',
                       'middle_name', 'city', 'street',
                       'house_number', 'apartment_number',
                       'postal_code', 'tracking_number')
        }),
    )


admin.site.register(Order, OrderAdmin)