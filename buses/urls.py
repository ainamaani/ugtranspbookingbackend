from django.urls import path
from . views import BusView,SingleBusView

urlpatterns = [
    path('add/', BusView.as_view(), name='add_bus'),
    path('', BusView.as_view(), name='buses'),
    path('<int:pk>/delete/', BusView.as_view(), name='delete_bus'),
    path('<int:pk>/update/', BusView.as_view(), name='update_bus'),
    path('<int:pk>/', SingleBusView.as_view(), name='single_bus')
]