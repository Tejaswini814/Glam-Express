from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Parlour(models.Model):
    parlour_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    image = models.ImageField(upload_to='parlour_images/')
    services = models.ManyToManyField('Service', related_name='parlours')  # NEW

    def __str__(self):
        return self.parlour_name


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parlour = models.ForeignKey(Parlour, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    user_location = models.CharField(max_length=255, help_text="Enter your address for home service")
    services = models.ManyToManyField(Service)
    is_approved = models.BooleanField(default=False)

    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} booked {self.parlour.parlour_name} on {self.booking_date} at {self.booking_time}"