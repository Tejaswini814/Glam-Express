from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([Parlour,Booking,Service])