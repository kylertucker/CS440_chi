from django.db import connections
from django.shortcuts import render, redirect

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

@csrf_exempt
def add_vehicle_history(request, id):

    vehicle = Vehicle.objects.get(pk=id)

    if request.method == 'POST':
        history_type = request.POST.get('history_type', '')
        history_date = request.POST.get('history_date', '')
        description = request.POST.get('history_description', '')

        cursor = connections['default'].cursor()
        db_response = cursor.execute("INSERT INTO vehicle_history"
                                     "(history_type, history_date, description, vehicle_id)"
                                     "VALUES (%s, %s, %s, %s)", [history_type, history_date, description, id])

        return redirect('vehicle', id=id)

    context = {
        "vehicle": vehicle
    }
    return render(request, 'chi_api/add_vehicle_history.html', context)

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

def employee_sales_stats(request, id):
    template = loader.get_template('chi_api/employee_sales_stats.html')

    cursor = connections['default'].cursor()

    cursor.execute("SELECT * FROM employee "
                   "WHERE employee_id = %s", [id])
    employee = cursor.fetchone()

    total_sales = cursor.execute("SELECT %s, SUM(sale_price) "
                                 "FROM vehicle_transaction "
                                 "WHERE employee_id = %s "
                                 "GROUP BY %s", [id, id, id])
    total_sales = cursor.fetchone()

    average_sales = cursor.execute("SELECT %s, ROUND(AVG(sale_price)) "
                                   "FROM vehicle_transaction "
                                   "WHERE employee_id = %s "
                                   "GROUP BY %s", [id, id, id])
    average_sales = cursor.fetchone()

    total_transactions = cursor.execute("SELECT %s, COUNT(sale_price) "
                                        "FROM vehicle_transaction "
                                        "WHERE employee_id = %s "
                                        "GROUP BY %s", [id, id, id])
    total_transactions = cursor.fetchone()

    context = {
        'employee': employee,
        'total_sales': total_sales,
        'average_sales': average_sales,
        'total_transactions': total_transactions
    }

    return HttpResponse(template.render(context, request))

def update_customer(request, id):
    customer = Customer.objects.get(pk=id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        license_number = request.POST.get('license_number', '')
        license_state = request.POST.get('license_state', '')
        insurance_provider = request.POST.get('insurance_provider', '')
        policy_number = request.POST.get('policy_number', '')

        cursor = connections['default'].cursor()
        db_response = cursor.execute(
            "UPDATE customer "
            "SET name = %s, license_number = %s, license_state = %s, insurance_provider = %s, policy_number = %s "
            "WHERE customer_id = %s",
            [name, license_number, license_state, insurance_provider, policy_number, id]
        )

        return redirect('customer', id=id)

    context = {'customer': customer}
    return render(request, 'chi_api/update_customer.html', context)


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
                   "ON  vehicle_transaction.customer_id = customer.customer_id "
                   "WHERE employee_id = %s", [id])
    transactions = cursor.fetchall()
    template = loader.get_template("chi_api/employee.html")

    context = {
        "employee": employee,
        "transactions": transactions
    }
    return HttpResponse(template.render(context, request))

def employee_form(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employe_id', '')
        employee_name = request.POST.get('employee_name', '')
        job_title = request.POST.get('job_title', '')
        salary = request.POST.get('salary', '')
        benefits = request.POST.get('benefits', '')
        cursor = connections['default'].cursor()
        db_response = cursor.execute("INSERT INTO employee "
            "(employee_id, employee_name, job_title, salary, benefits) "
            "VALUES (%s, %s, %s, %s, %s)",
            [employee_id, employee_name, job_title, salary, benefits])
        return HttpResponse('successfully submitted')

    template = loader.get_template('chi_api/employee_form.html')
    return HttpResponse(template.render(request=request))