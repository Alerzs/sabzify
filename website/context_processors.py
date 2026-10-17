from .data import PARTNERS


def site_info(request):
    return {
        'partners': PARTNERS,
        'SITE_NAME': 'سبزیفای',
        'SITE_PHONE': '۰۲۱-۹۱۰۰۴۵۶۷',
        'SITE_PHONE_TEL': '+982191004567',
        'SITE_MOBILE': '۰۹۱۲۱۲۳۴۵۶۷',
        'SITE_MOBILE_TEL': '+989121234567',
        'SITE_ADDRESS': 'تهران، بلوار مرزداران، مجتمع الوند، واحد ۸۰۹ جنوبی',
        'SITE_EMAIL': 'info@sabzify.ir',
    }
