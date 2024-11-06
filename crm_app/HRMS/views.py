from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .utils import load_country_data
from django.shortcuts import get_object_or_404, redirect, render
from .models import HR_Employee, PayGrade,SalaryStepGrade, Employment, HR_Company, HR_Department, TerminationReason, TerminationType
from .forms import EmploymentForm
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import json, logging
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework import status
from .models import SkillType, PayGrade, SalaryStepGrade ,Responsibility_Type,TerminationReason
from .serializers import SkillTypeSerializer, PayGradeSerializer, SalaryStepGradeSerializer,TerminationReasonSerializer, TerminationTypeSerializer

logger=logging.getLogger(__name__)

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



##########   Skill Type ##########################################################

#View for fetching all stored skill types
@csrf_exempt
def get_skill_type(request):
    if request.method == 'GET':
          skill_types = SkillType.objects.all().values('skillTypeId', 'description')
          return JsonResponse(list(skill_types), safe=False)


#View for adding  skill types
@csrf_exempt
def skill_type(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            skill_type_id = data.get('skillTypeId')
            description = data.get('description')

            # Validate received data
            if not skill_type_id or not description:
                return JsonResponse({'status': 'error', 'message': 'Missing skillTypeId or description'}, status=400)

            # Create and save the new skill type
            skill_type = SkillType(skillTypeId=skill_type_id, description=description)
            skill_type.save()

            return JsonResponse({'status': 'success', 'skillTypeId': skill_type.skillTypeId, 'description': skill_type.description})

        except json.JSONDecodeError:
            logger.error("Invalid JSON format received.")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error("Error creating skill type: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Failed to create skill type'}, status=500)

    elif request.method == 'DELETE':
        try:
            # Parse JSON data for DELETE request
            data = json.loads(request.body.decode('utf-8'))
            skill_type_id = data.get('skillTypeId')

            if not skill_type_id:
                return JsonResponse({'status': 'error', 'message': 'Missing skillTypeId'}, status=400)

            # Find and delete the skill type
            skill_type = SkillType.objects.get(skillTypeId=skill_type_id)
            skill_type.delete()

            return JsonResponse({'status': 'success', 'message': 'Skill type deleted successfully'})

        except SkillType.DoesNotExist:
            logger.error("Skill type with ID %s does not exist", skill_type_id)
            return JsonResponse({'status': 'error', 'message': 'Skill type not found'}, status=404)
        except Exception as e:
            logger.error("Error deleting skill type: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Failed to delete skill type'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


#View for fetching all stored Responsibility types
@csrf_exempt
def get_responsibility_type(request):
    if request.method == 'GET':
          responsibility_type = Responsibility_Type.objects.all().values('responsibilityTypeId', 'description')
          return JsonResponse(list(responsibility_type), safe=False)


#View for adding Responsibility types
@csrf_exempt
def responsibility_type(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            responsibility_type_id = data.get('responsibilityTypeId')
            description = data.get('description')

            responsibility_type = Responsibility_Type(
                responsibilityTypeId=responsibility_type_id,
                description=description
            )
            responsibility_type.save()

            return JsonResponse({
                'status': 'success',
                'responsibilityTypeId': responsibility_type.responsibilityTypeId,
                'description': responsibility_type.description
            })
        except Exception as e:
            logger.error("Error creating responsibility type: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Failed to create responsibility type'}, status=500)

    elif request.method == 'DELETE':
        data = json.loads(request.body)
        responsibility_type_id = data.get('responsibilityTypeId')

        try:
            responsibility_type = Responsibility_Type.objects.get(responsibilityTypeId=responsibility_type_id)
            responsibility_type.delete()
            return JsonResponse({'status': 'success', 'message': 'Responsibility type deleted successfully'})
        except Responsibility_Type.DoesNotExist:
            logger.error("Responsibility type with ID %s does not exist", responsibility_type_id)
            return JsonResponse({'status': 'error', 'message': 'Responsibility type not found'}, status=404)
        except Exception as e:
            logger.error("Error deleting responsibility type: %s", e)
            return JsonResponse({'status': 'error', 'message': 'Failed to delete responsibility type'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


#View for fetching all stored Termination Reasons 
@csrf_exempt
def get_termination_reason(request):
    if request.method == 'GET':
          reason = TerminationReason.objects.all().values('termination_reason', 'description')
          return JsonResponse(list(reason), safe=False)


#view for the Termination_Reason
@csrf_exempt
def termination_reason(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            termination_reason = data.get('termination_reason')
            description = data.get('description')

            # Create the termination reason object
            reason = TerminationReason(termination_reason=termination_reason, description=description)
            reason.save()

            return JsonResponse({'status': 'success', 'termination_reason': reason.termination_reason, 'description': reason.description})

        except IntegrityError:
            # Return an error response for duplicate ID
            return JsonResponse({'status': 'error', 'message': 'Termination Reason ID already exists. Please use a unique ID.'}, status=400)
        except Exception as e:
            # General error response
            return JsonResponse({'status': 'error', 'message': 'Failed to create termination reason'}, status=500)

    elif request.method == 'DELETE':
        data = json.loads(request.body)
        termination_reason = data.get('termination_reason')

        try:
            reason = TerminationReason.objects.get(termination_reason=termination_reason)
            reason.delete()
            return JsonResponse({'status': 'success', 'message': 'Termination reason deleted successfully'})
        except TerminationReason.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Termination reason not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to delete termination reason'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




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


def get_employee(request, employee_id):
    try:
        # Adjust the query to match the model's field names
        employee = Employment.objects.get(employment_id__employee_id=employee_id)
        
        data = {
            "success": True,
            "internal_organization": employee.internal_organization.name,
            "from_date": employee.from_date,
            "amount": employee.amount,
            "comments": employee.comments,
            "pay_grade": employee.pay_grade_id.grade_name if employee.pay_grade_id else employee.manual_pay_grade,
            "salary_step": employee.salary_step_sequence_id.step_name if employee.salary_step_sequence_id else employee.manual_salary_step,
            "period_type": employee.period_type_id,
        }
    except Employment.DoesNotExist:
        data = {"success": False}
    
    return JsonResponse(data)

def create_employment(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        internal_org_id = request.POST['internal_organization']
        from_date = request.POST['from_date']
        amount = request.POST['amount']
        comments = request.POST.get('comments', '')
        pay_grade_name = request.POST.get('pay_grade', '')
        salary_step_name = request.POST.get('salary_step', '')
        period_type = request.POST['period_type']

        # New fields for termination
        termination_type_name = request.POST.get('termination_type', '')  # Optional field
        termination_reason_name = request.POST.get('termination_reason', '')  # Optional field

        # Fetch the related instances
        employee = get_object_or_404(HR_Employee, employee_id=employee_id)
        internal_org = get_object_or_404(HR_Department, id=internal_org_id)
        pay_grade, _ = PayGrade.objects.get_or_create(grade_name=pay_grade_name)
        salary_step, _ = SalaryStepGrade.objects.get_or_create(step_name=salary_step_name)
        termination_type, _ = TerminationType.objects.get_or_create(termination_type=termination_type_name)
        termination_reason, _ = TerminationReason.objects.get_or_create(termination_reason=termination_reason_name)

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
                # Add new fields for termination
                'termination_type': termination_type,
                'termination_reason': termination_reason,
            }
        )

        return redirect('Employment')

    return render(request, 'hrms/emp_per/NewEmployment.html')



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