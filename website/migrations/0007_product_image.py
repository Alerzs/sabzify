from django.db import migrations, models


IMAGE_BY_SLUG = {
    'humic-acid': 'img/products/humic-acid.png',
    'amino-acid': 'img/products/amino-acid.png',
    'npk-12-12-36': 'img/products/npk-12-12-36.png',
    'npk-20-20-20': 'img/products/npk-20-20-20.png',
    'npk-10-52-10': 'img/products/npk-10-52-10.jpg',
}

NEW_PRODUCTS = [
    {
        'slug': 'calcium',
        'title': 'کود کلسیم',
        'summary': 'ساقه‌های محکم‌تر و برگ‌های سالم‌تر، با کاهش ریزش گل و برگ.',
        'description': (
            'کلسیم ساقه را محکم‌تر می‌کند و کیفیت و مقاومت ساقه و برگ را بالا می‌برد. ریزش گل و برگ را کم می‌کند و به درمان پیچ‌خوردگی و بدشکلی برگ کمک می‌کند.\n\n'
            'برای تمامی گیاهان، ماهی یک بار و به‌صورت محلول‌پاشی استفاده می‌شود.'
        ),
        'usage': '۲ گرم در ۱ لیتر آب حل شود و روی برگ محلول‌پاشی شود. هر یک ماه یک بار. زیر آفتاب مستقیم اسپری نکنید.',
        'price': 190000,
        'unit': 'بسته',
        'suitable_for': 'تمامی گیاهان',
        'kind': 'powder',
        'image': 'img/products/calcium.png',
        'sort_order': 6,
    },
    {
        'slug': 'seaweed',
        'title': 'کود جلبک دریایی',
        'summary': 'رشد بهتر، تحمل بیشتر و برگ‌های پهن‌تر.',
        'description': (
            'جلبک دریایی به شادابی گیاه، تحمل تنش‌های محیطی و پهن شدن برگ کمک می‌کند و تعداد جوانه‌ها را بیشتر می‌کند.\n\n'
            'برای گیاهان آپارتمانی و بقیه گیاهان، هم در آبیاری و هم به‌صورت محلول‌پاشی رقیق استفاده می‌شود.'
        ),
        'usage': '۱ قاشق چای‌خوری در ۱.۵ لیتر آب. برای آبیاری یا محلول‌پاشی. هر یک ماه یک بار برای تمامی گیاهان.',
        'price': 230000,
        'unit': 'بطری',
        'suitable_for': 'گیاهان آپارتمانی و تمامی گیاهان',
        'kind': 'liquid',
        'image': 'img/products/seaweed.png',
        'sort_order': 7,
    },
]


def set_product_images(apps, schema_editor):
    Product = apps.get_model('website', 'Product')
    for slug, image in IMAGE_BY_SLUG.items():
        Product.objects.filter(slug=slug).update(image=image)
    for item in NEW_PRODUCTS:
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
                'image': item['image'],
                'is_available': True,
                'sort_order': item['sort_order'],
            },
        )


def clear_product_images(apps, schema_editor):
    Product = apps.get_model('website', 'Product')
    Product.objects.filter(slug__in=[item['slug'] for item in NEW_PRODUCTS]).delete()
    Product.objects.filter(slug__in=IMAGE_BY_SLUG).update(image='')


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_replace_shop_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.CharField(
                blank=True,
                help_text='مسیر فایل داخل پوشه static. مثال: img/products/humic-acid.png',
                max_length=200,
                verbose_name='آدرس تصویر',
            ),
        ),
        migrations.RunPython(set_product_images, clear_product_images),
    ]
