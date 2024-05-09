from django.urls import path
from . import views
from . views import UserRegistration, UserLogin, ChangeUserPassword

urlpatterns = [
    path('register/', UserRegistration.as_view() , name="register"),
    path('', UserRegistration.as_view(), name="users_list"),
    path('login/', UserLogin.as_view(), name="login"),
    path('delete/<int:pk>/', UserRegistration.as_view(), name="delete"),
    path('update/<int:pk>/', UserRegistration.as_view(), name="update"),
    path('<int:pk>/changepassword/', ChangeUserPassword.as_view(), name="changepassword")
]