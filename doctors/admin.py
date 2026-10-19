from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'specialization', 'license_number', 'hospital', 'created_at')
    list_filter = ('specialization', 'created_at')
    search_fields = ('name', 'email', 'license_number', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
