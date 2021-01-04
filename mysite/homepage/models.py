from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    full_name = models.CharField(max_length=150)
    abbr = models.CharField(max_length=10)
    delegate = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['abbr']
    
    def __str__(self):
        return self.abbr

class Chair(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Committee(models.Model):
    full_name = models.CharField(max_length=150)
    abbr = models.CharField(max_length=10)

    countries = models.ManyToManyField(Country)
    
    chairs = models.ManyToManyField(Chair)
    
    class Meta:
        ordering = ['abbr']

    def __str__(self):
        return self.abbr + ": with " + str(self.countries.all()) + " countries"

class Conference(models.Model):
    full_name = models.CharField(max_length=500)
    abbr = models.CharField(max_length=15)
    conf_id = models.CharField(max_length=20)

    committees = models.ManyToManyField(Committee)

    #def __init__():
    #    if len(self.conf_id) < 1:
    #        print("please define a conference id: ex: CISSMUN2021")

    class Meta:
        ordering = ['abbr']

    def __str__(self):
        return self.abbr + ": with " + str(self.committees.all()) + " committees"
