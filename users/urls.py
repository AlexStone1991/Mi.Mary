from django.urls import path
from .views import (
    UserLoginView,
    UserLogoutView,
    UserRegistrationView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    UserProfileDetailView,
    UserProfileUpdateView,
    )
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("change-password/", CustomPasswordChangeView.as_view(), name="change_password"),
    path("profile/", UserProfileDetailView.as_view(), name="profile_detail"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="profile_edit"),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_link"),
    path("reset/done/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    ]