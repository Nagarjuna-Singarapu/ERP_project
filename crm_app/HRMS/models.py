# CRM_APP/hr/models.py
from django.db import models

class HR_Company(models.Model):
    name = models.CharField(max_length=255)

class HR_Department(models.Model):
    company = models.ForeignKey(HR_Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

######################By Amit #################################
#Add SkillType Model...
class SkillType(models.Model):
    skillTypeId = models.CharField(max_length=100,unique=True, blank=True, null=True)  # Assuming you want to store an ID
    description = models.CharField(max_length=255)  # Description field

    def __str__(self):
        return self.description

#Responsibility Type Model...
class Responsibility_Type(models.Model):
    responsibilityTypeId = models.CharField(max_length=100,unique=True, blank=True, null=True)  # Assuming you want to store an ID
    description = models.CharField(max_length=255)  # Description field

    def __str__(self):
        return self.description

class PayGrade(models.Model):
    grade_name = models.CharField(max_length=50)

    def __str__(self):
        return self.grade_name

class SalaryStepGrade(models.Model):
    step_name = models.CharField(max_length=50)

    def __str__(self):
        return self.step_name
    
class TerminationType(models.Model):
    termination_type = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.termination_type

#Termination Reason Model...
class TerminationReason(models.Model):
    termination_reason = models.CharField(max_length=100, unique=True,blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.termination_reason
    
###################################################################################################################################


class HR_Employee(models.Model):
    title = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    internal_organization = models.ForeignKey(HR_Department, on_delete=models.CASCADE)
    planned_start_date = models.DateField(blank=True, null=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    employee_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
    

class Employment(models.Model):
    internal_organization = models.ForeignKey(HR_Department, on_delete=models.CASCADE)
    employment_id = models.ForeignKey(HR_Employee, to_field='employee_id', on_delete=models.CASCADE)
    from_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(blank=True, null=True)
    
    # Allowing foreign key to PayGrade but also enabling manual entry if needed
    pay_grade_id = models.ForeignKey(PayGrade, on_delete=models.SET_NULL, blank=True, null=True)
    manual_pay_grade = models.CharField(max_length=50, blank=True, null=True)
    
    salary_step_sequence_id = models.ForeignKey(SalaryStepGrade, on_delete=models.SET_NULL, blank=True, null=True)
    manual_salary_step = models.CharField(max_length=50, blank=True, null=True)

    # Period type with predefined choices
    PERIOD_TYPE_CHOICES = [
        ('FISCAL_BIWEEK', 'Fiscal Bi-Week'),
        ('FISCAL_MONTH', 'Fiscal Month'),
        ('FISCAL_QUARTER', 'Fiscal Quarter'),
        ('FISCAL_WEEK', 'Fiscal Week'),
        ('FISCAL_YEAR', 'Fiscal Year'),
        ('RATE_HOUR', 'Rate amount per Hour'),
        ('RATE_QUARTER', 'Rate amount per Quarter'),
        ('RATE_WEEK', 'Rate amount per Week'),
        ('RATE_MONTH', 'Rate amount per Month'),
        ('SALES_MONTH', 'Sales Month'),
        ('SALES_QUARTER', 'Sales Quarter'),
    ]
    period_type_id = models.CharField(max_length=50, choices=PERIOD_TYPE_CHOICES)

    termination_type = models.ForeignKey(
        TerminationType, on_delete=models.SET_NULL, blank=True, null=True
    )
    termination_reason = models.ForeignKey(
        TerminationReason, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"Employment of {self.employment_id} in {self.internal_organization} from {self.from_date}"
