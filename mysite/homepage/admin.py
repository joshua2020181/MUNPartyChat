from django.contrib import admin

# Register your models here.

from .models import Country, Committee, Conference, Chair

admin.site.register(Country)
admin.site.register(Committee)
admin.site.register(Conference)
admin.site.register(Chair)