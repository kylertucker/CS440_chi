from django.db import connections
from django.shortcuts import render

from django.http import HttpResponse

from chi_api.models import Vehicle, Customer, Employee
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect

from .models import Vehicle


def home_page(request):
    template = loader.get_template("chi_api/home_page.html")
    return HttpResponse(template.render(request=request))


# def vehicle_list(request):
#     # TODO switch to sql
#     qs = Vehicle.objects.all()
#
#     template = loader.get_template("chi_api/vehicle_list.html")
#     context = {
#         "vehicle_list": qs,
#     }
#     return HttpResponse(template.render(context, request))

from django.db import connection
from django.http import HttpResponse
from django.template import loader

def vehicle_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM vehicle')
        rows = cursor.fetchall()
        vehicles = []
        for row in rows:
            vehicle = {
                'vehicle_id': row[0],
                'vin': row[1],
                'make': row[2],
                'model': row[3],
                'year': row[4],
                'trim': row[5],
                'color': row[6],
                'mpg': row[7],
                'mileage': row[8],
                'country_of_assembly': row[9]
            }
            vehicles.append(vehicle)

    template = loader.get_template('chi_api/vehicle_list.html')
    context = {
        'vehicle_list': vehicles,
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


# def employee_list(request):
#     cursor = connections['default'].cursor()
#
#     cursor.execute("SELECT * FROM employee")
#     employees = cursor.fetchall()
#     template = loader.get_template('chi_api/employee_list.html')
#     context = {
#         "employee_list": employees
#     }
#     return HttpResponse(template.render(context, request))

def employee_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM employee')
        rows = cursor.fetchall()
        employees = []
        for row in rows:
            employee = {
                'employee_id': row[0],
                'name': row[1],
                'job_title': row[2],
                'salary': row[3],
                'benefits': row[4]
            }
            employees.append(employee)

    template = loader.get_template('chi_api/employee_list.html')
    context = {
        'employee_list': employees,
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



@csrf_exempt
def delete_vehicle(request, id):
    cursor = connections['default'].cursor()

    # cursor.execute("DELETE FROM vehicles WHERE vin=?", (vehicle_id,))
    # cursor.execute("SELECT * FROM vehicles "
    #                "WHERE employee_id = %s", [id])

    cursor.execute("DELETE FROM vehicle WHERE vehicle_id = %s", [id])
    return redirect('vehicle_list')