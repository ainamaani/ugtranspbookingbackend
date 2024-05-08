from django.urls import path
from . import views
from . views import UserRegistration, UserLogin

urlpatterns = [
    path('register/', UserRegistration.as_view() , name="register"),
    path('', UserRegistration.as_view(), name="users_list"),
    path('login/', UserLogin.as_view(), name="login")
]