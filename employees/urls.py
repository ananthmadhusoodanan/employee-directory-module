from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='home'),

    path('login/', views.login_view, name='login'),

    path('register/', views.register_view, name='register'),

    path('logout/', views.logout_view, name='logout'),

    path('employees/', views.employee_list, name='employee_list'),

    path('add/', views.add_employee, name='add_employee'),

    path('<int:pk>/', views.employee_detail, name='employee_detail'),

    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),

    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),


    path(
    'logout/',
    views.logout_view,
    name='logout'
),

path(
    'download-csv/',
    views.download_csv,
    name='download_csv'
),
path(
    'import-csv/',
    views.import_csv,
    name='import_csv'
),
]