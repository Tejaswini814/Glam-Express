from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse

# Create your views here.

def registerView(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1!=password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        elif User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email Already Exists'}, status=400)
        elif User.objects.filter(username=firstname+lastname).exists():
            return JsonResponse({'error': 'Change FirstName or LastName'}, status=400)
        else:
            user=User.objects.create_user(first_name=firstname,last_name=lastname,email=email,password=password1,username=email)
            user.save()
            return JsonResponse({'success': 'User Registered Successfully'}, status=200)
    return render(request,'service_app/register.html')

def loginView(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)

        user=authenticate(request,username=email,password=password)

        if user is not None:
            login(request,user)
            return JsonResponse({'success': 'Login Successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid Credentials'}, status=400)
    return render(request,'service_app/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

def indexView(request):
    query = request.POST.get('location')
    if query:
        parlours = Parlour.objects.filter(location__icontains=query)
    else:
        parlours = Parlour.objects.all()
    return render(request, 'service_app/index.html', {'parlours': parlours, 'query': query})

@login_required(login_url='login')
def parlour_detail(request, pk):
    parlour = get_object_or_404(Parlour, pk=pk)
    services = Service.objects.all()
    return render(request, 'service_app/details.html', {'parlour': parlour,'services': services})

@login_required(login_url='login')
def book_parlour(request):
    if request.method == 'POST':
        parlour_id = request.POST.get('parlour_id')
        booking_date = request.POST.get('date')
        booking_time = request.POST.get('time')
        location = request.POST.get('location')
        service_ids = request.POST.getlist('services')  # Handle multiple selected services

        if not (parlour_id and booking_date and booking_time and location and service_ids):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            parlour_id=parlour_id,
            booking_date=booking_date,
            booking_time=booking_time,
            user_location=location,
        )

        # Add selected services to the booking
        for service_id in service_ids:
            try:
                service = Service.objects.get(id=service_id)
                booking.services.add(service)
            except Service.DoesNotExist:
                continue  # Or log the issue

        review_url = reverse('review_booking', args=[booking.id])
        return JsonResponse({
            'status': 'success',
            'message': 'Booking successful!',
            'redirect_url': review_url
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('parlour').order_by('-booking_date', '-booking_time')
    today = timezone.now().date()
    return render(request, 'service_app/my_bookings.html', {'bookings': bookings,'today': today})

@login_required(login_url='login')
def profile_view(request):
    user = request.user
    return render(request, 'service_app/profile.html', {'user': user})

@login_required(login_url='login')
def review_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        review = request.POST.get('review')
        rating = request.POST.get('rating')

        if not review or not rating:
            return JsonResponse({'status': 'error', 'message': 'Review and rating required.'})

        booking.review = review
        booking.rating = int(rating)
        booking.save()
        return JsonResponse({'status': 'success', 'message': 'Thank you for your feedback!'})

    return render(request, 'service_app/review_booking.html', {'booking': booking})


def add_or_update_parlour(request, pk=None):
    parlour = get_object_or_404(Parlour, pk=pk) if pk else None
    services = Service.objects.all()

    if request.method == 'POST':
        name = request.POST.get('parlour_name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')
        selected_services = request.POST.getlist('services')

        if parlour:
            # Update existing
            parlour.parlour_name = name
            parlour.description = description
            parlour.location = location
            parlour.rating = rating
            if image:
                parlour.image = image
            parlour.save()
            parlour.services.set(selected_services)  # update services
        else:
            # Add new
            parlour = Parlour.objects.create(
                parlour_name=name,
                description=description,
                location=location,
                rating=rating,
                image=image,
            )
            parlour.services.set(selected_services)

        return redirect(f"{request.path}?success=1")

    return render(request, 'service_app/admin.html', {
        'parlour': parlour,
        'services': services,
    })