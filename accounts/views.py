from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Count, Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from mailing.models import Mailing

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import User


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    permission_required = "view_all_users"
    context_object_name = "users"

    def get_queryset(self):
        # Annotate with mailing count and prefetch related mailings
        return User.objects.annotate(mailing_count=Count("mailings")).prefetch_related(
            Prefetch("mailings", queryset=Mailing.objects.all())
        )


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        user = form.save()
        send_welcome_email(user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("login")


class LoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class ProfileView(DetailView):
    model = User
    template_name = "accounts/profile.html"

    def get_object(self):
        return self.request.user


class ProfileEditView(UpdateView):
    form_class = ProfileForm
    template_name = "accounts/profile_form.html"

    def get_success_url(self):
        return reverse_lazy("profile")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Профиль успешно обновлён!")
        return super().form_valid(form)

    def get_object(self):
        return self.request.user


class ProfileDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("home")

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        messages.success(self.request, "Профиль успешно удалён!")
        return super().delete(request, *args, **kwargs)


class ProfileBlockView(PermissionRequiredMixin, View):
    permission_required = "accounts.can_block_user"

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(self.request, "Пользователь успешно разблокирован!")
        else:
            user.is_active = False
            user.save()
            messages.success(self.request, "Пользователь успешно заблокирован!")
        return redirect("users")


def send_welcome_email(user: User):
    subject = "Добро пожаловать в MahiruMailing!"
    message = """
    Спасибо, что присоединились к MahiruMailing! Мы рады приветствовать вас в нашем сообществе.

    Вы теперь можете наслаждаться всеми преимуществами нашего магазина, включая:
    - Просмотр и покупку самых популярных товаров в различных категориях.
    - Легкость поиска нужных товаров благодаря удобной навигации по каталогу.
    - Получение эксклюзивных предложений и акций только для зарегистрированных пользователей.

    Чтобы начать, вы можете посетить наш каталог товаров по следующей ссылке:
    https://localhost:8000/

    Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться к нашей службе поддержки:
    - Email: support@mahirumailing.com
    - Телефон: +7(123)456-78-90

    С уважением,
    Команда MahiruStore
    """

    # Email settings from settings.py should be configured
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # from email
        [user.email],  # recipient list
    )
