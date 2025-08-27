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

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_all = self.request.GET.get('show_all', False)

        # Отзывы с пользователями (оптимизировано)
        all_reviews = Review.objects.filter(status="published")
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

class ThanksViews(TemplateView):
    template_name = 'thanks.html'

@method_decorator(login_required, name="dispatch")
class OrdersListView(ListView):
    model = Order
    template_name = "orders_list.html"
    context_object_name = "orders"
    ordering = ["-date_created"]

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("services")
        search_query = self.request.GET.get("q", "")
        search_fields = self.request.GET.getlist("search_fields", ["client_name"])

        if search_query:
            q_objects = Q()
            if "client_name" in search_fields:
                q_objects |= Q(client_name__icontains=search_query)
            if "phone" in search_fields:
                q_objects |= Q(phone__icontains=search_query)
            if "comment" in search_fields:
                q_objects |= Q(comment__icontains=search_query)
            queryset = queryset.filter(q_objects)

        return queryset

@method_decorator(login_required, name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("services").annotate(total_price=Sum("services__price"))
    
class ServicesListView(TemplateView):
    template_name = "service_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "services": Service.objects.all(),
            "form": OrderForm(),
            "min_date": timezone.now().strftime('%Y-%m-%dT%H:%M')
        })
        return context
    
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'create_review.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, "Ваш отзыв отправлен на модерацию")
        return super().form_valid(form)
    
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, "Заявка успешно отправлена!")
        return super().form_valid(form)