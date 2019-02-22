from django import forms
from .models import Employee, Designation

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'birthdate', 'department', 'designation')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['designation'].queryset = Designation.objects.filter(department_id=department_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Designation queryset
        elif self.instance.pk:
            self.fields['designation'].queryset = self.instance.department.designation_set.order_by('name')