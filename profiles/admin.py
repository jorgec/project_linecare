from django.contrib import admin

# Register your models here.
from profiles.models import BaseProfile, ProfilePhone, Gender


class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'first_name', 'last_name')
    list_filter = ('gender',)
    search_fields = ('first_name', 'last_name', 'user')
    ordering = ('-created',)

admin.site.register(BaseProfile, BaseProfileAdmin)


class ProfilePhoneAdmin(admin.ModelAdmin):
    list_display = ('number', 'profile', 'carrier', 'is_public', 'is_active')
    list_filter = ('profile', 'carrier', 'is_public', 'is_active')
    search_fields = ('profile', 'carrier')


admin.site.register(ProfilePhone, ProfilePhoneAdmin)


class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Gender, GenderAdmin)