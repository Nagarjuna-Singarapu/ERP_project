import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib import messages
from .utils import load_country_data
from django.shortcuts import get_object_or_404, redirect, render
from .models import HR_Employee, PayGrade,SalaryStepGrade, Employment, HR_Company, HR_Department, TerminationReason, TerminationType
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PayGrade, SalaryStepGrade
from .serializers import PayGradeSerializer, SalaryStepGradeSerializer,TerminationReasonSerializer, TerminationTypeSerializer

def NewEmploye(request):
    return render(request, 'hrms/emp_per/NewEmploye.html')

def get_departments(request):
    """Return a list of departments with their names and associated companies."""
    departments = HR_Department.objects.select_related('company').all()
    result = [
        {"id": dept.id, "name": dept.name, "company_name": dept.company.name}
        for dept in departments
    ]
    return JsonResponse(result, safe=False)

def get_countries(request):
    """Return a list of countries and their phone codes."""
    countries = load_country_data()
    result = [{"name": c["name"], "phonecode": c["phonecode"]} for c in countries]
    return JsonResponse(result, safe=False)

def get_states(request, country_name):
    """Return the list of states for the selected country."""
    countries = load_country_data()
    states = next((c["states"] for c in countries if c["name"] == country_name), [])
    return JsonResponse(states, safe=False)

def submit_employee(request):
    if request.method == 'POST':
        # Extract form data from POST request
        title = request.POST.get('title')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_initial = request.POST.get('middle_initial')
        gender = request.POST.get('gender')
        department_id = request.POST.get('internal_organization')
        internal_organization = get_object_or_404(HR_Department, id=department_id)
        planned_start_date = request.POST.get('planned_start_date')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        country = request.POST.get('country')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone_code = request.POST.get('phone_code')
        phone_number = request.POST.get('phone_number')
        employee_id = request.POST.get('employee_id')
        email = request.POST.get('email')

        # Save the data to the database
        HR_Employee.objects.create(
            title=title,
            first_name=first_name,
            middle_initial=middle_initial,
            last_name=last_name,
            gender=gender,
            internal_organization=internal_organization,
            planned_start_date=planned_start_date,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            phone_code=phone_code,
            phone_number=phone_number,
            employee_id=employee_id,
            email=email
        )

        # messages.success(request, "Employee created successfully!")
        # return redirect('success_page_url')
        # Redirect to a success page or return a success message
        return JsonResponse({"message": "Employee created successfully!"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
def check_email(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        exists = HR_Employee.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})

def check_employee_id(request):
    if request.method == 'GET':
        employee_id = request.GET.get('employee_id')
        exists = HR_Employee.objects.filter(employee_id=employee_id).exists()
        return JsonResponse({'exists': exists})
    
def search_employees(request):
    if request.method == 'GET':
        # Fetch search parameters from request
        employee_id = request.GET.get('employee_id')
        email = request.GET.get('email')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        phone_number = request.GET.get('phone_number')

        # Initialize queryset
        queryset = HR_Employee.objects.all()

        # Filter queryset based on available parameters
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if email:
            queryset = queryset.filter(email=email)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)

        # Prepare the response data
        results = [
            {
                'employee_id': emp.employee_id,
                'title': emp.title,
                'first_name': emp.first_name,
                'last_name': emp.last_name,
                'mobile': emp.phone_number,
            }
            for emp in queryset
        ]

        return JsonResponse(results, safe=False)
    

@xframe_options_exempt
def lookup(request):
    return render(request, 'hrms/emp_per/lookup.html')


def get_employee_data(request):
    employee_id = request.GET.get('employee_id')
    try:
        employee = Employment.objects.get(employment_id__employee_id=employee_id)
        data = {
            'internal_organization': employee.internal_organization.id,
            'from_date': employee.from_date,
            'amount': employee.amount,
            'comments': employee.comments,
            'pay_grade': employee.pay_grade_id.grade_name if employee.pay_grade_id else '',
            'salary_step': employee.salary_step_sequence_id.step_name if employee.salary_step_sequence_id else '',
            'period_type': employee.period_type_id,
            'termination_type': employee.termination_type.termination_type if employee.termination_type else '',
            'termination_reason': employee.termination_reason.termination_reason if employee.termination_reason else '',
        }
        return JsonResponse(data)
    except Employment.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

