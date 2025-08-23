from .models import Order, Service, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from core.context_processors import menu_items
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Prefetch
from django.shortcuts import get_object_or_404
from .forms import OrderForm, ReviewForm
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
)

class AboutView(TemplateView):
    template_name = "about.html"

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_all = self.request.GET.get('show_all', False)

        # Отзывы с пользователями (оптимизировано)
        all_reviews = Review.objects.filter(status="published").select_related('user')
        total_reviews = all_reviews.count()
        reviews = all_reviews[:6] if not show_all else all_reviews

        # Популярные услуги
        popular_services = Service.objects.filter(is_popular=True)

        context.update({
            'reviews': reviews,
            'show_all': show_all,
            'total_reviews': total_reviews,
            'popular_services': popular_services,
        })
        return context