from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views
app_name = 'users'

urlpatterns = [
    path("users/", views.UserListView.as_view(), name="users"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="mailing:index"), name="logout",),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", views.email_verification, name="email-confirm"),
    path("users/<int:pk>/block", views.UserBlockView.as_view(), name="user_block"),
    path("password_reset/", auth_views.PasswordResetView.as_view(
            template_name="password_reset/password_reset_form.html",
            email_template_name="password_reset/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete")), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/password_reset_complete.html"), name="password_reset_complete",),

]
