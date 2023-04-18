from django.shortcuts import render

from django.http import HttpResponse

from chi_api.models import Vehicle, Customer
from django.template import loader



def home_page(request):
    template = loader.get_template("chi_api/home_page.html")
    return HttpResponse(template.render(request=request))

def vehicle_list(request):
    # TODO switch to sql
    qs = Vehicle.objects.all()

    template = loader.get_template("chi_api/vehicle_list.html")
    context = {
        "vehicle_list": qs,
    }
    return HttpResponse(template.render(context, request))

def vehicle(request, id):
    # TODO switch to sql
    vehicle = Vehicle.objects.get(pk=id)

    template = loader.get_template("chi_api/vehicle.html")
    context = {
        "vehicle": vehicle,
    }
    return HttpResponse(template.render(context, request))

def customer_list(request):
    # TODO switch to sql
    customers = Customer.objects.all()
    template = loader.get_template('chi_api/customer_list.html')
    context = {
        "customer_list": customers
    }
    return HttpResponse(template.render(context, request))

def customer(request, id) :
    # TODO switch to sql
    customer = Customer.objects.get(pk=id)
    template = loader.get_template('chi_api/customer.html')
    transactions = []
    for transaction in customer.vehicletransaction_set.all():
        transactions.append(transaction)
    context = {
        "customer": customer,
        "transactions": transactions
    }
    return HttpResponse(template.render(context, request))

