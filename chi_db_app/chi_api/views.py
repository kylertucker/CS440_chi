from django.shortcuts import render

from django.http import HttpResponse

from chi_api.models import Vehicle
from django.template import loader


def home_page(request):
    template = loader.get_template("chi_api/home_page.html")
    return HttpResponse(template.render(request=request))

def vehicle_list(request):
    qs = Vehicle.objects.all()

    template = loader.get_template("chi_api/vehicle_list.html")
    context = {
        "vehicle_list": qs,
    }
    return HttpResponse(template.render(context, request))

def vehicle(request, id):
    vehicle = Vehicle.objects.get(pk=id)
    template = loader.get_template("chi_api/vehicle.html")
    context = {
        "vehicle": vehicle,
    }
    return HttpResponse(template.render(context, request))
