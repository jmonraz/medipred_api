from django.db import models

# Create your models here.

class Address(models.Model):
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True)
    address_3 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class Patient(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=False)
    contact_email = models.EmailField(max_length=255, null=False)
    contact_phone = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(null=False)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    blood_group = models.CharField(max_length=10, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)