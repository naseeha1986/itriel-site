from django.urls import path
from . import views

# Single-page site: one route. Every menu item is an #anchor on this page.
urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
]
