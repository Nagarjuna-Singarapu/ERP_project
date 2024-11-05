from django import forms
from .models import Employment, PartySkill, PayGrade, SalaryStepGrade

class EmploymentForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = ['internal_organization', 'employment_id', 'from_date', 'amount', 
                  'comments', 'pay_grade_id', 'manual_pay_grade', 
                  'salary_step_sequence_id', 'manual_salary_step', 'period_type_id']

    def clean(self):
        cleaned_data = super().clean()
        pay_grade_id = cleaned_data.get('pay_grade_id')
        manual_pay_grade = cleaned_data.get('manual_pay_grade')
        salary_step_sequence_id = cleaned_data.get('salary_step_sequence_id')
        manual_salary_step = cleaned_data.get('manual_salary_step')

        # Ensure that either the foreign key or manual entry is filled
        if not pay_grade_id and not manual_pay_grade:
            raise forms.ValidationError("You must provide either a Pay Grade or a Manual Pay Grade.")

        if not salary_step_sequence_id and not manual_salary_step:
            raise forms.ValidationError("You must provide either a Salary Step Sequence or a Manual Salary Step.")

class PartySkillForm(forms.ModelForm):
    class Meta:
        model = PartySkill
        fields = ['hr_employee', 'skill_type', 'years_of_experience', 'rating', 'skill_level', 'description']

