# CRM_APP/hr/models.py
from django.db import models

class HR_Company(models.Model):
    name = models.CharField(max_length=255)

class HR_Department(models.Model):
    company = models.ForeignKey(HR_Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

###################### Global HR Section #################################
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
    
class PositionType(models.Model):
    # Fields for the PositionType model

    name = models.CharField(max_length=100, unique=True)
    parent_type = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_positions'
    )
    has_table = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Position Type"
        verbose_name_plural = "Position Types"

class LeaveReason(models.Model):
    leave_reason = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.leave_reason

class LeaveType(models.Model):
    leave_type = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.leave_type
    
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
    
    salary_step_sequence_id = models.ForeignKey(SalaryStepGrade, on_delete=models.SET_NULL, blank=True, null=True)

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
    

class EmployeePosition(models.Model):
    employee = models.ForeignKey(HR_Employee, to_field='employee_id', on_delete=models.CASCADE, related_name="positions")
    status = models.CharField(max_length=50, null=True, blank=True)  # Allows null and empty values
    internal_organization = models.ForeignKey(HR_Department, on_delete=models.CASCADE, related_name="employee_positions", null=True, blank=True)
    budget_id = models.CharField(max_length=50, null=True, blank=True)
    budget_item_sequence_id = models.CharField(max_length=50, null=True, blank=True)
    employee_position_type = models.ForeignKey(PositionType, on_delete=models.CASCADE, related_name="positions", null=True, blank=True)
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    salary_flag = models.BooleanField(default=False, null=True, blank=True)
    tax_exempt_flag = models.BooleanField(default=False, null=True, blank=True)
    full_time_flag = models.BooleanField(default=False, null=True, blank=True)
    temporary_flag = models.BooleanField(default=False, null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_finish_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Position for {self.employee} in {self.internal_organization} - {self.status}"
    

class EmployeeQualification(models.Model):
    QUALIFICATION_TYPES = [
        ('BSC', 'Bachelor of Science'),
        ('B.Tech', 'Bachelor of Technology'),
        ('CERTIFICATION', 'Certification'),
        ('DEGREE', 'Degree'),
        ('MSC', 'Masters of Science'),
        ('MBA', 'Masters of Business Administration'),
        ('EXPERIENCE', 'Work Experience'),
    ]

    STATUS_CHOICES = [
        ('HR_DS_COMPLETE', 'Completed'),
        ('HR_DS_DEFERRED', 'Deferred'),
        ('HR_DS_INCOMPLETE', 'Incomplete'),
    ]

    VERIFICATION_CHOICES = [
        ('PQV_NOT_VERIFIED', 'Not verified'),
        ('PQV_VERIFIED', 'Verified'),
    ]

    qualification_desc = models.CharField(max_length=60)
    title = models.CharField(max_length=60)
    status_id = models.CharField(max_length=20, choices=STATUS_CHOICES)
    verify_status_id = models.CharField(max_length=20, choices=VERIFICATION_CHOICES)
    through_date = models.DateField(null=True, blank=True)
    employee_id = models.ForeignKey(
        HR_Employee,
        to_field='employee_id',  # Link to employee_id field in HR_Employee
        on_delete=models.CASCADE,
        related_name="qualification"
    )
    party_qual_type_id = models.CharField(max_length=20, choices=QUALIFICATION_TYPES)
    from_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.qualification_desc}"
    
class EmployeeLeave(models.Model):
    STATUS_CHOICES = [
        ('Created', 'Created'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(HR_Employee, to_field='employee_id', on_delete=models.CASCADE, related_name="leaves")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    leave_reason = models.ForeignKey(LeaveReason, on_delete=models.SET_NULL, null=True)
    from_date = models.DateField()
    through_date = models.DateField(null=True, blank=True)
    approver = models.ForeignKey(HR_Employee, on_delete=models.SET_NULL, to_field='employee_id', null=True, related_name="approved_leaves")
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Created')  # New field with default status "Created"

    def __str__(self):
        return f"Leave for {self.employee.employee_id} from {self.from_date} to {self.through_date}, Status: {self.status}"

####################### Resume Section #######################################
    
class EmployeeResume(models.Model):
    resume_id = models.CharField(max_length=255)
    employee_id = models.ForeignKey(
        HR_Employee, 
        on_delete=models.CASCADE, 
        to_field='employee_id',  # Specify that the foreign key relates to the 'employee_id' field of HR_Employee
        related_name='party_resumes'
    )
    content_id = models.CharField(max_length=255)
    resume_date = models.DateField()

    def __str__(self):
        return self.resume_id

