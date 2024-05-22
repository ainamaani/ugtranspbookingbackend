from django.urls import path
from . views import BusCompanyView,SingleBusCompanyView

urlpatterns = [
    path('add/', BusCompanyView.as_view(), name="add_company"),
    path('', BusCompanyView.as_view(), name="bus_companies"),
    path('<int:pk>/', SingleBusCompanyView.as_view(), name="single_company"),
    path('<int:pk>/update', BusCompanyView.as_view(), name="update_company_details"),
    path('<int:pk>/delete', BusCompanyView.as_view(), name="delete_company"),
    
]