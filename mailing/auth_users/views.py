from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse

from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserCreationForm, CustomLoginForm, ResetPasswordForm, NewPasswordForm, CustomUserUpdateForm
from .models import CustomUser, ResetPassword, NewPassword


class RegisterView(CreateView):
    model = CustomUser
    template_name = "auth_users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("auth_users:confirm_email_views")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = default_token_generator.make_token(user)
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        current_site = get_current_site(self.request)
        mail_subject = "Activate your account"
        message = render_to_string(
            "auth_users/verify_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": uid,
                "token": user.token,
            },
        )
        user.email_user(mail_subject, message, "serega94nn@yandex.ru")

        return super(RegisterView, self).form_valid(form)


class UserLoginView(LoginView):
    model = CustomUser
    form_class = CustomLoginForm
    template_name = "auth_users/login.html"
    success_url = reverse_lazy("mailing_service:home_views")


class ActivateAccount(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and token == user.token:
            user.is_active = True
            user.save()
            return redirect(reverse_lazy("auth_users:login_views"))
        else:
            return HttpResponse("Activation link is invalid")


class ResetPasswordView(CreateView):
    model = ResetPassword
    form_class = ResetPasswordForm
    template_name = "auth_users/password_reset.html"
    # success_url = reverse_lazy("auth_users:login_views")

    def form_valid(self, form):
        data = form.cleaned_data
        email = data["email"]
        try:
            user = CustomUser.objects.filter(email=email)[0]
        except IndexError:
            return HttpResponse("ERROR: вы ввели неверный Email")

        token = user.token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        message = render_to_string(
            "auth_users/password_reset_email.html",
            {
                "uid": uid,
                "token": token,
            },
        )

        if user:
            send_mail(
                "Восстановите пароль",
                message,
                "serega94nn@yandex.ru",
                [
                    email,
                ],
            )

        return redirect(reverse_lazy("auth_users:login_views"))


class NewPasswordView(CreateView):
    template_name = "auth_users/new_password.html"
    form_class = NewPasswordForm
    success_url = reverse_lazy("auth_users:login_views")
    model = NewPassword

    def form_valid(self, form):
        data = form.cleaned_data
        email = data["email"]
        password1 = data["password1"]
        password2 = data["password2"]
        user = CustomUser.objects.filter(email=email)[0]
        if user and password1 == password2:
            user.password = make_password(password1)
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(self.request)
            message = render_to_string(
                "auth_users/verify_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": uid,
                    "token": user.token,
                },
            )
            send_mail(
                "Восстановите пароль",
                message,
                "serega94nn@yandex.ru",
                [
                    email,
                ],
            )
            return redirect(reverse_lazy("auth_users:login_views"))


class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "auth_users/custom_user_detail.html"
    context_object_name = "user"


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "auth_users/custom_user_update.html"
    context_object_name = "user"

    def get_success_url(self):
        return reverse_lazy("auth_users:custom_user_detail_views", args=[self.kwargs.get("pk")])


class UnauthorizedUserListView(TemplateView):
    template_name = "auth_users/unauthorized_user.html"


# @method_decorator(cache_page(60 * 15), name='dispatch')
class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "auth_users/custom_users.html"
    success_url = reverse_lazy("mailing_service:home_views")
    context_object_name = "users"

    def get_queryset(self):
        # Получаем только активные объекты
        if self.request.user.has_perm("customuser.can_view_all_custom_user_lists"):
            return CustomUser.objects.all()


class ConfirmEmailView(TemplateView):
    template_name = "auth_users/confirm_email.html"


class BlockUserView(LoginRequiredMixin, View):

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)

        user.is_active = False
        user.save()

        return redirect("auth_users:custom_users_views")


class UnblockUserView(LoginRequiredMixin, View):

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)

        user.is_active = True
        user.save()

        return redirect("auth_users:custom_users_views")
