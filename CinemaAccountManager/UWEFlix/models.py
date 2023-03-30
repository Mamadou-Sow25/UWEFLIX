
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# Club models
class ClubRepresentative(models.Model):
    clubRepNumber = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=300)
    lastName = models.CharField(max_length=300)
    dateOfBirth = models.DateField(validators=[MaxValueValidator(datetime.date.today)])
    clubRepPassword = models.CharField(max_length=300)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(max_length=30)
    representative = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.clubRepNumber)


class Club(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    representative = models.ForeignKey(ClubRepresentative, on_delete=models.PROTECT)
    address = models.CharField(max_length=300)
    landline = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)
    def __str__(self):
        return str(self.name)
    


    

# Cinema models
class Screens(models.Model):
    number = models.PositiveIntegerField() 
    capacity = models.PositiveIntegerField() 
    def __str__(self):
        return str(self.number)


class Film(models.Model):
    title = models.CharField(max_length=300)
    #rating = models.IntegerField(max_length=1)
    duration = models.PositiveIntegerField()
    short_description = models.CharField(max_length=300)
    long_description = models.CharField(max_length=300)
    image_URL = models.URLField()
    #trailer_url = models.URLField()
    upload_date = models.DateTimeField("date logged")
    def __str__(self):
        return self.title
        

class Showing(models.Model):
    date = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    time = models.TimeField()
    film = models.ForeignKey(Film, on_delete=models.PROTECT)
    screen = models.ForeignKey(Screens, on_delete=models.PROTECT)
    taken_tickets = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.film)+" "+str(self.date)+" "+str(self.time)

# Customer models

class Customer(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    card_number = models.IntegerField()
    expiry_date = models.DateField(validators=[MinValueValidator(datetime.date.today)])

