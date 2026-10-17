from django.contrib import admin

from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_code',
        'full_name',
        'phone',
        'service',
        'city',
        'status',
        'created_at',
    )
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('tracking_code', 'full_name', 'phone', 'email', 'city')
    list_editable = ('status',)
    readonly_fields = ('tracking_code', 'created_at')
    ordering = ('-created_at',)
