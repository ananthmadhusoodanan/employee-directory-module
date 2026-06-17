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
path(
    "dashboard/",
    views.dashboard,
    name="dashboard"
),

path(
    "apply-leave/",
    views.apply_leave,
    name="apply_leave"
),

path(
    "my-leaves/",
    views.my_leaves,
    name="my_leaves"
),
path(
    "hr-dashboard/",
    views.hr_dashboard,
    name="hr_dashboard"
),

path(
    "approve-leave/<int:pk>/",
    views.approve_leave,
    name="approve_leave"
),

path(
    "reject-leave/<int:pk>/",
    views.reject_leave,
    name="reject_leave"
),
]