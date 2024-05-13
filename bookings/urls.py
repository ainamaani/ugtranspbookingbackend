from django.urls import path
from . views import BookingView,SingleBookingView,handle_booking

urlpatterns = [
    path('add/', BookingView.as_view(), name='add_booking'),
    path('', BookingView.as_view(), name='bookings'),
    path('<int:pk>/delete/', BookingView.as_view(), name='delete_booking'),
    path('<int:pk>/update/', BookingView.as_view(), name='update_booking'),
    path('<int:pk>/', SingleBookingView.as_view(), name='single_booking'),
    path('book_bus/', handle_booking, name='book_bus')
]