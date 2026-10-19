from django import forms
from django.contrib import admin

from .forms import JalaliDateField
from .jalali import format_jalali
from .models import BlogPost, Product, ServiceRequest, ShopOrder, format_toman


class ServiceRequestAdminForm(forms.ModelForm):
    preferred_date = JalaliDateField(required=False, label='تاریخ ترجیحی')

    class Meta:
        model = ServiceRequest
        fields = '__all__'


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    form = ServiceRequestAdminForm
    list_display = (
        'tracking_code',
        'full_name',
        'phone',
        'service',
        'city',
        'status',
        'created_at_display',
    )
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('tracking_code', 'full_name', 'phone', 'email', 'city')
    list_editable = ('status',)
    readonly_fields = ('tracking_code', 'created_at_display')
    ordering = ('-created_at',)

    @admin.display(description='تاریخ ثبت', ordering='created_at')
    def created_at_display(self, obj):
        if obj is None or not getattr(obj, 'created_at', None):
            return '—'
        return format_jalali(obj.created_at, with_time=True)


class BlogPostAdminForm(forms.ModelForm):
    published_on = JalaliDateField(label='تاریخ انتشار')

    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'published_on_display', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    ordering = ('-published_on',)

    @admin.display(description='تاریخ انتشار', ordering='published_on')
    def published_on_display(self, obj):
        if obj is None or not getattr(obj, 'published_on', None):
            return '—'
        return format_jalali(obj.published_on)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'price_display', 'kind', 'is_available', 'sort_order')
    list_filter = ('kind', 'is_available')
    search_fields = ('title', 'summary', 'suitable_for')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_available', 'sort_order')
    ordering = ('sort_order', 'pk')

    @admin.display(description='قیمت', ordering='price')
    def price_display(self, obj):
        if obj is None or obj.price is None:
            return '—'
        return f'{format_toman(obj.price)} تومان'


@admin.register(ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_code',
        'full_name',
        'phone',
        'product_title',
        'quantity',
        'total_display',
        'status',
        'created_at_display',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('tracking_code', 'full_name', 'phone', 'city', 'product_title')
    list_editable = ('status',)
    readonly_fields = (
        'tracking_code',
        'product',
        'product_title',
        'unit_price',
        'unit_label',
        'created_at_display',
        'total_display',
    )
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    @admin.display(description='مبلغ کل')
    def total_display(self, obj):
        if obj is None or not getattr(obj, 'pk', None):
            return '—'
        return f'{obj.total_display} تومان'

    @admin.display(description='تاریخ ثبت', ordering='created_at')
    def created_at_display(self, obj):
        if obj is None or not getattr(obj, 'created_at', None):
            return '—'
        return format_jalali(obj.created_at, with_time=True)
