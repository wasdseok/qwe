from django.urls import path

from . import views

urlpatterns=[
    path("", views.main),
    path("login", views.login),
    path("signin", views.signin),
]
