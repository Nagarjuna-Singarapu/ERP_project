#ERP_project/crm_app/HRMS/views.py


from rest_framework import viewsets, status
import logging, json
from django.contrib import messages
from .utils import load_country_data
from django.shortcuts import get_object_or_404, redirect, render
from .models import HR_Employee, PerformanceReview, PayGrade,SalaryStepGrade, Employment, HR_Company, HR_Department, TerminationReason, TerminationType
# from .forms import EmploymentForm, PartySkillForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PartySkill
from .serializers import HREmployeeSerializer,PerformanceReviewSerializer, PayGradeSerializer, SalaryStepGradeSerializer,TerminationReasonSerializer, TerminationTypeSerializer

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

def performance(request):
    return render(request, 'hrms/emp_per/performance.html')

def EditPerformace(request):
    return render(request, 'hrms/emp_per/EditPerformace.html')



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

@xframe_options_exempt
def LookUpPerformace(request):
    return render(request, 'hrms/emp_per/LookUpPerformace.html')


    
# sunny
def employement_appli(request):
    return render(request, 'hrms/emp_res_lea/employement_appli.html')

def New_emp_app(request):
    return render(request, 'hrms/emp_res_lea/New_emp_app.html')

def resume(request):
    return render(request, 'hrms/emp_res_lea/resume.html')

def leave(request):
    return render(request, 'hrms/emp_res_lea/leave.html')

def New_resume(request):
    return render(request, 'hrms/emp_res_lea/New_resume.html')

def leave_approval(request):
    return render(request, 'hrms/emp_res_lea/leave_approval.html')

def add_emp_leave(request):
    return render(request, 'hrms/emp_res_lea/add_emp_leave.html')


@xframe_options_exempt
def lookup_emp_app(request):
    return render(request, 'hrms/emp_res_lea/lookup_emp_app.html')

@xframe_options_exempt
def lookup_emp_posi(request):
    return render(request, 'hrms/emp_res_lea/lookup_emp_posi.html')

@xframe_options_exempt
def lookup_party(request):
    return render(request, 'hrms/emp_res_lea/lookup_party.html')

@xframe_options_exempt
def lookup_party_resume(request):
    return render(request, 'hrms/emp_res_lea/lookup_party_resume.html')


# global HR by sunny and amit 
def skill_types(request):
    return render(request, 'hrms/global_hr/skill_types.html')

def responsibility_types(request):
    return render(request, 'hrms/global_hr/responsibility_types.html')

def termination_reasons(request):
    return render(request, 'hrms/global_hr/termination_reasons.html')

def termination_types(request):
    return render(request, 'hrms/global_hr/termination_types.html')

def position_types(request):
    return render(request, 'hrms/global_hr/position_types.html')

def emp_leave_types(request):
    return render(request, 'hrms/global_hr/emp_leave_types.html')

def pay_grades(request):
    return render(request, 'hrms/global_hr/pay_grades.html')

def job_interview_types(request):
    return render(request, 'hrms/global_hr/job_interview_types.html')

def tranning_class_types(request):
    return render(request, 'hrms/global_hr/tranning_class_types.html')

def public_holiday(request):
    return render(request, 'hrms/global_hr/public_holiday.html')

def EditPayGrade(request):
    return render(request, 'hrms/global_hr/EditPayGrade.html')

def EmpLeaveReasonType(request):
    return render(request, 'hrms/global_hr/EmpLeaveReasonType.html')

def emp_leave_types(request):
    return render(request, 'hrms/global_hr/emp_leave_types.html')

def Edit_PositionTypes(request):
    return render(request, 'hrms/global_hr/Edit_PositionTypes.html')


# gannu
def Skills(request):
    return render(request, 'hrms/skill_qual/Skills.html')

def Qualification(request):
    return render(request, 'hrms/skill_qual/Qualification.html')

def newparties(request):
    return render(request, 'hrms/skill_qual/newparties.html')

def newpartiesQualifivation(request):
    return render(request, 'hrms/skill_qual/newpartiesQualifivation.html')

def Recruitment(request):
    return render(request, 'hrms/skill_qual/Recruitment.html')

def JobRequision(request):
    return render(request, 'hrms/skill_qual/JobRequision.html')

def NewJobRequision(request):
    return render(request, 'hrms/skill_qual/NewJobRequision.html')

def Approvals(request):
    return render(request, 'hrms/skill_qual/Approvals.html')

def jobInterview(request):
    return render(request, 'hrms/skill_qual/jobInterview.html') 

def newInternalJobPosting(request):
    return render(request, 'hrms/skill_qual/newInternalJobPosting.html')

def NewjobInterview(request):
    return render(request, 'hrms/skill_qual/NewjobInterview.html')

def Relocation(request):
    return render(request, 'hrms/skill_qual/Relocation.html')



def TrainingCalender(request):
    return render(request, 'hrms/skill_qual/TrainingCalender.html')

def dayView(request):
    return render(request, 'hrms/skill_qual/dayView.html')

def monthView(request):
    return render(request, 'hrms/skill_qual/monthView.html')

