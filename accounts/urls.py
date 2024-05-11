from django.urls import path
from . views import AccountView, SingleAccountView

urlpatterns = [
    path('add/', AccountView.as_view(), name='add_account'),
    path('', AccountView.as_view(), name='accounts'),
    path('<int:pk>/delete/', AccountView.as_view(), name='delete_account'),
    path('<int:pk>/update/', AccountView.as_view(), name='update_account'),
    path('<int:pk>/', SingleAccountView.as_view(), name='single_account')
]