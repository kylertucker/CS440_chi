from django.shortcuts import render

from django.http import HttpResponse

from chi_api.models import Vehicle


def index(request):
    vehicle_list = Vehicle.objects.filter()
    output = ", ".join([q.vin for q in vehicle_list])
    return HttpResponse(output)
