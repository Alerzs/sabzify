import secrets

from django.db import models


_PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def format_toman(amount):
    grouped = f'{int(amount):,}'.replace(',', '٬')
    return grouped.translate(_PERSIAN_DIGITS)


def make_tracking_code():
    return 'SZ' + secrets.token_hex(3).upper()


def make_shop_code():
    return 'KD' + secrets.token_hex(3).upper()


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


class BlogPost(models.Model):
    title = models.CharField('عنوان', max_length=200)
    slug = models.SlugField('نامک', max_length=80, unique=True, allow_unicode=True)
    excerpt = models.TextField('خلاصه')
    body = models.TextField(
        'متن',
        help_text='هر پاراگراف را با یک خط خالی از پاراگراف بعدی جدا کنید.',
    )
    image = models.ImageField('تصویر', upload_to='blog/')
    published_on = models.DateField('تاریخ انتشار')
    is_published = models.BooleanField('منتشر شده', default=True)

    class Meta:
        verbose_name = 'نوشته'
        verbose_name_plural = 'وبلاگ'
        ordering = ['-published_on', '-pk']

    def __str__(self):
        return self.title

    @property
    def date(self):
        from .jalali import format_jalali
        return format_jalali(self.published_on)

    @property
    def paragraphs(self):
        return [part.strip() for part in self.body.split('\n\n') if part.strip()]


class Product(models.Model):
    KIND_CHOICES = [
        ('solid', 'جامد'),
        ('liquid', 'مایع'),
        ('powder', 'پودر'),
    ]

    title = models.CharField('نام محصول', max_length=160)
    slug = models.SlugField('نامک', max_length=80, unique=True)
    summary = models.CharField('خلاصه', max_length=240)
    description = models.TextField(
        'توضیح',
        help_text='هر پاراگراف را با یک خط خالی از پاراگراف بعدی جدا کنید.',
    )
    usage = models.TextField('طرز مصرف')
    price = models.PositiveIntegerField('قیمت (تومان)')
    unit = models.CharField('واحد فروش', max_length=80)
    suitable_for = models.CharField('مناسب برای', max_length=160)
    kind = models.CharField('نوع', max_length=16, choices=KIND_CHOICES, default='solid')
    image = models.CharField(
        'آدرس تصویر',
        max_length=200,
        blank=True,
        help_text='مسیر فایل داخل پوشه static. مثال: img/products/humic-acid.png',
    )
    is_available = models.BooleanField('قابل سفارش', default=True)
    sort_order = models.PositiveSmallIntegerField('ترتیب نمایش', default=0)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'فروشگاه کود'
        ordering = ['sort_order', 'pk']

    def __str__(self):
        return self.title

    @property
    def price_display(self):
        return format_toman(self.price)

    @property
    def paragraphs(self):
        return [part.strip() for part in self.description.split('\n\n') if part.strip()]


class ShopOrder(models.Model):
    STATUS_CHOICES = [
        ('new', 'در انتظار تماس کارشناس'),
        ('contacted', 'تماس گرفته شد'),
        ('preparing', 'در حال آماده‌سازی'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('cancelled', 'لغو شده'),
    ]
    STATUS_HINTS = {
        'new': 'درخواست خرید ثبت شده است. کارشناس برای تأیید تعداد و آدرس با شما تماس می‌گیرد.',
        'contacted': 'کارشناس با شما تماس گرفته است. پس از هماهنگی، کود آماده ارسال می‌شود.',
        'preparing': 'سفارش تأیید شده و در حال بسته‌بندی است.',
        'shipped': 'کود ارسال شده و در راه آدرس شماست.',
        'delivered': 'سفارش تحویل داده شده است.',
        'cancelled': 'این سفارش لغو شده است. برای ثبت دوباره به فروشگاه برگردید.',
    }

    tracking_code = models.CharField(
        'کد پیگیری',
        max_length=12,
        unique=True,
        editable=False,
        default=make_shop_code,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='محصول',
        on_delete=models.PROTECT,
        related_name='orders',
    )
    product_title = models.CharField('نام محصول در زمان سفارش', max_length=160)
    unit_price = models.PositiveIntegerField('قیمت واحد (تومان)')
    unit_label = models.CharField('واحد', max_length=80)
    quantity = models.PositiveSmallIntegerField('تعداد', default=1)
    full_name = models.CharField('نام و نام خانوادگی', max_length=120)
    phone = models.CharField('شماره تماس', max_length=20)
    city = models.CharField('شهر', max_length=80)
    address = models.TextField('آدرس')
    note = models.TextField('توضیحات', blank=True)
    status = models.CharField(
        'وضعیت',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    created_at = models.DateTimeField('تاریخ ثبت', auto_now_add=True)

    class Meta:
        verbose_name = 'سفارش فروشگاه'
        verbose_name_plural = 'سفارش‌های فروشگاه'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tracking_code} — {self.full_name}'

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    @property
    def total_display(self):
        return format_toman(self.total_price)

    @property
    def unit_price_display(self):
        return format_toman(self.unit_price)

    @property
    def status_hint(self):
        return self.STATUS_HINTS.get(self.status, '')
