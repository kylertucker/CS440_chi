from django.db import models


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, blank=False, null=False)
    vin = models.CharField(max_length=50, blank=True, null=True)
    make = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    trim = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    mpg = models.IntegerField(blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    country_of_assembly = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "vehicle"


class VehicleHistory(models.Model):
    history_id = models.AutoField(primary_key=True, blank=False, null=False)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)
    history_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    history_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "vehicle_history"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    license_number = models.CharField(max_length=10, blank=True, null=True)
    license_state = models.CharField(max_length=20, blank=True, null=True)
    insurance_provider = models.CharField(max_length=20, blank=True, null=True)
    policy_number = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "customer"


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    job_title = models.CharField(max_length=20, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    benefits = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "employee"


class VehicleTransaction(models.Model):
    vehicle_transaction_id = models.AutoField(primary_key=True, blank=False, null=False)
    employee = models.ForeignKey(Employee, models.DO_NOTHING)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING)
    transaction_type = models.CharField(max_length=20, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "vehicle_transaction"







