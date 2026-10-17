from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('request/', views.request_create, name='request'),
    path('request/success/<str:code>/', views.request_success, name='request_success'),
    path('track/', views.track, name='track'),
    path('contact/', views.contact, name='contact'),
]
