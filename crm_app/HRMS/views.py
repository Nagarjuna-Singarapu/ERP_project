
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import logging
import re
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib import messages
from django.urls import reverse
from .utils import load_country_data
from django.shortcuts import get_object_or_404, redirect, render
from .models import EmployeeLeave, EmployeePosition, EmployeeQualification, HR_Employee, LeaveReason, LeaveType, PayGrade, PositionType,SalaryStepGrade, Employment, HR_Company, HR_Department, TerminationReason, TerminationType
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

from .models import PayGrade, SalaryStepGrade
from .serializers import LeaveReasonSerializer, LeaveTypeSerializer, PayGradeSerializer, PositionTypeSerializer, SalaryStepGradeSerializer,TerminationReasonSerializer, TerminationTypeSerializer


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

logger = logging.getLogger(__name__)

def employment_search(request):
    if request.method == 'POST':
        # Parse the JSON request body
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Extract search parameters
        employee_id = body.get('employee_id')
        termination_reason_name = body.get('termination_reason')  # The name, e.g., "Company Downsizing"
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        termination_type = body.get('termination_type')
        planned_start_date = body.get('from_date')  # Date in HR_Employee
        from_date = body.get('through_date')  # Date in Employment

        # Initialize querysets
        queryset = HR_Employee.objects.all()
        employment_queryset = Employment.objects.all()

        # Apply filters to HR_Employee
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if planned_start_date:
            queryset = queryset.filter(planned_start_date=planned_start_date)

        # Apply filters to Employment based on TerminationReason
        if termination_reason_name:
            try:
                termination_reason = TerminationReason.objects.get(termination_reason=termination_reason_name)
                employment_queryset = employment_queryset.filter(termination_reason=termination_reason)
            except TerminationReason.DoesNotExist:
                return JsonResponse({'error': 'Termination reason not found'}, status=404)

        # Additional Employment filters
        if termination_type:
            try:
                termination_type_obj = TerminationType.objects.get(termination_type=termination_type)
                employment_queryset = employment_queryset.filter(termination_type=termination_type_obj)
            except TerminationType.DoesNotExist:
                return JsonResponse({'error': 'Termination type not found'}, status=404)
        if from_date:
            employment_queryset = employment_queryset.filter(from_date=from_date)

        # Prepare response data
        results = []
        for employee in queryset:
            # Filter Employment records for each HR_Employee
            employment_records = employment_queryset.filter(employment_id=employee)
            logger.debug("Employment Records for Employee %s: %s", employee.employee_id, employment_records)

            for employment in employment_records:
                results.append({
                    'internal_organization': employment.internal_organization.name,
                    'employment_id': {
                        'employee_id': employee.employee_id,
                        'first_name': employee.first_name,
                        'last_name': employee.last_name,
                        'from_date': employee.planned_start_date,
                    },
                    'through_date': employment.from_date,
                    'termination_reason': str(employment.termination_reason),
                    'termination_type': str(employment.termination_type),
                })

        logger.debug("Results: %s", results)
        print(results)

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

from datetime import datetime

