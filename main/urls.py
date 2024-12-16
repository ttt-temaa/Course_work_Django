from django.urls import path

from .views import ContactsPageView, HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("contacts", ContactsPageView.as_view(), name="contacts"),
]
