from django.db import migrations


PRODUCTS = [
    {
        'slug': 'vermicompost',
        'title': 'ورمی‌کمپوست خانگی',
        'summary': 'کود تیره و نرم از بستر کرم، برای تقویت خاک گلدان و باغچه.',
        'description': (
            'ورمی‌کمپوست سبزیفای از پسماند گیاهی خانگی و بستر کرم خاکی آماده شده و بوی تند کود دامی ندارد.\n\n'
            'بافت آن نرم است و رطوبت را در خاک نگه می‌دارد. برای گلدان، باغچه کوچک و نهال جوان مناسب است.'
        ),
        'usage': 'یک لایه نازک روی خاک بریزید و با آبیاری ملایم مخلوط کنید. برای باغچه، پیش از کاشت با خاک سطحی قاطی شود. مقدار دقیق را کارشناس موقع تماس می‌گوید.',
        'price': 185000,
        'unit': 'بسته ۲ کیلوگرمی',
        'suitable_for': 'گلدان، باغچه و نهال جوان',
        'kind': 'solid',
        'sort_order': 1,
    },
    {
        'slug': 'leaf-compost',
        'title': 'کمپوست برگ',
        'summary': 'خاک‌برگ پوسیده برای سبک کردن خاک و نگه داشتن رطوبت.',
        'description': (
            'کمپوست برگ از برگ‌های خشک‌شده و پوسیده آماده می‌شود و خاک سنگین را قابل‌تنفس می‌کند.\n\n'
            'برای تعویض خاک گلدان، باغچه و لایه سطحی روف‌گاردن استفاده می‌شود.'
        ),
        'usage': 'با خاک موجود به نسبت حدود یک به سه مخلوط کنید. روی سطح خاک تنها نریزید؛ باید با لایه بالایی قاطی شود.',
        'price': 145000,
        'unit': 'بسته ۵ کیلوگرمی',
        'suitable_for': 'باغچه، روف‌گاردن و تعویض خاک گلدان',
        'kind': 'solid',
        'sort_order': 2,
    },
    {
        'slug': 'compost-tea',
        'title': 'چای کمپوست',
        'summary': 'کود مایع رقیق‌شده برای آبیاری دوره‌ای گیاهان آپارتمانی.',
        'description': (
            'چای کمپوست عصاره رقیق کمپوست گیاهی است و برای تغذیه ملایم در فصل رشد استفاده می‌شود.\n\n'
            'جایگزین کود شیمیایی قوی نیست؛ برای نگهداری روزمره گلدان‌ها کافی است.'
        ),
        'usage': 'در فصل رشد، هر دو هفته یک‌بار همراه آبیاری استفاده کنید. روی برگ خیس نریزید و در گرمای ظهر کود ندهید.',
        'price': 89000,
        'unit': 'بطری ۱ لیتری',
        'suitable_for': 'گیاهان آپارتمانی و گل فصلی',
        'kind': 'liquid',
        'sort_order': 3,
    },
    {
        'slug': 'fruit-peel',
        'title': 'کود مایع پوست میوه',
        'summary': 'تغذیه پتاسیمی ملایم از پوست میوه، برای شادابی برگ و گل‌دهی.',
        'description': (
            'این کود مایع از پوست میوه خانگی تهیه و صاف شده است تا بتوانید مستقیم در آبیاری از آن استفاده کنید.\n\n'
            'برای گل‌های آپارتمانی و سبزیجات گلدانی مناسب است.'
        ),
        'usage': 'ماهی دو بار، مقدار کمی را در آب آبیاری حل کنید. اگر برگ نوک‌سوز شد، فاصله مصرف را بیشتر کنید و با کارشناس مشورت کنید.',
        'price': 76000,
        'unit': 'بطری ۱ لیتری',
        'suitable_for': 'گل‌های آپارتمانی و سبزیجات خانگی',
        'kind': 'liquid',
        'sort_order': 4,
    },
    {
        'slug': 'eggshell',
        'title': 'پودر پوسته تخم‌مرغ',
        'summary': 'منبع کلسیم برای خاک گلدان و استحکام ریشه.',
        'description': (
            'پوسته تخم‌مرغ شسته، خشک و آسیاب شده است تا دیرتر در خاک بماند و کلسیم را آهسته آزاد کند.\n\n'
            'برای گیاهانی که گل و میوه می‌دهند مفیدتر است.'
        ),
        'usage': 'یک قاشق غذاخوری را با خاک سطحی گلدان مخلوط کنید. پودر را یکجا پای ساقه تلنبار نکنید.',
        'price': 64000,
        'unit': 'بسته ۱ کیلوگرمی',
        'suitable_for': 'گوجه و فلفل گلدانی، گیاهان برگ‌درشت',
        'kind': 'powder',
        'sort_order': 5,
    },
    {
        'slug': 'wood-ash',
        'title': 'خاکستر چوب الک‌شده',
        'summary': 'مکمل پتاسیم برای خاک‌های اسیدی؛ فقط به مقدار کم.',
        'description': (
            'خاکستر چوب طبیعی، بدون زغال رنگی و خاک اضافه، الک شده و در بسته کوچک عرضه می‌شود.\n\n'
            'برای هر خاکی مناسب نیست. کارشناس هنگام تماس می‌پرسد چه گیاهی دارید و اگر خاک قلیایی باشد این کود را پیشنهاد نمی‌کند.'
        ),
        'usage': 'مقدار خیلی کم را با خاک مخلوط کنید، نه روی برگ. بدون هماهنگی با کارشناس روی گیاه حساس نریزید.',
        'price': 52000,
        'unit': 'بسته ۱ کیلوگرمی',
        'suitable_for': 'گیاهان گل‌دار و درختچه، با تأیید کارشناس',
        'kind': 'powder',
        'sort_order': 6,
    },
]


def seed_products(apps, schema_editor):
    Product = apps.get_model('website', 'Product')
    for item in PRODUCTS:
        Product.objects.update_or_create(
            slug=item['slug'],
            defaults={
                'title': item['title'],
                'summary': item['summary'],
                'description': item['description'],
                'usage': item['usage'],
                'price': item['price'],
                'unit': item['unit'],
                'suitable_for': item['suitable_for'],
                'kind': item['kind'],
                'is_available': True,
                'sort_order': item['sort_order'],
            },
        )


def unseed_products(apps, schema_editor):
    Product = apps.get_model('website', 'Product')
    Product.objects.filter(slug__in=[item['slug'] for item in PRODUCTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_product_shoporder'),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