def create_employee_position(request):
    errors = {}
    
    if request.method == 'POST':
        # Retrieve and validate form data from POST request
        employee_id = request.POST.get('employee_id')
        status = request.POST.get('status')
        internal_organization_id = request.POST.get('internal_organization')
        budget_id = request.POST.get('budgetID')
        budget_item_sequence_id = request.POST.get('budgetItemSequenceID')
        employee_position_type_id = request.POST.get('employeePositionTypeID')

        # Validate employee_id
        if not employee_id:
            errors['employee_id'] = "Employee ID is required."
        else:
            try:
                employee = HR_Employee.objects.get(employee_id=employee_id)
            except HR_Employee.DoesNotExist:
                errors['employee_id'] = "Employee ID does not exist."

        # Validate internal_organization_id
        if not internal_organization_id:
            errors['internal_organization'] = "Internal Organization ID is required."
        else:
            try:
                internal_organization = HR_Department.objects.get(id=internal_organization_id)
            except HR_Department.DoesNotExist:
                errors['internal_organization'] = "Internal Organization ID does not exist."
            except ValueError:
                errors['internal_organization'] = "Invalid format for Internal Organization ID."

        # Validate employee_position_type_id
        if not employee_position_type_id:
            errors['employee_position_type'] = "Position Type ID is required."
        else:
            try:
                employee_position_type = PositionType.objects.get(id=employee_position_type_id)
            except PositionType.DoesNotExist:
                errors['employee_position_type'] = "Position Type ID does not exist."
            except ValueError:
                errors['employee_position_type'] = "Invalid format for Position Type ID."

        # Validate date fields and convert empty values to None
        date_format = "%Y-%m-%d"
        def parse_date(date_str, field_name):
            try:
                return datetime.strptime(date_str, date_format).date() if date_str else None
            except ValueError:
                errors[field_name] = f"Invalid date format for {field_name}. Expected YYYY-MM-DD."
                return None

        planned_start_date = parse_date(request.POST.get('plannedStartDate'), 'planned_start_date')
        planned_end_date = parse_date(request.POST.get('plannedEndDate'), 'planned_end_date')
        actual_start_date = parse_date(request.POST.get('actualStartDate'), 'actual_start_date')
        actual_finish_date = parse_date(request.POST.get('actualFinishDate'), 'actual_finish_date')

        # Validate date ranges
        if planned_start_date and planned_end_date and planned_start_date > planned_end_date:
            errors['planned_dates'] = "Planned Start Date must be before Planned End Date."
        if actual_start_date and actual_finish_date and actual_start_date > actual_finish_date:
            errors['actual_dates'] = "Actual Start Date must be before Actual Finish Date."

        # Validate flag fields
        def validate_flag(flag_value, field_name):
            if flag_value not in ['YES', 'NO', None]:
                errors[field_name] = f"{field_name} must be either 'YES' or 'NO'."
            return flag_value == 'YES'

        salary_flag = validate_flag(request.POST.get('salaryFlag'), 'salary_flag')
        tax_exempt_flag = validate_flag(request.POST.get('taxExemptFlag'), 'tax_exempt_flag')
        full_time_flag = validate_flag(request.POST.get('fullTimeFlag'), 'full_time_flag')
        temporary_flag = validate_flag(request.POST.get('temporaryFlag'), 'temporary_flag')

        # Validate budget_id and budget_item_sequence_id
        if budget_id and not budget_id.isdigit():
            errors['budget_id'] = "Budget ID must be a number."
        if budget_item_sequence_id and not budget_item_sequence_id.isdigit():
            errors['budget_item_sequence_id'] = "Budget Item Sequence ID must be a number."

        # If there are errors, render the form with error messages
        if errors:
            return render(request, 'hrms/emp_per/New_positions.html', {
                'errors': errors,
                'employee_id': employee_id,
            })

        # Proceed to create or update the EmployeePosition if no errors are found
        EmployeePosition.objects.update_or_create(
            employee=employee,
            defaults={
                'status': status,
                'internal_organization': internal_organization,
                'budget_id': budget_id,
                'budget_item_sequence_id': budget_item_sequence_id,
                'employee_position_type': employee_position_type,
                'planned_start_date': planned_start_date,
                'planned_end_date': planned_end_date,
                'salary_flag': salary_flag,
                'tax_exempt_flag': tax_exempt_flag,
                'full_time_flag': full_time_flag,
                'temporary_flag': temporary_flag,
                'actual_start_date': actual_start_date,
                'actual_finish_date': actual_finish_date
            }
        )

        # Redirect to a success page or back to the form
        return render(request, 'hrms/emp_per/New_positions.html', {'success': True})

    # Render the form with empty fields for a new instance or pre-filled data for update
    return render(request, 'hrms/emp_per/New_positions.html')



def get_employee_position(request):
    employee_id = request.GET.get('employee_id')
    try:
        employee_position = EmployeePosition.objects.get(employee__employee_id=employee_id)
        data = {
            'status': employee_position.status,
            'internal_organization': employee_position.internal_organization.id if employee_position.internal_organization else '',
            'budget_id': employee_position.budget_id,
            'budget_item_sequence_id': employee_position.budget_item_sequence_id,
            'employee_position_type': employee_position.employee_position_type.id if employee_position.employee_position_type else '',
            'planned_start_date': employee_position.planned_start_date,
            'planned_end_date': employee_position.planned_end_date,
            'salary_flag': employee_position.salary_flag,
            'tax_exempt_flag': employee_position.tax_exempt_flag,
            'full_time_flag': employee_position.full_time_flag,
            'temporary_flag': employee_position.temporary_flag,
            'actual_start_date': employee_position.actual_start_date,
            'actual_finish_date': employee_position.actual_finish_date,
        }
        return JsonResponse(data)
    except EmployeePosition.DoesNotExist:
        return JsonResponse({'error': 'Employee position data not found'}, status=404)
    


