from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home_page),
    path("vehicles", views.vehicle_list, name='vehicle_list'),
    path("vehicle/<int:id>", views.vehicle, name='vehicle'),
    # path("temployees", views.employees, name='employees'),
    # path("customers", views.customers, name='customers'),
    # path("transactions", views.transactions, name='transactions'),
]