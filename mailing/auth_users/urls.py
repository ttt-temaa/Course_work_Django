from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "auth_users"

urlpatterns = [
    path("register_views/", views.RegisterView.as_view(), name="register_views"),
    path("login_views/", views.UserLoginView.as_view(), name="login_views"),
    path("logout_views/", LogoutView.as_view(next_page="mailing_service:home_views"), name="logout_views"),
    path("activate_views/<uidb64>/<token>/", views.ActivateAccount.as_view(), name="activate_views"),
    path("password_reset_views/", views.ResetPasswordView.as_view(), name="password_reset_views"),
    path("new_password_views/<uidb64>/<token>/", views.NewPasswordView.as_view(), name="new_password_views"),
    path("custom_user_detail_views/<int:pk>/", views.CustomUserDetailView.as_view(), name="custom_user_detail_views"),
    path("custom_user_update_views/<int:pk>/", views.CustomUserUpdateView.as_view(), name="custom_user_update_views"),
    path("unauthorized_user_views/", views.UnauthorizedUserListView.as_view(), name="unauthorized_user_views"),
    path("custom_users_views/", views.CustomUserListView.as_view(), name="custom_users_views"),
    path("confirm_email_views/", views.ConfirmEmailView.as_view(), name="confirm_email_views"),
    path("block_user_views/<int:pk>/", views.BlockUserView.as_view(), name="block_user_views"),
    path("unblock_user_views/<int:pk>/", views.UnblockUserView.as_view(), name="unblock_user_views"),
]
