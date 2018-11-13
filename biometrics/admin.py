from django.contrib import admin

# Register your models here.
from biometrics.models import Biometric


class BiometricAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'weight', 'blood_type')


admin.site.register(Biometric, BiometricAdmin)
