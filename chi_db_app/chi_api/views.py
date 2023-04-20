from django.db import connections
from django.shortcuts import render

from django.http import HttpResponse

from chi_api.models import Vehicle, Customer, Employee
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


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

    histories = []
    for history in vehicle.vehiclehistory_set.all():
        histories.append(history)

    context = {
        "vehicle": vehicle,
        "histories": histories
    }
    return HttpResponse(template.render(context, request))


def customer_list(request):
    cursor = connections['default'].cursor()

    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    template = loader.get_template('chi_api/customer_list.html')
    context = {
        "customer_list": customers
    }
    return HttpResponse(template.render(context, request))


def customer(request, id) :
    cursor = connections['default'].cursor()
    cursor.execute("SELECT * FROM customer "
                   "WHERE customer.customer_id = %s", [id])
    customer = cursor.fetchone()
    cursor.execute("SELECT * FROM vehicle_transaction "
                   "LEFT JOIN vehicle "
                   "ON vehicle_transaction.vehicle_id = vehicle.vehicle_id "
                   "LEFT JOIN employee "
                   "ON vehicle_transaction.employee_id = employee.employee_id " 
                   "WHERE customer_id = %s", [id])
    transactions = cursor.fetchall()
    template = loader.get_template('chi_api/customer.html')
    context = {
        "customer": customer,
        "transactions": transactions
    }
    return HttpResponse(template.render(context, request))

def delete_customer(request, id):
    cursor = connections['default'].cursor()
    cursor.execute("DELETE * FROM Customer WHERE customer.id= %s", id)

    return redirect("chi_api/customer_list.html")




@csrf_exempt
def customer_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        license_number = request.POST.get('license_number', '')
        license_state = request.POST.get('license_state', '')
        insurance_provider = request.POST.get('insurance_provider', '')
        policy_number = request.POST.get('policy_number', '')
        cursor = connections['default'].cursor()
        db_response = cursor.execute("INSERT INTO customer "
                                     "(name, license_number, license_state, insurance_provider, policy_number) "
                                     "VALUES (%s, %s, %s, %s, %s)",
                                     [name, license_number, license_state, insurance_provider, policy_number])
        return HttpResponse('successfully submitted')

    template = loader.get_template('chi_api/customer_form.html')
    return HttpResponse(template.render(request=request))


def employee_list(request):
    cursor = connections['default'].cursor()

    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    template = loader.get_template('chi_api/employee_list.html')
    context = {
        "employee_list": employees
    }
    return HttpResponse(template.render(context, request))


def employee(request, id):
    cursor = connections['default'].cursor()
    cursor.execute("SELECT * FROM employee "
                   "WHERE employee_id = %s", [id])
    employee = cursor.fetchone()
    cursor.execute("SELECT * FROM vehicle_transaction "
                   "LEFT JOIN vehicle "
                   "ON  vehicle_transaction.vehicle_id = vehicle.vehicle_id "
                   "LEFT JOIN customer "
                   "ON  vehicle_transaction.employee_id = customer.customer_id "
                   "WHERE employee_id = %s", [id])
    transactions = cursor.fetchall()
    template = loader.get_template("chi_api/employee.html")

    context = {
        "employee": employee,
        "transactions": transactions
    }
    return HttpResponse(template.render(context, request))