########################################################### Creating New Employment ###################################################

def create_employment(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        internal_org_id = request.POST['internal_organization']
        from_date = request.POST['from_date']
        amount = request.POST['amount']
        comments = request.POST.get('comments', '')
        pay_grade_id = request.POST.get('pay_grade', '')
        salary_step_id = request.POST.get('salary_step', '')
        period_type = request.POST['period_type']

        # New fields for termination
        termination_type_id = request.POST.get('termination_type', '')
        termination_reason_id = request.POST.get('termination_reason', '')

        # Fetch the related instances
        employee = get_object_or_404(HR_Employee, employee_id=employee_id)
        internal_org = get_object_or_404(HR_Department, id=internal_org_id)

        # Ensure that pay grade and salary step exist in the database
        try:
            pay_grade = PayGrade.objects.get(id=pay_grade_id)
        except PayGrade.DoesNotExist:
            return JsonResponse({'error': f'Invalid pay grade: {pay_grade_id}'}, status=400)

        try:
            salary_step = SalaryStepGrade.objects.get(id=salary_step_id)
        except SalaryStepGrade.DoesNotExist:
            return JsonResponse({'error': f'Invalid salary step: {salary_step_id}'}, status=400)

        # Optional fields for termination
        termination_type = None
        termination_reason = None
        if termination_type_id:
            termination_type = get_object_or_404(TerminationType, id=termination_type_id)
        if termination_reason_id:
            termination_reason = get_object_or_404(TerminationReason, id=termination_reason_id)

        # Create or update Employment record
        employment, created = Employment.objects.update_or_create(
            employment_id=employee,
            defaults={
                'internal_organization': internal_org,
                'from_date': from_date,
                'amount': amount,
                'comments': comments,
                'pay_grade_id': pay_grade,
                'salary_step_sequence_id': salary_step,
                'period_type_id': period_type,
                'termination_type': termination_type,
                'termination_reason': termination_reason,
            }
        )

        messages.success(request, 'Employment record created/updated successfully.')

        return redirect('Employment')

    return render(request, 'hrms/emp_per/NewEmployment.html')



################################################### Filterring Employment Data ##############################################################

def employment_search(request):
    if request.method == 'POST':
        # Parse the JSON body of the request
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Fetch search parameters from the request body
        employee_id = body.get('employee_id')
        email = body.get('email')
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        phone_number = body.get('phone_number')

        # Initialize queryset for HR_Employee
        queryset = HR_Employee.objects.all()

        # Filter queryset based on available parameters
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if email:
            queryset = queryset.filter(email=email)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)  # Case-insensitive contains
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)  # Case-insensitive contains
        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)

        # Prepare the response data
        results = []
        for employee in queryset:
            employment_records = Employment.objects.filter(employment_id__employee_id=employee.employee_id)
            for employment in employment_records:
                results.append({
                    'internal_organization': employment.internal_organization.name,  # Adjust to a field that returns a string
                    'employment_id': {
                        'employee_id': employee.employee_id,
                        'first_name': employee.first_name,
                        'last_name': employee.last_name,
                    },
                    'from_date': employee.planned_start_date,
                    'through_date': employment.from_date,
                    'termination_reason': str(employment.termination_reason),
                    'termination_type': str(employment.termination_type),
                })

        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def employment_data(request):
    if request.method == 'GET':
        results = []

        # Fetch all employees; you might want to apply filters if needed
        employees = HR_Employee.objects.all()
        # print(f"Total Employees: {employees.count()}")  # Debugging line

        for employee in employees:
            # Get all employment records for the current employee
            employment_records = Employment.objects.filter(employment_id__employee_id=employee.employee_id)

            # print(f"Employee ID: {employee.employee_id}, Employment Records Found: {employment_records.count()}")  # Debugging line
            
            for employment in employment_records:
                results.append({
                    'internal_organization': employment.internal_organization.name if employment.internal_organization else 'N/A',
                    'employment_id': {
                        'employee_id': employee.employee_id,  # Assuming employee_id is a field in HR_Employee
                        'first_name': employee.first_name,
                        'last_name': employee.last_name,
                    },
                    'from_date': employee.planned_start_date.strftime('%Y-%m-%d') if employee.planned_start_date else 'N/A',
                    'through_date': employment.from_date.strftime('%Y-%m-%d') if employment.from_date else 'N/A',
                    'termination_reason': str(employment.termination_reason) if employment.termination_reason else 'N/A',
                    'termination_type': str(employment.termination_type) if employment.termination_type else 'N/A',
                })

        # print(f"Results: {results}")  # Debugging line to check the final results
        return JsonResponse(results, safe=False)



