from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from .views import book_slot, get_category_services
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.sitemap import StaticViewSitemap, CategorySitemap
from core.views import (
    LandingView,
    ThanksViews,
    OrdersListView,
    OrderDetailView,
    OrderCreateView,
    ReviewCreateView,
    ServicesListView,
    CategoryServicesView,
    OrderStatusUpdateView,
    AboutView
)

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('thanks/<str:source>/', ThanksViews.as_view(), name='thanks'),
    path('about/', AboutView.as_view(), name='about'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path("services_list/", ServicesListView.as_view(), name="service_list"),
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('order/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
    path('category/<int:category_id>/', CategoryServicesView.as_view(), name='category_services'),
    path('api/book-slot/<int:slot_id>/', book_slot, name='book_slot'),
    path('api/category-services/<int:category_id>/', get_category_services, name='get_category_services'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]