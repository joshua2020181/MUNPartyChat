from django.contrib import admin

# Register your models here.

from .models import Country, Committee, Conference

admin.site.register(Country)
admin.site.register(Committee)
admin.site.register(Conference)