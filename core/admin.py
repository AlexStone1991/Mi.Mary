# core/admin.py
from django.contrib import admin
from .models import Service, Order, Review, Category, TimeSlot

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "is_popular"]
    list_editable = ["is_popular"]
    search_fields = ["name"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "client_name", "status", "appointment_date"]
    list_filter = ["status", "appointment_date"]
    filter_horizontal = ["services"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "client_name", "rating", "status", "created_at"]
    list_filter = ["status", "rating"]
    actions = ["publish_reviews"]

    def publish_reviews(self, request, queryset):
        queryset.update(status="published")
    publish_reviews.short_description = "Опубликовать выбранные отзывы"

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ["date_time", "is_booked"]
    list_filter = ["is_booked"]
    list_editable = ["is_booked"]
    ordering = ["date_time"]
