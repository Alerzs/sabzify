from django.shortcuts import get_object_or_404, redirect, render

from .data import FEATURED, SERVICES, STATS, STEPS
from .forms import ContactForm, ServiceRequestForm, ShopOrderForm
from .models import BlogPost, Product, ServiceRequest, ShopOrder


def home(request):
    return render(request, 'website/home.html', {
        'services': SERVICES[:6],
        'featured': FEATURED,
        'stats': STATS,
        'posts': BlogPost.objects.filter(is_published=True)[:3],
        'steps': STEPS,
        'shop_products': Product.objects.filter(is_available=True)[:3],
    })


def about(request):
    return render(request, 'website/about.html', {'stats': STATS[:4]})


def services(request):
    return render(request, 'website/services.html', {'services': SERVICES})


def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'website/blog.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    others = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)
    return render(request, 'website/blog_detail.html', {'post': post, 'others': others})


def request_create(request):
    initial = {}
    selected = request.GET.get('service')
    valid = {key for key, _label in ServiceRequest.SERVICE_CHOICES}
    if request.method != 'POST' and selected in valid:
        initial['service'] = selected

    form = ServiceRequestForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        item = form.save()
        return redirect('request_success', code=item.tracking_code)
    return render(request, 'website/request_form.html', {'form': form})


def request_success(request, code):
    item = get_object_or_404(ServiceRequest, tracking_code=code)
    return render(request, 'website/request_success.html', {'item': item})


def track(request):
    code = request.GET.get('code', '').strip().upper()
    item = None
    kind = None
    if code:
        item = ServiceRequest.objects.filter(tracking_code=code).first()
        if item:
            kind = 'service'
        else:
            item = ShopOrder.objects.filter(tracking_code=code).select_related('product').first()
            if item:
                kind = 'shop'
    return render(request, 'website/track.html', {
        'code': code,
        'item': item,
        'kind': kind,
        'searched': bool(code),
    })


def shop(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'website/shop.html', {'products': products})


def shop_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    form = ShopOrderForm(request.POST or None, product=product)
    if request.method == 'POST' and form.is_valid():
        order = form.save()
        return redirect('shop_success', code=order.tracking_code)
    return render(request, 'website/shop_detail.html', {
        'product': product,
        'form': form,
    })


def shop_success(request, code):
    order = get_object_or_404(ShopOrder, tracking_code=code)
    return render(request, 'website/shop_success.html', {'order': order})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save()
        return redirect('request_success', code=item.tracking_code)
    return render(request, 'website/contact.html', {'form': form})
