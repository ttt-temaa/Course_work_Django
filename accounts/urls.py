from django.contrib.auth.views import (LogoutView, PasswordChangeDoneView, PasswordChangeView,
                                       PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from .views import (LoginView, ProfileBlockView, ProfileDeleteView, ProfileEditView, ProfileView, RegisterView,
                    UserListView)

urlpatterns = [
    path("", view=UserListView.as_view(), name="users"),
    path("login", view=LoginView.as_view(), name="login"),
    path("logout", view=LogoutView.as_view(next_page="home"), name="logout"),
    path("signup", view=RegisterView.as_view(), name="signup"),
    path("profile", view=ProfileView.as_view(), name="profile"),
    path("profile/edit", view=ProfileEditView.as_view(), name="profile-edit"),
    path("profile/delete", view=ProfileDeleteView.as_view(), name="profile-delete"),
    path("profile/<str:username>/block", view=ProfileBlockView.as_view(), name="profile-block"),
    path(
        "password-reset",
        view=PasswordResetView.as_view(
            template_name="accounts/password_reset.html", form_class=CustomPasswordResetForm
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        view=PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>",
        view=PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html", form_class=CustomSetPasswordForm
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete",
        view=PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path(
        "password-change",
        view=PasswordChangeView.as_view(
            template_name="accounts/password_change.html", form_class=CustomPasswordChangeForm
        ),
        name="password_change",
    ),
    path(
        "password-change/done",
        view=PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done",
    ),
]
