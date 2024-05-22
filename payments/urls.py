from django.urls import path
from . views import PaymentView,SinglePaymentView

urlpatterns = [
    path('add/', PaymentView.as_view(), name='add_booking'),
    path('', PaymentView.as_view(), name='bookings'),
    path('<int:pk>/delete/', PaymentView.as_view(), name='delete_booking'),
    path('<int:pk>/update/', PaymentView.as_view(), name='update_booking'),
    path('<int:pk>/', SinglePaymentView.as_view(), name='single_booking'),
]