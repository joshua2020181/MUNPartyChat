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

    countries = models.ManyToManyField(Country, blank=True)
    
    chairs = models.ManyToManyField(Chair, blank=True)
    
    class Meta:
        ordering = ['abbr']

    def __str__(self):
        return self.abbr + ": with " + str(self.countries.all()) + " countries"

class Conference(models.Model):
    full_name = models.CharField(max_length=500)
    abbr = models.CharField(max_length=15)
    conf_id = models.CharField(max_length=20)

    committees = models.ManyToManyField(Committee, blank=True)

    def file_path(instance, filename):
        return instance.conf_id + '/logo/' + filename
    
    logo = models.ImageField(upload_to=file_path, null=True, blank=True)

    class Meta:
        ordering = ['abbr']

    def __str__(self):
        return self.abbr + ": with " + str(self.committees.all()) + " committees"
