from .models import Order, Service, Review, Category, TimeSlot
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.context_processors import menu_items
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Prefetch
from django.shortcuts import get_object_or_404
from .forms import OrderForm, ReviewForm, OrderStatusForms
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.views.generic import UpdateView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
)


def get_category_services(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    services = category.services.all().values('id', 'name', 'price')
    return JsonResponse({'services': list(services)})


# представление для обновления статуса слота после бронирования
@csrf_exempt
@require_POST
def book_slot(request, slot_id):
    slot = TimeSlot.objects.get(id=slot_id)
    slot.is_booked = True
    slot.save()
    return JsonResponse({'success': True})


class AboutView(TemplateView):
    template_name = "about.html"


class OrderStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderStatusForms
    template_name = 'order_status_update.html'  # Убедитесь, что имя шаблона указано правильно
    success_url = reverse_lazy('order_detail')

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})



def get_min_appointment_time():
    now = datetime.now()
    # Округляем текущее время до ближайших 30 минут
    rounded_minutes = (now.minute // 30) * 30
    if now.minute % 30 >= 30:
        rounded_minutes += 30
    rounded_time = now.replace(minute=rounded_minutes, second=0, microsecond=0)
    # Если округленное время меньше текущего, добавляем час
    if rounded_time < now:
        rounded_time += timedelta(hours=1)
    return rounded_time.strftime('%Y-%m-%dT%H:%M')

def get_max_appointment_time():
    now = datetime.now()
    # Устанавливаем максимальное время на 1000 дней вперед
    max_appointment_time = now + timedelta(days=1000)
    return max_appointment_time.strftime('%Y-%m-%dT%H:%M')

class CategoryServicesView(TemplateView):
    template_name = 'category_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        context['category'] = category
        context['services'] = category.services.all()
        context['min_date'] = get_min_appointment_time()
        context['max_date'] = get_max_appointment_time()
        return context


class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        free_slots = TimeSlot.objects.filter(is_booked=False).order_by('date_time')
        context['free_slots'] = free_slots
        context["categories"] = Category.objects.all()
        context['services'] = Service.objects.all()
        show_all = self.request.GET.get('show_all', False)

        # Отзывы с пользователями (оптимизировано)
        all_reviews = Review.objects.filter(is_published=True)
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

    def get_context_data(self, **kwargs):
        """
        Расширение get_context_data для возможности передать в шаблон {{ title }} и {{ message }}.

        Они будут разные, в зависимости от куда пришел человек.
        Со страницы order/create/ с псевдонимом order-create
        Или со страницы review/create/ с псевдонимом review-create
        """
        context = super().get_context_data(**kwargs)

        if kwargs["source"]:
            source = kwargs["source"]
            if source == "create_order":
                context["title"] = "Спасибо за заказ!"
                context["message"] = (
                    "Ваш заказ принят. Скоро с вами свяжется наш менеджер для уточнения деталей."
                )
            elif source == "create_review":
                context["title"] = "Спасибо за отзыв!"
                context["message"] = (
                    "Ваш отзыв принят и отправлен на модерацию. После проверки он появится на сайте."
                )

        else:
            context["title"] = "Спасибо!"
            context["message"] = "Спасибо за ваше обращение!"

        return context

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
    success_url = reverse_lazy("thanks", kwargs={"source": "create_review"})

    def form_valid(self, form):
        messages.success(self.request, "Ваш отзыв отправлен на модерацию")
        return super().form_valid(form)

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("thanks", kwargs={"source": "create_order"})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ваша заявка принята и отправлена на модерацию")
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "services": Service.objects.all(),
            "min_date": timezone.now().strftime('%Y-%m-%dT%H:%M')
        })
        return context
