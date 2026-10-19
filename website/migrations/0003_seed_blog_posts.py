from pathlib import Path

import jdatetime
from django.core.files import File
from django.db import migrations

POSTS = [
    {
        'slug': 'apartment-plants',
        'title': 'راز شادابی گیاهان آپارتمانی',
        'image': 'blog-1.jpg',
        'jalali': (1405, 7, 2),
        'excerpt': 'نور غیرمستقیم، آبیاری وقتی خاک کمی خشک شد، و گلدانی که آب را نگه نمی‌دارد؛ سه عادت ساده که برگ‌ها را سبز نگه می‌دارد.',
        'paragraphs': [
            'بیشتر گیاهان آپارتمانی از آب زیاد خراب می‌شوند، نه از آب کم. قبل از آبیاری یک بند انگشت خاک را لمس کنید؛ اگر هنوز نم دارد، یکی دو روز صبر کنید.',
            'گلدان را جایی بگذارید که نور روز را ببیند ولی آفتاب تند ظهر مستقیم به برگ نخورد. اگر برگ‌ها رنگ‌پریده و کشیده شدند، نور کم است.',
            'هر ماه برگ‌ها را با دستمال نم‌دار گردگیری کنید تا روزنه‌ها باز بمانند. کود مایع را فقط در فصل رشد و با نصف غلظت نوشته‌شده روی بسته استفاده کنید.',
        ],
    },
    {
        'slug': 'pruning-time',
        'title': 'بهترین زمان هرس درختان',
        'image': 'blog-2.jpg',
        'jalali': (1405, 6, 28),
        'excerpt': 'هرس سنگین را به خواب زمستانی بسپارید و در تابستان فقط شاخه خشک، بیمار و مزاحم را بردارید.',
        'paragraphs': [
            'درختان خزان‌کننده را اواخر زمستان، پیش از باز شدن جوانه‌ها، هرس کنید. در این زمان شیره گیاه کمتر است و شکل تاج هم بهتر دیده می‌شود.',
            'هرس سبز تابستانه باید سبک باشد. برداشتن حجم زیاد برگ در گرما درخت را تحت فشار می‌گذارد و ممکن است سوختگی تنه ایجاد کند.',
            'ابزار را تیز و تمیز نگه دارید. برش باید مایل و نزدیک یقه شاخه باشد، نه چسبیده به تنه و نه با یک زائده بلند.',
        ],
    },
    {
        'slug': 'smart-watering',
        'title': 'آبیاری هوشمند برای باغچه‌های کوچک',
        'image': 'blog-3.jpg',
        'jalali': (1405, 6, 15),
        'excerpt': 'با یک زمان‌بندی ساده و قطره‌چکان مناسب، باغچه کوچک هم بدون اسراف آب شاداب می‌ماند.',
        'paragraphs': [
            'صبح زود بهترین زمان آبیاری است. ظهر آب سریع بخار می‌شود و شب ماندن رطوبت روی برگ، بیماری قارچی را بیشتر می‌کند.',
            'برای باغچه زیر بیست متر، یک خط قطره‌ای با تایمر ساده کافی است. درختچه‌ها قطره‌چکان بیشتر می‌خواهند و گل فصلی کمتر.',
            'هفته‌ای یک‌بار عمیق آب بدهید بهتر از هر روز آب سطحی است. ریشه دنبال رطوبت به عمق خاک می‌رود و گیاه در برابر گرما مقاوم‌تر می‌شود.',
        ],
    },
]


def seed_blog_posts(apps, schema_editor):
    BlogPost = apps.get_model('website', 'BlogPost')
    # Bundled with the app so a fresh migrate on the server can find them.
    seed_dir = Path(__file__).resolve().parent.parent / 'seed_images'
    for item in POSTS:
        if BlogPost.objects.filter(slug=item['slug']).exists():
            continue
        post = BlogPost(
            slug=item['slug'],
            title=item['title'],
            excerpt=item['excerpt'],
            body='\n\n'.join(item['paragraphs']),
            published_on=jdatetime.date(*item['jalali']).togregorian(),
            is_published=True,
        )
        image_path = seed_dir / item['image']
        if not image_path.is_file():
            raise FileNotFoundError(
                f'Seed image is missing from the deploy: {image_path}'
            )
        with image_path.open('rb') as handle:
            post.image.save(item['image'], File(handle), save=False)
        post.save()


def unseed_blog_posts(apps, schema_editor):
    BlogPost = apps.get_model('website', 'BlogPost')
    BlogPost.objects.filter(slug__in=[item['slug'] for item in POSTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_blogpost'),
    ]

    operations = [
        migrations.RunPython(seed_blog_posts, unseed_blog_posts),
    ]