##############################################################################################################################################


# anuj
def emp_main(request):
    return render(request, 'hrms/emp_per/emp_main.html')

def Employments(request):
    return render(request, 'hrms/emp_per/Employment.html')

def Employe_position(request):
    return render(request, 'hrms/emp_per/Employe_position.html')

def NewEmployement(request):
    return render(request, 'hrms/emp_per/NewEmployement.html')

def New_positions(request):
    return render(request, 'hrms/emp_per/New_positions.html')

@xframe_options_exempt
def lookup(request):
    return render(request, 'hrms/emp_per/lookup.html')

@xframe_options_exempt
def FindEmploye(request):
    return render(request, 'hrms/emp_per/FindEmploye.html')

@xframe_options_exempt
def Search_Emp_position(request):
    return render(request, 'hrms/emp_per/Search_Emp_position.html')

@xframe_options_exempt
def Paygrad(request):
    return render(request, 'hrms/emp_per/Paygrad.html')

@xframe_options_exempt
def EditSalary(request):
    return render(request, 'hrms/emp_per/EditSalary.html')


    
# sunny
def Employee_app(request):
    return render(request, 'hrms/emp_res_lea/Employee_app.html')

def New_emp_app(request):
    return render(request, 'hrms/emp_res_lea/New_emp_app.html')

def resume(request):
    return render(request, 'hrms/emp_res_lea/resume.html')

def leave(request):
    return render(request, 'hrms/emp_res_lea/leave.html')

def Newresume(request):
    return render(request, 'hrms/emp_res_lea/Newresume.html')

def leaveappr(request):
    return render(request, 'hrms/emp_res_lea/leaveappr.html')

def addempleave(request):
    return render(request, 'hrms/emp_res_lea/addempleave.html')


@xframe_options_exempt
def lookupempapp(request):
    return render(request, 'hrms/emp_res_lea/lookupempapp.html')

@xframe_options_exempt
def lookupempposi(request):
    return render(request, 'hrms/emp_res_lea/lookupempposi.html')

@xframe_options_exempt
def lookupparty(request):
    return render(request, 'hrms/emp_res_lea/lookupparty.html')

@xframe_options_exempt
def lookpartyresume(request):
    return render(request, 'hrms/emp_res_lea/lookpartyresume.html')


# gannu
def Skills(request):
    return render(request, 'hrms/skill_qual/Skills.html')

def Qualification(request):
    return render(request, 'hrms/skill_qual/Qualification.html')

def newparties(request):
    return render(request, 'hrms/skill_qual/newparties.html')

def newpartiesQualifivation(request):
    return render(request, 'hrms/skill_qual/newpartiesQualifivation.html')

@xframe_options_exempt
def skill_lookupparty(request):
    return render(request, 'hrms/skill_qual/skill_lookupparty.html')




class PayGradeList(APIView):
    def get(self, request):
        pay_grades = PayGrade.objects.all()
        serializer = PayGradeSerializer(pay_grades, many=True)
        return Response(serializer.data)

class SalaryStepList(APIView):
    def get(self, request):
        salary_steps = SalaryStepGrade.objects.all()
        serializer = SalaryStepGradeSerializer(salary_steps, many=True)
        return Response(serializer.data)
    
class TerminationTypeList(APIView):
    def get(self, request):
        pay_grades = TerminationType.objects.all()
        serializer = TerminationTypeSerializer(pay_grades, many=True)
        return Response(serializer.data)

class TerminationReasonList(APIView):
    def get(self, request):
        salary_steps = TerminationReason.objects.all()
        serializer = TerminationReasonSerializer(salary_steps, many=True)
        return Response(serializer.data)