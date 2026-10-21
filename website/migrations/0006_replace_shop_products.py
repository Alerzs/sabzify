from django.db import migrations


OLD_SLUGS = [
    'vermicompost',
    'leaf-compost',
    'compost-tea',
    'fruit-peel',
    'eggshell',
    'wood-ash',
]

PRODUCTS = [
    {
        'slug': 'humic-acid',
        'title': 'کود هیومیک اسید',
        'summary': 'بهبود ساختار خاک و جذب بهتر آب و مواد غذایی برای ریشه.',
        'description': (
            'هیومیک اسید از مواد آلی خاک می‌آید و ریشه را برای گرفتن آب و کود آماده‌تر می‌کند. خاک سفت را نرم‌تر می‌کند و اثر کودهای دیگر را بهتر نشان می‌دهد.\n\n'
            'برای گلدان، باغچه، درخت و گیاهانی که رشدشان کند شده مناسب است. جای برنامه تغذیه را نمی‌گیرد و همراه آن استفاده می‌شود.'
        ),
        'usage': 'در آب آبیاری رقیق شود و پای ریشه داده شود. روی برگ غلیظ نریزید. فاصله و مقدار را کارشناس با توجه به نوع گیاه می‌گوید.',
        'price': 220000,
        'unit': 'بطری ۱ لیتری',
        'suitable_for': 'گلدان، باغچه و درخت',
        'kind': 'liquid',
        'sort_order': 1,
    },
    {
        'slug': 'amino-acid',
        'title': 'کود آمینو اسید',
        'summary': 'محرک رشد برای دوران تنش، جابه‌جایی گلدان و ضعف برگ.',
        'description': (
            'آمینو اسید به گیاه کمک می‌کند انرژی‌اش را صرف ساخت پروتئین و سبز ماندن برگ کند. بعد از گرما، جابه‌جایی یا توقف رشد، اثرش واضح‌تر است.\n\n'
            'برای محلول‌پاشی و آبیاری رقیق استفاده می‌شود و با برنامه کودی اصلی همراه است.'
        ),
        'usage': 'در هوای خنک صبح یا عصر، رقیق‌شده روی برگ اسپری شود. ظهر و زیر آفتاب مستقیم استفاده نکنید. اگر نوک برگ سوخت، غلظت را کم کنید و با کارشناس مشورت کنید.',
        'price': 245000,
        'unit': 'بطری ۱ لیتری',
        'suitable_for': 'گیاهان آپارتمانی، نشا و باغچه',
        'kind': 'liquid',
        'sort_order': 2,
    },
    {
        'slug': 'npk-12-12-36',
        'title': 'کود 12-12-36',
        'summary': 'پتاسیم بالا برای گل‌دهی، میوه‌دهی و درشت شدن محصول.',
        'description': (
            'فرمول ۱۲-۱۲-۳۶ نیتروژن و فسفر متعادل دارد و پتاسیم آن بالاست. پتاسیم به تشکیل گل، پر شدن میوه و مقاومت گیاه در برابر تنش کمک می‌کند.\n\n'
            'برای گوجه، فلفل، صیفی و درخت میوه در مرحله گل و میوه مناسب‌تر از مرحله‌ای است که گیاه فقط برگ می‌سازد.'
        ),
        'usage': 'در آب حل شود و همراه آبیاری مصرف شود. در مرحله رشد برگ، این فرمول انتخاب اول نیست. مقدار را کارشناس موقع تماس می‌گوید.',
        'price': 185000,
        'unit': 'بسته ۱ کیلوگرمی',
        'suitable_for': 'گل، صیفی و درخت میوه',
        'kind': 'powder',
        'sort_order': 3,
    },
    {
        'slug': 'npk-20-20-20',
        'title': 'کود 20-20-20',
        'summary': 'کود کامل و متعادل برای رشد عمومی برگ، ساقه و ریشه.',
        'description': (
            'فرمول ۲۰-۲۰-۲۰ نیتروژن، فسفر و پتاسیم را به نسبت برابر دارد. وقتی گیاه در حال رشد کلی است و هنوز به کود تخصصی گل یا ریشه نیاز ندارد، انتخاب ساده‌ای است.\n\n'
            'برای گیاهان آپارتمانی، سبزیجات و باغچه در فصل رشد مناسب است.'
        ),
        'usage': 'در آب آبیاری حل شود. فاصله مصرف را فشرده نکنید؛ کود زیاد برگ را می‌سوزاند. در خواب زمستانی گیاه استفاده نکنید.',
        'price': 165000,
        'unit': 'بسته ۱ کیلوگرمی',
        'suitable_for': 'گیاهان آپارتمانی، سبزی و باغچه',
        'kind': 'powder',
        'sort_order': 4,
    },
    {
        'slug': 'npk-10-52-10',
        'title': 'کود 10-52-10',
        'summary': 'فسفر بالا برای ریشه‌زایی، استقرار نشا و شروع گل‌دهی.',
        'description': (
            'فرمول ۱۰-۵۲-۱۰ فسفر زیادی دارد. فسفر به ساخت ریشه قوی و استقرار گیاه بعد از کاشت یا تعویض گلدان کمک می‌کند و شروع گل را پشتیبانی می‌کند.\n\n'
            'برای نشا، قلمه ریشه‌دار و اوایل فصل مناسب است. وقتی میوه در حال درشت شدن است، کود پتاس‌بالا جایگزین بهتری است.'
        ),
        'usage': 'موقع کاشت یا اوایل رشد، رقیق در آب آبیاری استفاده شود. پشت سر هم و بدون فاصله مصرف نکنید. کارشناس با دیدن مرحله رشد گیاه مقدار را مشخص می‌کند.',
        'price': 198000,
        'unit': 'بسته ۱ کیلوگرمی',
        'suitable_for': 'نشا، قلمه و شروع گل‌دهی',
        'kind': 'powder',
        'sort_order': 5,
    },
]


def replace_products(apps, schema_editor):
    Product = apps.get_model('website', 'Product')
    Product.objects.filter(slug__in=OLD_SLUGS).update(is_available=False)
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


def restore_products(apps, schema_editor):
    Product = apps.get_model('website', 'Product')
    Product.objects.filter(slug__in=[item['slug'] for item in PRODUCTS]).delete()
    Product.objects.filter(slug__in=OLD_SLUGS).update(is_available=True)


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_seed_products'),
    ]

    operations = [
        migrations.RunPython(replace_products, restore_products),
    ]
