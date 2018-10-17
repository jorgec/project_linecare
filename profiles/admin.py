from django.contrib import admin

# Register your models here.
from profiles.models import BaseProfile, ProfilePhone


class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    list_filter = ('gender',)
    search_fields = ('first_name', 'last_name', 'user')

admin.site.register(BaseProfile, BaseProfileAdmin)


class ProfilePhoneAdmin(admin.ModelAdmin):
    list_display = ('number', 'profile', 'carrier', 'is_public', 'is_active')
    list_filter = ('profile', 'carrier', 'is_public', 'is_active')
    search_fields = ('profile', 'carrier')


admin.site.register(ProfilePhone, ProfilePhoneAdmin)