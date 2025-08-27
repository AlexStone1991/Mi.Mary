from django.shortcuts import redirect
from .forms import UserRegistrationForm, UserLoginForm, CustomPasswordChangeForm, CustomSetPasswordForm, CustomPasswordResetForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import UserProfileUpdateForm

# Юзер профиль
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile_detail.html"
    context_object_name = "user_profile"
    
    def get_object(self, queryset=None):
        return self.request.user
    
# Юзер редактирование и обновления профиля

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = "profile_update_form.html"
    context_object_name = "user_profile"

    def get_object(self, queryset = None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy("profile_detail")
    
# Восстановаление пароля
class CustomPasswordResetView(PasswordResetView):
    template_name = "users_login_registr.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password_reset_done")
    email_template_name = "password_reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Восстановление пароля" # operation_type - переменная для кнопки!
        return context
    
# Восстановаление пароля(инструкции)
class CustomPasswordResetDoneView(PasswordResetDoneView):
    message = "Инструкции по всстановалению пароля отправлены на Ваш EMAIL"
    operation_type = "ВНИМАНИЕ!"

    template_name = "users_message.html"
    extra_context = {
        "operation_type": operation_type,
        "message": message,
    }

# Смена пароля
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    operation_type = "Сменить пароль"
    extra_context = {"operation_type": operation_type}
    form_class = CustomSetPasswordForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("password_reset_complete")

# Смена пароля(успешно)
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    message = "Вы успешно сменили пароль!"
    operation_type = "ВНИМАНИЕ!"
    extra_context = {
        "operation_type": operation_type,
        "message": message,
    }
    template_name = "users_message.html"

# Регистрация
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")
    success_message = "Вы успешно зарегистрировались! Добро пожаловать!"

    def form_valid(self, form):
        user = form.save()
        self.object = user
        login(self.request, user)
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        messages.error(
            self.request, "Ощибка регистрации. Пожалуйста, проверьте введенные данные!"
        )
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Регистрация"
        return context
    
# Логин/Авторизация
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")
    success_message = "Вы успешно вошли в систему!"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка входа. Пожалуйста, проверьте введеные данные!"
        )
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Вход"
        context["is_auth_form"] = True
        return context
    
    # Логаут
class UserLogoutView(LogoutView):
    next_page = "/"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "Вы успешно вышли из системы!")
        return response
        
# Смена пароля(Авторизация пользователя)
class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")

    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Смена пароля"
        return context
    