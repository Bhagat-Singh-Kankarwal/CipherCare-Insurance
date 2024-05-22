from django.contrib import admin
from .models import InsuranceData

# Register your models here.

# admin.site.register(InsuranceData)


@admin.register(InsuranceData)
class InsuranceDataAdmin(admin.ModelAdmin):
    fields = ('user', 'approved')