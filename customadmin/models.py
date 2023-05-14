from django.db import models
from django.core.exceptions import ValidationError

class Signup(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    cpassword=models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=200)
    address=models.CharField(max_length=400)

def clean_password(self):
    password=self.cleaned_data.get('password')
    if len(password) < 8:
        raise ValidationError('password must be atleast 8 characters')
    return password
# class Booknow(models.Model):
#     username=models.CharField(max_length=200)
#     email=models.CharField(max_length=200)
#     password=models.CharField(max_length=200)
#     cpassword=models.CharField(max_length=200)
#     phonenumber=models.CharField(max_length=200)
#     address=models.CharField(max_length=400)
#     room=models.CharField(max_length=400)
#     checkindate=models.CharField(max_length=400)
#     checkoutdate=models.CharField(max_length=400)
#     No_of_people=models.IntegerField()

