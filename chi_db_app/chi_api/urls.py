from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home_page),
    path("vehicles", views.vehicle_list, name='vehicle_list'),
    path("vehicle/<int:id>", views.vehicle, name='vehicle'),
    path("customer_list", views.customer_list, name='customer_list'),
    path("customer/<int:id>", views.customer, name='customer'),
    path("customer-form", views.customer_form, name='customer_form'),
]