from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('', views.indexView, name='index'),
    path('parlour/<int:pk>/', views.parlour_detail, name='parlour_detail'),
    path('book_parlour/', views.book_parlour, name='book_parlour'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('profile/', views.profile_view, name='profile'),
    path('booking/<int:booking_id>/review/', views.review_booking, name='review_booking'),
    # Admin URLs
    path('adminpage/add/', views.add_or_update_parlour, name='add_parlour'),
]