def employment_position_search(request):
    if request.method == 'POST':
        # Parse the JSON request body
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Extract search parameters
        employee_id = body.get('employee_id')
        employee_position_type = body.get('employee_position_type')
        status = body.get('status')
        budget_id = body.get('budget_id')
        budget_item_sequence_id = body.get('budget_item_sequence_id')
        salary_flag = body.get('salary_flag')
        tax_exempt_flag = body.get('tax_exempt_flag')
        full_time_flag = body.get('full_time_flag')
        temporary_flag = body.get('temporary_flag')
        actual_start_date = body.get('actual_start_date')
        actual_finish_date = body.get('actual_finish_date')

        # Initialize querysets
        queryset = HR_Employee.objects.all()
        position_queryset = EmployeePosition.objects.all()

        # Apply filters to HR_Employee
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        # Apply filters to EmployeePosition
        if employee_position_type:
            position_queryset = position_queryset.filter(employee_position_type=employee_position_type)
        if status:
            position_queryset = position_queryset.filter(status=status)
        if budget_id:
            position_queryset = position_queryset.filter(budget_id=budget_id)
        if budget_item_sequence_id:
            position_queryset = position_queryset.filter(budget_item_sequence_id=budget_item_sequence_id)
        if salary_flag:
            position_queryset = position_queryset.filter(salary_flag=salary_flag)
        if tax_exempt_flag:
            position_queryset = position_queryset.filter(tax_exempt_flag=tax_exempt_flag)
        if full_time_flag:
            position_queryset = position_queryset.filter(full_time_flag=full_time_flag)
        if temporary_flag:
            position_queryset = position_queryset.filter(temporary_flag=temporary_flag)
        if actual_start_date:
            position_queryset = position_queryset.filter(actual_start_date=actual_start_date)
        if actual_finish_date:
            position_queryset = position_queryset.filter(actual_finish_date=actual_finish_date)

        # Prepare response data
        results = []
        for employee in queryset:
            # Filter EmployeePosition records for each HR_Employee
            position_records = position_queryset.filter(employee=employee)
            logger.debug("Position Records for Employee %s: %s", employee.employee_id, position_records)

            for position in position_records:
                results.append({
                    'employee': position.employee.employee_id,  # Employee Position ID
                    'status_id': position.status,  # Directly access the status string
                    'budget_id': position.budget_id,
                    'budget_item_sequence_id': position.budget_item_sequence_id,
                    'employee_position_type_id': position.employee_position_type.id if position.employee_position_type else None,
                    'planned_start_date': position.planned_start_date,
                    'planned_end_date': position.planned_end_date,
                    'salary_flag': position.salary_flag,
                    'tax_exempt_flag': position.tax_exempt_flag,
                    'full_time_flag': position.full_time_flag,
                    'temporary_flag': position.temporary_flag,
                    'actual_start_date': position.actual_start_date,
                    'actual_finish_date': position.actual_finish_date,
                })

        # logger.debug("Results: %s", results)
        # print(results)

        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def employment_position_data(request):
    # Fetch employment position data
    positions = EmployeePosition.objects.all().select_related('employee' , 'employee_position_type')  # Adjust as necessary

    # Prepare the data to be returned
    data = []
    for position in positions:
        data.append({
            'employee': position.employee.employee_id,  # Assuming you want employee_id from the employee model
            'status_id': position.status,
            'budget_id': position.budget_id,
            'budget_item_sequence_id': position.budget_item_sequence_id,
            'employee_position_type_id': position.employee_position_type.name if position.employee_position_type else None,
            'planned_start_date': position.planned_start_date,
            'planned_end_date': position.planned_end_date,
            'salary_flag': position.salary_flag,
            'tax_exempt_flag': position.tax_exempt_flag,
            'full_time_flag': position.full_time_flag,
            'temporary_flag': position.temporary_flag,
            'actual_start_date': position.actual_start_date,
            'actual_finish_date': position.actual_finish_date,
        })

    return JsonResponse(data, safe=False)


############################################################################################################################################

