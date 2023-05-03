from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home_page, name="home"),
    path("vehicles", views.vehicle_list, name='vehicle_list'),
    path("vehicle/<int:id>", views.vehicle, name='vehicle'),
    path("customer_list", views.customer_list, name='customer_list'),
    path("customer/<int:id>", views.customer, name='customer'),
    path("customer-form", views.customer_form, name='customer_form'),
    path('customer/<int:id>/update', views.update_customer, name='update_customer'),
    path('vehicle/<int:id>/add-history', views.add_vehicle_history, name='add_vehicle_history'),
    path('vehicle-form', views.vehicle_form, name='vehicle-form'),
    path("employee-list", views.employee_list, name='employee_list'),
    path("employee/<int:id>", views.employee, name='employee'),
    path("employee/<int:id>/sales-stats", views.employee_sales_stats, name='employee_sales_stats'),
    path("employee-form", views.employee_form, name="employee-form"),
    path('employee/delete/<int:employee_id>/', views.employee_delete, name='employee_delete')
]