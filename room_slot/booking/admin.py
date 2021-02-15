from django.contrib import admin
from .models import Apartment, BookingApartment

# Register your models here.
admin.site.register(Apartment)
admin.site.register(BookingApartment)
