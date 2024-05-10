from django.urls import path
from . import views
from . views import UserRegistration, UserLogin, ChangeUserPassword, HandlePasswordResetCode, HandleResetForgotPassword

urlpatterns = [
    path('register/', UserRegistration.as_view() , name="register"),
    path('', UserRegistration.as_view(), name="users_list"),
    path('login/', UserLogin.as_view(), name="login"),
    path('delete/<int:pk>/', UserRegistration.as_view(), name="delete"),
    path('update/<int:pk>/', UserRegistration.as_view(), name="update"),
    path('<int:pk>/changepassword/', ChangeUserPassword.as_view(), name="change_password"),
    path('forgotpassword/', HandlePasswordResetCode.as_view(), name="forgot_password"),
    path('resetcodes/', HandlePasswordResetCode.as_view(), name="reset_codes"),
    path('resetpassword/', HandleResetForgotPassword.as_view(), name="reset_password")
    
]