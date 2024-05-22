from django.db import models
from django.contrib.auth.models import User  
from django.contrib import admin

# Create your models here.


INSURANCE_TYPE_CHOICES = [
    ('health', 'Health Insurance'),
    ('auto', 'Auto Insurance'),
    
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
]


class InsuranceData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect to the user who submitted the data
    name_convention = models.CharField(max_length=255, default="None")

    # Personal Information
    first_name = models.CharField(max_length=255, null=True)
    enc_first_name = models.BinaryField(null=True)

    last_name = models.CharField(max_length=255, null=True)
    enc_last_name = models.BinaryField(null=True)

    date_of_birth = models.DateField(null=True)
    enc_date_of_birth = models.BinaryField(null=True)

    address = models.CharField(max_length=255, null=True)
    enc_address = models.BinaryField(null=True)

    city = models.CharField(max_length=255, null=True)
    enc_city = models.BinaryField(null=True)
    
    state = models.CharField(max_length=255, null=True)
    enc_state = models.BinaryField(null=True)
    
    zip_code = models.IntegerField(null=True)
    enc_zip_code = models.BinaryField(null=True)
    
    phone_number = models.IntegerField(null=True)
    enc_phone_number = models.BinaryField(null=True)

    email = models.EmailField(null=True)
    enc_email = models.BinaryField(null=True)

    # Insurance Information

    
    gender = models.CharField(choices=GENDER_CHOICES, max_length=25, null=True)
    enc_gender = models.BinaryField(null=True)

    height = models.IntegerField(null=True)
    enc_height = models.BinaryField(null=True)

    weight = models.IntegerField(null=True)
    enc_weight = models.BinaryField(null=True)

    dl_no = models.CharField(null=True, max_length=16)
    enc_dl_no = models.BinaryField(null=True)

    license_plate = models.CharField(null=True, max_length=11)
    enc_license_plate = models.BinaryField(null=True)




    insurance_type = models.CharField(choices=INSURANCE_TYPE_CHOICES, max_length=255, null=True)
    enc_insurance_type = models.BinaryField(null=True)

    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    enc_coverage_amount = models.BinaryField(null=True)

    start_date = models.DateField(null=True)
    enc_start_date = models.BinaryField(null=True)
    
    end_date = models.DateField(blank=True, null=True)  # Allow for policies with no end date
    enc_end_date = models.BinaryField(null=True)

    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return f"{self.user.username} - {self.name_convention}"
    

    