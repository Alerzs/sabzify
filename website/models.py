import secrets

from django.db import models


def make_tracking_code():
    return 'SZ' + secrets.token_hex(3).upper()


class ServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ('design', 'طراحی فضای سبز'),
        ('maintenance', 'نگهداری دوره‌ای'),
        ('pruning', 'هرس درختان'),
        ('planting', 'کاشت گل و گیاه'),
        ('irrigation', 'سیستم آبیاری'),
        ('lawn', 'چمن‌کاری'),
        ('roof', 'روف گاردن'),
        ('consult', 'مشاوره حضوری'),
        ('other', 'سایر خدمات'),
    ]
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('review', 'در حال بررسی'),
        ('scheduled', 'زمان‌بندی شده'),
        ('done', 'انجام شده'),
        ('cancelled', 'لغو شده'),
    ]

    full_name = models.CharField('نام و نام خانوادگی', max_length=120)
    phone = models.CharField('شماره تماس', max_length=20)
    email = models.EmailField('ایمیل', blank=True)
    city = models.CharField('شهر', max_length=80, blank=True)
    address = models.TextField('آدرس', blank=True)
    service = models.CharField('نوع خدمت', max_length=32, choices=SERVICE_CHOICES)
    area = models.CharField('متراژ تقریبی', max_length=40, blank=True)
    preferred_date = models.DateField('تاریخ ترجیحی', null=True, blank=True)
    message = models.TextField('توضیحات', blank=True)
    status = models.CharField(
        'وضعیت',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    tracking_code = models.CharField(
        'کد پیگیری',
        max_length=12,
        unique=True,
        editable=False,
        default=make_tracking_code,
    )
    created_at = models.DateTimeField('تاریخ ثبت', auto_now_add=True)

    class Meta:
        verbose_name = 'درخواست'
        verbose_name_plural = 'درخواست‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tracking_code} — {self.full_name}'
