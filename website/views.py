from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .data import FEATURED, POSTS, SERVICES, STATS, STEPS, TESTIMONIALS
from .forms import ContactForm, ServiceRequestForm
from .models import ServiceRequest


def home(request):
    return render(request, 'website/home.html', {
        'services': SERVICES[:6],
        'featured': FEATURED,
        'stats': STATS,
        'testimonials': TESTIMONIALS,
        'posts': POSTS,
        'steps': STEPS,
    })


def about(request):
    return render(request, 'website/about.html', {'stats': STATS[:4]})


def services(request):
    return render(request, 'website/services.html', {'services': SERVICES})


def blog(request):
    return render(request, 'website/blog.html', {'posts': POSTS})


def blog_detail(request, slug):
    post = next((item for item in POSTS if item['slug'] == slug), None)
    if post is None:
        raise Http404
    others = [item for item in POSTS if item['slug'] != slug]
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
    if code:
        item = ServiceRequest.objects.filter(tracking_code=code).first()
    return render(request, 'website/track.html', {
        'code': code,
        'item': item,
        'searched': bool(code),
    })


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save()
        return redirect('request_success', code=item.tracking_code)
    return render(request, 'website/contact.html', {'form': form})
