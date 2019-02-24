from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee_changelist'),
    path('add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_change'),
    path('ajax/load-designations/', views.load_designations, name='ajax_load_designations'),
    path('ajax/load-units/', views.load_units, name='ajax_load_units'), # <-- this one here
]