def upcomingEvent(request):
    return render(request, 'hrms/skill_qual/upcomingEvent.html')

def TrainingApproval(request):
    return render(request, 'hrms/skill_qual/TrainingApproval.html')

def weekView(request):
    return render(request, 'hrms/skill_qual/weekView.html')

def CalenderSection(request):
    return render(request, 'hrms/skill_qual/CalenderSection.html')

def addnewEventMonth(request):
    return render(request, 'hrms/skill_qual/addnewEventMonth.html')

def addnewEvent(request):
    return render(request, 'hrms/skill_qual/addnewEvent.html')



@xframe_options_exempt
def skill_lookupparty(request):
    return render(request, 'hrms/skill_qual/skill_lookupparty.html')

@xframe_options_exempt
def nagaslookup(request):
    return render(request, 'hrms/skill_qual/nagaslookup.html')




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
    
# class HREmployeeViewSet(viewsets.ModelViewSet):
#     queryset = HR_Employee.objects.all()
#     serializer_class = HREmployeeSerializer

#     def list(self, request, *args, **kwargs):
#         employee_id = request.query_params.get('employee_id', None)
#         email = request.query_params.get('email', None)

#         # Apply filters based on query parameters
#         if employee_id:
#             employees = self.queryset.filter(employee_id=employee_id)
#         elif email:
#             employees = self.queryset.filter(email=email)
#         else:
#             employees = self.queryset

#         if not employees.exists():
#             return Response({"detail": "No employee found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(employees, many=True)
#         return Response(serializer.data)


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer

    def list(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee_id', None)
        email = request.query_params.get('email', None)
        performance_review_id = request.query_params.get('performance_review_id', None)

        # Apply filters based on query parameters
        if performance_review_id:
            performance_reviews = self.queryset.filter(perf_review_id=performance_review_id)
        elif employee_id:
            performance_reviews = self.queryset.filter(hr_employee__employee_id=employee_id)
        elif email:
            performance_reviews = self.queryset.filter(hr_employee__email=email)
        else:
            performance_reviews = self.queryset

        if not performance_reviews.exists():
            return Response({"detail": "No performance review found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(performance_reviews, many=True)
        return Response(serializer.data)
    
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# View to create or update PartySkill record
def create_party_skill(request):
    if request.method == 'POST':
        # Get the form data
        party_id = request.POST.get('partyId')
        skill_type_id = request.POST.get('skillTypeId')
        years_experience = request.POST.get('yearsExperience')
        rating = request.POST.get('rating')
        skill_level = request.POST.get('skillLevel')
        description = request.POST.get('description')

        # Validate Party ID (HR_Employee) existence
        try:
            employee = HR_Employee.objects.get(employee_id=party_id)
        except HR_Employee.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Employee not found."}, status=400)
        
        # Validate Skill Type
        if skill_type_id not in dict(PartySkill.SKILL_TYPE_CHOICES).keys():
            return JsonResponse({"status": "error", "message": "Invalid skill type."}, status=400)

        # Create or update PartySkill record
        party_skill, created = PartySkill.objects.update_or_create(
            hr_employee=employee,
            skill_type=skill_type_id,
            defaults={
                'years_of_experience': years_experience,
                'rating': rating,
                'skill_level': skill_level,
                'description': description,
            }
        )

        if created:
            return JsonResponse({"status": "success", "message": "Skill created successfully!"})
        else:
            return JsonResponse({"status": "success", "message": "Skill updated successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

from django.shortcuts import render
from .models import PartySkill

def search_party_skills(request):
    skills = PartySkill.objects.all()

    # Retrieve the filtering parameters from the GET request
    party_id = request.GET.get('partyId', '')
    skill_type = request.GET.get('skillTypeId', '')
    years_experience = request.GET.get('yearsExperience', '')
    rating = request.GET.get('rating', '')
    skill_level = request.GET.get('skillLevel', '')

    # Build the query dynamically based on available parameters
    if party_id:
        skills = skills.filter(hr_employee__employee_id=party_id)
    
    if skill_type:
        skills = skills.filter(skill_type=skill_type)
    
    # Handle years of experience - perform an exact match
    if years_experience:
        try:
            years_experience = float(years_experience)  # Convert to float
            skills = skills.filter(years_of_experience=years_experience)  # Exact match
        except ValueError:
            pass  # If conversion fails, ignore the filter

    # Handle rating - perform an exact match, allow float values
    if rating:
        try:
            rating = float(rating)  # Convert to float
            skills = skills.filter(rating=rating)  # Exact match
        except ValueError:
            pass  # If conversion fails, ignore the filter

    # Handle skill level - case-insensitive match
    if skill_level:
        skills = skills.filter(skill_level__icontains=skill_level)

    print(f"Skills queryset: {skills}")
    
    # Pass filtered skills to the template
    return render(request, 'hrms/skill_qual/Skills.html', {'skills': skills})



def delete_skill(request, skill_id):
    skill = get_object_or_404(PartySkill, id=skill_id)

    if request.method == 'POST':
        skill.delete()
        return JsonResponse({'status': 'success', 'message': 'Skill deleted successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}
)



        
