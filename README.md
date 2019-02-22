# Dependent Dropdownlist

# FIRST CREATE PROJECT

>>virtualenv -p python3 .

>>source bin/activate

>>pip install django

>>mkdir src

>>cd src

>>django-admin startproject myproject .

>>python manage.py startapp employee

>>python manage.py runserver


# 2.EDIT myproject/settings.py

```
INSTALLED_APPS = [
    'people.apps.PeopleConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'employee',
]
```

```

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
# models.py

```
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Designation(models.Model):
    department = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
 ```

# urls.py

```
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee_changelist'),
    path('add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_change'),
]
```
# views.py

```
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Employee

class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employee'

class EmployeeCreateView(CreateView):
    model = Employee
    fields = ('name', 'birthdate', 'department', 'designation')
    success_url = reverse_lazy('employee_changelist')

class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = ('name', 'birthdate', 'department', 'designation')
    success_url = reverse_lazy('employee_changelist')
```
# employee_form.html

```
{% extends 'base.html' %}

{% block content %}
  <h2>Employee Form</h2>
  <form method="post" novalidate>
    {% csrf_token %}
    <table>
      {{ form.as_table }}
    </table>
    <button type="submit">Save</button>
    <a href="{% url 'employee_changelist' %}">Nevermind</a>
  </form>
{% endblock %}
```
# forms.py

```
from django import forms
from .models import Employee, Designation

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'birthdate', 'department', 'designation')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.none()
```
# views.py

```
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

```
# views.py

```
def load_designations(request):
    department_id = request.GET.get('department')
    designations = Designation.objects.filter(department_id=department_id).order_by('name')
    return render(request, 'employee/designation_dropdown_list_options.html', {'designations': designations})
```
# templates/employee/designation_dropdown_list_options.html

```
<option value="">---------</option>
{% for designation in designations %}
<option value="{{ designation.pk }}">{{ designation.name }}</option>
{% endfor %}
```
# urls.py

```
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee_changelist'),
    path('add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_change'),

    path('ajax/load-designations/', views.load_designations, name='ajax_load_designations'),  # <-- this one here
]
```
# templates/employee_form.html

```
{% extends 'base.html' %}

{% block content %}

  <h2>Employee Form</h2>

  <form method="post" id="employeeForm" data-designations-url="{% url 'ajax_load_designations' %}" novalidate>
    {% csrf_token %}
    <table>
      {{ form.as_table }}
    </table>
    <button type="submit">Save</button>
    <a href="{% url 'employee_changelist' %}">Nevermind</a>
  </form>

  <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
  <script>
    $("#id_department").change(function () {
      var url = $("#employeeForm").attr("data-designations-url");  // get the url of the `load_designations` view
      var departmentId = $(this).val();  // get the selected department ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/employee/ajax/load-designations/)
        data: {
          'department': departmentId       // add the department id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_designations` view function
          $("#id_designation").html(data);  // replace the contents of the designation input with the data that came from the server
        }
      });

    });
  </script>

{% endblock %}
```
# forms.py

```
from django import forms
from .models import Employee, Designation

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'birthdate', 'department', 'designations')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designations'].queryset = Designation.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['designations'].queryset = Designation.objects.filter(department_id=department_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Designation queryset
        elif self.instance.pk:
            self.fields['designations'].queryset = self.instance.department.designation_set.order_by('name')
```
