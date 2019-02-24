from django import forms
from .models import Employee, Designation,Unit

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('name', 'birthdate','office', 'unit','department', 'designation')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['designation'].queryset = Designation.objects.none()
        self.fields['unit'].queryset = Unit.objects.none()


        if 'department' and 'office' in self.data:
            try:
                department_id = int(self.data.get('department'))
                office_id = int(self.data.get('office'))
                self.fields['designation'].queryset = Designation.objects.filter(department_id=department_id).order_by('name')
                self.fields['unit'].queryset = Unit.objects.filter(office_id=office_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Designation queryset
        elif self.instance.pk:
            self.fields['designation'].queryset = self.instance.department.designation_set.order_by('name')
            self.fields['unit'].queryset = self.instance.office.unit_set.order_by('name')
