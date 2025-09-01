from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import (
    LandingView,
    ThanksViews,
    OrdersListView,
    OrderDetailView,
    OrderCreateView,
    ReviewCreateView,
    ServicesListView,
)

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksViews.as_view(), name='thanks'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path("services_list/", ServicesListView.as_view(), name="service_list"),
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
]