def create_employee_qualification(request):
    errors = {}  # Dictionary to store validation errors

    if request.method == 'POST':
        qualification_desc = request.POST.get('AddPartyQual_qualificationDesc')
        title = request.POST.get('title')
        status_id = request.POST.get('AddPartyQual_statusId')
        verify_status_id = request.POST.get('AddPartyQual_verifStatusId')
        through_date = request.POST.get('AddPartyQual_thruDate')
        employee_id_value = request.POST.get('employee_id')
        party_qual_type_id = request.POST.get('AddPartyQual_partyQualTypeId')
        from_date = request.POST.get('AddPartyQual_fromDate')

        # Validation for qualification description (cannot start with special characters)
        if qualification_desc and re.match(r'^[^a-zA-Z0-9]', qualification_desc):
            errors['qualification_desc'] = "Qualification description cannot start with a special character."

        # Validation for title (no special characters allowed)
        if title and re.search(r'[^a-zA-Z0-9 ]', title):
            errors['title'] = "Title should not contain special characters."

        # Validation for from_date and through_date (from_date < through_date)
        if from_date and through_date:
            try:
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
                through_date_obj = datetime.strptime(through_date, '%Y-%m-%d')
                if from_date_obj >= through_date_obj:
                    errors['date'] = "From date must be earlier than Through date."
            except ValueError:
                errors['date_format'] = "Dates must be in YYYY-MM-DD format."

        # Check if employee_id exists
        try:
            employee = HR_Employee.objects.get(employee_id=employee_id_value)
        except HR_Employee.DoesNotExist:
            errors['employee_id'] = "Employee ID does not exist."

        # If there are validation errors, render the form with errors
        if errors:
            return render(request, 'hrms/skill_qual/newpartiesQualifivation.html', {
                'errors': errors,
            })

        # If no errors, create or update EmployeeQualification
        qualification, created = EmployeeQualification.objects.update_or_create(
            employee_id=employee,
            defaults={
                'qualification_desc': qualification_desc,
                'title': title,
                'status_id': status_id,
                'verify_status_id': verify_status_id,
                'through_date': through_date if through_date else None,
                'party_qual_type_id': party_qual_type_id,
                'from_date': from_date if from_date else None,
            })

        return render(request, 'hrms/skill_qual/newpartiesQualifivation.html', {'success': True})
    return render(request, 'hrms/skill_qual/newpartiesQualifivation.html')


def employee_qualification_search(request):
    if request.method == 'POST':
        # Get the search parameters from the request body
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        employee_id = json_data.get('employee_id')
        qualification_desc = json_data.get('qualification_desc')
        title = json_data.get('title')
        status_ids = json_data.get('status_id', [])  # List of selected status ids
        verify_status_id = json_data.get('verify_status_id')
        from_date = json_data.get('from_date')
        through_date = json_data.get('through_date')
        party_qual_type_id = json_data.get('party_qual_type_id')

        # Build the query filters based on the provided parameters
        filters = {}

        if employee_id:
            filters['employee_id__employee_id'] = employee_id
        if qualification_desc:
            filters['qualification_desc__icontains'] = qualification_desc
        if title:
            filters['title__icontains'] = title
        if status_ids:
            filters['status_id__in'] = status_ids
        if verify_status_id:
            filters['verify_status_id'] = verify_status_id
        if from_date:
            filters['from_date__gte'] = from_date
        if through_date:
            filters['through_date__lte'] = through_date
        if party_qual_type_id:
            filters['party_qual_type_id'] = party_qual_type_id

        # Filter the EmployeeQualification records based on the filters
        qualifications = EmployeeQualification.objects.filter(**filters)

        # Prepare the response data
        response_data = []
        for qualification in qualifications:
            response_data.append({
                'employee_id': qualification.employee_id.employee_id,  # Assuming HR_Employee has employee_id
                'party_qual_type_id': dict(EmployeeQualification.QUALIFICATION_TYPES).get(qualification.party_qual_type_id, 'N/A'),
                'qualification_desc': qualification.qualification_desc,
                'title': qualification.title,
                'status_id': dict(EmployeeQualification.STATUS_CHOICES).get(qualification.status_id, 'N/A'),
                'verify_status_id': dict(EmployeeQualification.VERIFICATION_CHOICES).get(qualification.verify_status_id, 'N/A'),
                'from_date': qualification.from_date,
                'through_date': qualification.through_date,
            })

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def employee_qualification_data(request):
    # Fetch employee qualification data
    qualifications = EmployeeQualification.objects.all().select_related('employee_id')  # Only fetch related 'employee_id'

    # Prepare the data to be returned
    data = []
    for qualification in qualifications:
        data.append({
            'employee_id': qualification.employee_id.employee_id,  # Assuming you want employee_id from the HR_Employee model
            'party_qual_type_id': dict(EmployeeQualification.QUALIFICATION_TYPES).get(qualification.party_qual_type_id, None),  # Convert party_qual_type_id to name
            'qualification_desc': qualification.qualification_desc,
            'title': qualification.title,
            'status_id': qualification.status_id,
            'verify_status_id': qualification.verify_status_id,
            'from_date': qualification.from_date,
            'through_date': qualification.through_date,
        })

    # Return the data as a JSON response
    return JsonResponse(data, safe=False)


