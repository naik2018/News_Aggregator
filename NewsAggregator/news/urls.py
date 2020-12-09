from django.contrib import admin
from django.urls import path
from news import views
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
urlpatterns = [
    path('', views.home, name ="home"),
    path(r'^favicon\.ico$', favicon_view),
]