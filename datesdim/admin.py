from django.contrib import admin

# Register your models here.
from datesdim.models import DateDim


class DateDimAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'day', 'day_name')
    list_filter = ('year', 'month')


admin.site.register(DateDim, DateDimAdmin)