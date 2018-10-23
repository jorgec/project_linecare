from django.contrib import admin

# Register your models here.
from appglobals.models import AppGlobal


class AppGlobalAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'value_type')
    search_fields = ('name', 'value_type')
    list_filter = ['value_type']


admin.site.register(AppGlobal, AppGlobalAdmin)
