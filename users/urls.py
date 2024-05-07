from django.urls import path
from . import views
from . views import UserRegistration

urlpatterns = [
    path('register/', UserRegistration.as_view() , name="register"),
    path('', UserRegistration.as_view(), name="users_list")
]