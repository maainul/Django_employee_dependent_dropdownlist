from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Employee, Designation
from .forms import EmployeeForm


class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employee'


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_changelist')


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_changelist')


def load_designations(request):
    department_id = request.GET.get('department')
    designations = Designation.objects.filter(department_id=department_id).order_by('name')
    return render(request, 'employee/designation_dropdown_list_options.html', {'designations': designations})