from django import forms
from .models import Order, Service, Review
from django.forms import DateTimeInput
from django import forms

class BaseBootstrapForm(forms.ModelForm):
    """Базовый класс для всех форм с Bootstrap 5."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Добавляем класс `form-control` ко всем полям
            field.widget.attrs.update({"class": "form-control"})
            # Дополнительные настройки для конкретных типов полей
            if isinstance(field, forms.DateField):
                field.widget.attrs.update({"type": "date"})
            elif isinstance(field, forms.FileField):
                field.widget.attrs.update({"class": "form-control-file"})

class OrderStatusForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        labels = {
            "status": "Статус заказа"
        }


class ReviewForm(BaseBootstrapForm):
    class Meta:
        model = Review
        fields = ["text", "client_name", "photo", "rating"]
        widgets = {
            "text": forms.Textarea(),
            "rating": forms.Select(),
        }

class ServiceForm(BaseBootstrapForm):
    class Meta:
        models = Service
        fields = ["name", "description", "price", "is_popular", "image"]
        widgets = {
            "description": forms.Textarea(),
            "price": forms.NumberInput(),
        }

class OrderForm(BaseBootstrapForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),  
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = Order
        fields = ["client_name", "phone", "comment", "appointment_date", "services"]
        widgets = {
            "client_name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            "phone": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 999-99-99'
            }),

            "comment": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий к заказу'
            }),
            'services': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input'}
            ),

            'appointment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }
