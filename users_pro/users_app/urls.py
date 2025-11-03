from django.urls import path
from . import views

urlpatterns = [
    path('get_users/', views.get_users),
    path('get_user/<int:id>/', views.get_user),
    path('reg_user/', views.reg_user),
    # path('update_user/<int:id>/', views.update_user),
    # path('delete_user/<int:id>/', views.delete_user),
]