@api_view(['DELETE'])
def delete_employee_qualification(request, employee_id):
    try:
        qualification = EmployeeQualification.objects.get(employee_id=employee_id)
        qualification.delete()
        return Response({'message': 'Qualification deleted successfully'}, status=200)
    except EmployeeQualification.DoesNotExist:
        return Response({'error': 'Qualification not found'}, status=404)

##############################################################################################################################################

def add_employee_leave(request):
    if request.method == 'POST':
        errors = {}
        employee_id = request.POST.get('employee_id')
        leave_type_id = request.POST.get('leaveTypeID')
        leave_reason_id = request.POST.get('leaveReasonType')
        from_date = request.POST.get('fromDate')
        through_date = request.POST.get('throughDate')
        approver_party_id = request.POST.get('approverParty')
        description = request.POST.get('description', '')

        # Validate required fields
        if not employee_id:
            errors['employee_id'] = 'Employee ID is required.'
        if not leave_type_id:
            errors['leaveTypeID'] = 'Leave Type ID is required.'
        if not leave_reason_id:
            errors['leaveReasonType'] = 'Leave Reason Type is required.'
        if not from_date:
            errors['fromDate'] = 'From Date is required.'
        if not approver_party_id:
            errors['approverParty'] = 'Approver Party is required.'

        # Validate date formats and that from_date is less than through_date
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            if through_date:
                through_date_obj = datetime.strptime(through_date, "%Y-%m-%d")
                if from_date_obj >= through_date_obj:
                    errors['date_range'] = 'From Date must be earlier than Through Date.'
        except ValueError:
            errors['date_format'] = 'Invalid date format. Please use YYYY-MM-DD.'

        # Validate existence of employee and approver in HR_Employee table
        try:
            employee = HR_Employee.objects.get(employee_id=employee_id)
        except HR_Employee.DoesNotExist:
            errors['employee_id'] = 'Employee with the provided ID does not exist.'

        try:
            approver_party = HR_Employee.objects.get(employee_id=approver_party_id)
        except HR_Employee.DoesNotExist:
            errors['approverParty'] = 'Approver with the provided ID does not exist.'

        # Validate leave type and reason IDs
        try:
            leave_type = LeaveType.objects.get(id=leave_type_id)
        except LeaveType.DoesNotExist:
            errors['leaveTypeID'] = 'Invalid Leave Type ID.'

        try:
            leave_reason = LeaveReason.objects.get(id=leave_reason_id)
        except LeaveReason.DoesNotExist:
            errors['leaveReasonType'] = 'Invalid Leave Reason Type.'
        
        if not re.match("^[a-zA-Z0-9\s]*$", description):
            errors['description'] = 'Description must contain only alphanumeric characters and spaces.'

        # If errors exist after validation, return them to the template
        if errors:
            return render(request, 'hrms/emp_res_lea/add_emp_leave.html', {'errors': errors})

        # Create the EmployeeLeave record if no errors
        employee_leave = EmployeeLeave.objects.create(
            employee=employee,
            leave_type=leave_type,
            leave_reason=leave_reason,
            from_date=from_date,
            through_date=through_date if through_date else None,
            approver=approver_party,
            description=description
        )

        return render(request, 'hrms/emp_res_lea/add_emp_leave.html', {'success': True})
    
    return render(request, 'hrms/emp_res_lea/add_emp_leave.html')

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
    
class PositionTypeList(APIView):
    def get(self, request):
        position_types = PositionType.objects.all()
        serializer = PositionTypeSerializer(position_types, many=True)
        return Response(serializer.data)

class LeaveTypeList(APIView):
    def get(self, request):
        leave_types = LeaveType.objects.all()
        serializer = LeaveTypeSerializer(leave_types, many=True)
        return Response(serializer.data)

class LeaveReasonList(APIView):
    def get(self, request):
        leave_reasons = LeaveReason.objects.all()
        serializer = LeaveReasonSerializer(leave_reasons, many=True)
        return Response(serializer.data)
    

