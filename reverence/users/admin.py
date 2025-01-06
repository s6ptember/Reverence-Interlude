from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'middle_name',
                       'city', 'street', 'house_number',
                       'apartment_number', 'postal_code')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

    add_fieldets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 
                       'is_active', 'is_staff', 'is_superuser')
        })
    )


    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['password'].widget.attrs['readonly'] = True
        return form
