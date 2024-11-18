
#ERP_project/crm_app/HRMS/views.py

from datetime import datetime
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from django.http import JsonResponse
# Standard Library Imports
import json
import logging
import re
from django.db.models import Prefetch
# Django Imports
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Q
from django.views.decorators.http import require_GET

# Django REST Framework Imports
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# Project Specific Imports - Models
from .models import (
    EmployeeLeave, EmployeePosition, EmployeeQualification, EmployeeResume, EmploymentApplication,
    HR_Employee, InternalJobPosting, JobInterview, JobInterviewType, JobRequisition, LeaveReason, LeaveType, PayGrade, PositionType, PublicHoliday, Responsibility_Type, SalaryStepGrade,
    Employment, HR_Company, HR_Department, SkillType, TerminationReason, TerminationType,
    PerformanceReview, PartySkill, TrainingAttendee, TrainingClass, TrainingClassType
)

# Project Specific Imports - Serializers
from .serializers import (
    JobInterviewTypeSerializer, PerformanceReviewSerializer, PayGradeSerializer, SalaryStepGradeSerializer,
    LeaveReasonSerializer, LeaveTypeSerializer, PositionTypeSerializer, SkillTypeSerializer,
    TerminationReasonSerializer, TerminationTypeSerializer, TrainingClassTypeSerializer
)

# Project Specific Utilities
from .utils import load_country_data
# Django Database Exceptions
from django.db import IntegrityError
# Logger
logger = logging.getLogger(__name__)
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
def skill_type(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            skill_type_id = data.get('skillTypeId')
            description = data.get('description')
            print(' ',skill_type_id)
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


# view for the Termination_Types
def create_termination_type(request):
    if request.method == "POST":
        termination_type = request.POST.get("termination_type", "").strip()
        description = request.POST.get("description", "").strip()

        # Validate description to contain only letters, numbers, and spaces
        if not description.replace(" ", "").isalnum():
            return JsonResponse({"success": False, "message": "Description should contain only letters, numbers, and spaces."})

        # Check for duplicate termination_type ID
        if TerminationType.objects.filter(termination_type=termination_type).exists():
            return JsonResponse({"success": False, "message": "This Termination Type ID already exists. Please enter a unique ID."})

        try:
            # Create new TerminationType entry
            TerminationType.objects.create(termination_type=termination_type, description=description)
            return JsonResponse({"success": True})
        except Exception as e:
            # Handle any other unexpected error
            return JsonResponse({"success": False, "message": str(e)})



def delete_termination_type(request):
    if request.method == "POST" and request.headers.get("X-HTTP-Method-Override") == "DELETE":
        termination_type_id = request.POST.get("termination_type", "").strip()
        try:
            TerminationType.objects.get(termination_type=termination_type_id).delete()
            return JsonResponse({"success": True})
        except TerminationType.DoesNotExist:
            return JsonResponse({"success": False, "message": "Termination Type not found."})

def list_termination_types(request):
    termination_types = list(TerminationType.objects.values("termination_type", "description"))
    return JsonResponse({"termination_types": termination_types})

# view for the Create LeaveType

def create_leave_type(request):
    if request.method == "POST":
        leave_type = request.POST.get("leave_type", "").strip()
        description = request.POST.get("description", "").strip()

        # Validate description to contain only letters, numbers, and spaces
        if not description.replace(" ", "").isalnum():
            return JsonResponse({"success": False, "message": "Description should contain only letters, numbers, and spaces."})

        # Check for duplicate leave_type ID
        if LeaveType.objects.filter(leave_type=leave_type).exists():
            return JsonResponse({"success": False, "message": "This Leave Type ID already exists. Please enter a unique ID."})

        try:
            # Create new LeaveType entry
            LeaveType.objects.create(leave_type=leave_type, description=description)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
        
#view for the delete LeaveType 

def delete_leave_type(request):
    if request.method == "POST" and request.headers.get("X-HTTP-Method-Override") == "DELETE":
        leave_type = request.POST.get("leave_type", "").strip()

        try:
            leave_type_instance = LeaveType.objects.get(leave_type=leave_type)
            leave_type_instance.delete()
            return JsonResponse({"success": True})
        except LeaveType.DoesNotExist:
            return JsonResponse({"success": False, "message": "Leave Type ID not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
        
#view for the show List LeaveType
def list_leave_types(request):
    leave_types = LeaveType.objects.all().values("leave_type", "description")
    return JsonResponse({"leave_types": list(leave_types)})


# View to get PayGrade data
def get_paygrade_data(request):
    pay_grades = PayGrade.objects.all().values('payGradeId', 'grade_name', 'comments')
    return JsonResponse(list(pay_grades), safe=False)

#view to search Grades data
def search_pay_grades(request):
    payGradeId = request.GET.get('payGradeId', '')
    grade_name= request.GET.get('grade_name', '')
    comments = request.GET.get('comments')

    # Filter based on the selected filters
    filters = {}
    if payGradeId:
        filters['payGradeId__icontains'] = payGradeId
    if grade_name:
        filters['grade_name__icontains'] = grade_name
    if comments:
        filters['comments__icontains'] = comments

    data = PayGrade.objects.filter(**filters).values('id', 'payGradeId', 'grade_name','comments')
    return JsonResponse(list(data), safe=False)

def create_paygrade(request):
    if request.method == 'POST':
        payGradeId = request.POST.get('payGradeId')
        grade_name = request.POST.get('grade_name')
        comments = request.POST.get('comments')

        # Backend validation
        errors = {}

        # Validate Pay Grade ID
        if not payGradeId:
            errors['payGradeId'] = 'Pay Grade ID is required.'
        elif not payGradeId.isalnum():
            errors['payGradeId'] = 'Pay Grade ID must be alphanumeric.'
        
        # Validate Pay Grade Name
        if not grade_name:
            errors['grade_name'] = 'Pay Grade Name is required.'
        elif not re.match(r'^[a-zA-Z0-9\s]+$', grade_name):
            errors['grade_name'] = 'Pay Grade Name must be alphanumeric.'

        # Validate Comments (if provided)
        if comments and not re.match(r'^[a-zA-Z\s]*$', comments):
            errors['comments'] = 'Comments should only contain alphabets.'

        # Check if Pay Grade ID already exists
        if PayGrade.objects.filter(payGradeId=payGradeId).exists():
            errors['payGradeId'] = 'Pay Grade ID already exists.'

        # Return errors if any
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Save to database
        try:
            pay_grade = PayGrade(
                payGradeId=payGradeId,
                grade_name=grade_name,
                comments=comments
            )
            pay_grade.save()
            return JsonResponse({'success': True, 'message': 'Pay Grade created successfully!'})
        except Exception as e:
            print(f"Error saving PayGrade: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Failed to save Pay Grade.'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

# View to delete a pay grade by ID
@csrf_protect
def delete_pay_grade(request, id):
    print("Triggerring")
    try:
        # Try to get the PayGrade object by ID
        pay_grade = PayGrade.objects.get(payGradeId=id)
        print('pay grade : {pay_grade}')
        pay_grade.delete()  # Delete the pay grade
        return JsonResponse({'message': 'Pay Grade deleted successfully'}, status=200)
    except PayGrade.DoesNotExist:
        # If the PayGrade with the given ID doesn't exist
        return JsonResponse({'message': 'Pay Grade not found'}, status=404)



#view for get list show Position Type 
def get_position_data(request):
    data = PositionType.objects.all().values('name','parent_type','has_table', 'description')
    return JsonResponse(list(data), safe=False)

#view to search Position Type data
def search_position_type(request):
    # Extract parameters from the GET request
    position_type = request.GET.get('positionType', '')
    parent_type = request.GET.get('parentType', '')
    has_table = request.GET.get('hasTable', '')
    description = request.GET.get('description', '')

    # Filter the PositionType based on the query parameters
    filters = {}
    if position_type:
        filters['name__icontains'] = position_type
    if parent_type:
        filters['parent_type__name__icontains'] = parent_type
    if has_table:
        filters['has_table'] = has_table.lower() == 'true'
    if description:
        filters['description__icontains'] = description

    # Fetch the filtered position types
    position_types = PositionType.objects.filter(**filters).values('id', 'name', 'parent_type__name', 'description')

    return JsonResponse(list(position_types), safe=False)

#create Position Type View 
def create_position(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        parent_type_id = request.POST.get('parent_type').strip()
        has_table = request.POST.get('has_table')
        description = request.POST.get('description').strip()

        # Backend validation for alphanumeric (A-Z, a-z, 0-9)
        if not re.match(r'^[a-zA-Z0-9]+$', name):
            return JsonResponse({'success': False, 'message': 'Position Type ID must be alphanumeric'}, status=400)
        
        if parent_type_id and not re.match(r'^[a-zA-Z0-9]+$', parent_type_id):
            return JsonResponse({'success': False, 'message': 'Parent Type ID must be alphanumeric'}, status=400)

        # Validate 'has_table' input
        if has_table not in ['Yes', 'No']:
            return JsonResponse({'success': False, 'message': 'Invalid value for Has Table'}, status=400)

        # Convert 'has_table' to Boolean
        has_table_value = True if has_table == 'Yes' else False

        # Check if parent type exists
        print(f"Parent Type ID entered: {parent_type_id}")
        print(f"Available Parent Types: {[p.name for p in PositionType.objects.all()]}")
        parent_type_obj = None
        if parent_type_id:
            try:
                parent_type_obj = PositionType.objects.get(name__iexact=parent_type_id)
            except PositionType.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Parent Type ID does not exist'}, status=404)

        # Create new Position Type
        try:
            position_type = PositionType.objects.create(
                name=name,
                parent_type=parent_type_obj,
                has_table=has_table_value,
                description=description
            )
            return JsonResponse({'success': True, 'message': 'Position Type created successfully'})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Position Type ID must be unique'}, status=400)

    return render(request, 'Edit_PositionTypes.html')


# View for delete to Position type by ID
@csrf_protect
def delete_position_type(request, name):
    print(f"Triggering delete for position type ID: {name}")
    
    if request.method == 'DELETE':
        try:
            # Make sure you are using the correct field, which should be `id` in this case
            position_type = PositionType.objects.get(name=name)
            position_type.delete()
            return JsonResponse({'message': 'Position type deleted successfully'}, status=200)
        except PositionType.DoesNotExist:
            return JsonResponse({'message': 'Position type not found'}, status=404)
        except Exception as e:
            print(f"Error deleting position type: {str(e)}")
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request'}, status=400)




# create Leave Reason Types
@csrf_protect
def create_leave_reason_type(request):
    if request.method == "POST":
        leave_reason = request.POST.get("leave_reason", "").strip()
        description = request.POST.get("description", "").strip()

        # Validate leave_reason to contain only alphanumeric characters
        if not leave_reason.isalnum():
            return JsonResponse({"success": False, "message": "Leave Reason ID should contain only alphanumeric characters."})

        # Validate description to contain only letters, numbers, and spaces
        if not description.replace(" ", "").isalnum():
            return JsonResponse({"success": False, "message": "Description should contain only letters, numbers, and spaces."})

        # Check for duplicate leave_reason ID
        if LeaveReason.objects.filter(leave_reason=leave_reason).exists():
            return JsonResponse({"success": False, "message": "This Leave Reason ID already exists. Please enter a unique ID."})

        try:
            LeaveReason.objects.create(leave_reason=leave_reason, description=description)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

# Delete Leave Reason Types
@csrf_protect
def delete_leave_reason_type(request):
    if request.method == "POST":
        leave_reason = request.POST.get("leave_reason", "").strip()

        try:
            leave_reason_instance = LeaveReason.objects.get(leave_reason=leave_reason)
            leave_reason_instance.delete()
            return JsonResponse({"success": True})
        except LeaveReason.DoesNotExist:
            return JsonResponse({"success": False, "message": "Leave Reason ID not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
# get List Leave Reason Types
@csrf_protect
def list_leave_reason_types(request):
    leave_reasons = LeaveReason.objects.all().values("leave_reason", "description")
    return JsonResponse({"leave_reasons": list(leave_reasons)})



#create JobInterviewType view 
@csrf_protect
def create_job_interview_type(request):
    if request.method == "POST":
        jobinterview_type = request.POST.get("jobinterviewTypeId", "").strip()
        description = request.POST.get("description", "").strip()

        # Validate jobinterview_type to contain only alphanumeric characters
        if not jobinterview_type.isalnum():
            return JsonResponse({"success": False, "message": "Job Interview Type ID should contain only alphanumeric characters."})

        # Validate description to contain only letters, numbers, and spaces
        if not description.replace(" ", "").isalnum():
            return JsonResponse({"success": False, "message": "Description should contain only letters, numbers, and spaces."})

        # Check for duplicate jobinterview_type ID
        if JobInterviewType.objects.filter(jobinterviewType=jobinterview_type).exists():
            return JsonResponse({"success": False, "message": "This Job Interview Type ID already exists. Please enter a unique ID."})

        try:
            JobInterviewType.objects.create(jobinterviewType=jobinterview_type, description=description)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

# Delete JobInterviewType view 
@csrf_protect
def delete_job_interview_type(request):
    if request.method == "POST":
        jobinterview_type = request.POST.get("jobinterviewTypeId", "").strip()

        try:
            jobinterview_instance = JobInterviewType.objects.get(jobinterviewType=jobinterview_type)
            jobinterview_instance.delete()
            return JsonResponse({"success": True})
        except JobInterviewType.DoesNotExist:
            return JsonResponse({"success": False, "message": "Job Interview Type ID not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
        
# get List Jobinterview Type View 
@csrf_protect
def list_job_interview_types(request):
    job_interviews = JobInterviewType.objects.all().values("jobinterviewType", "description")
    return JsonResponse({"job_interviews": list(job_interviews)})



#create Public Holiday View 
@csrf_protect
def create_public_holiday(request):
    if request.method == "POST":
        holiday_name = request.POST.get('holidayName', '').strip()
        description = request.POST.get('description', '').strip()
        from_date = request.POST.get('fromDate', '').strip()

        # Validation for holiday_name (Alphanumeric and spaces)
        if not re.match(r'^[a-zA-Z0-9\s]+$', holiday_name):
            return JsonResponse({"success": False, "message": "Holiday Name should be alphanumeric."})

        # Validation for description (Optional but must be alphanumeric and spaces if provided)
        if description and not re.match(r'^[a-zA-Z0-9\s]*$', description):
            return JsonResponse({"success": False, "message": "Description should contain only letters, numbers, and spaces."})

        # Validation for from_date
        try:
            datetime.strptime(from_date, '%Y-%m-%d')
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid date format."})

        # Check for unique holiday_name
        if PublicHoliday.objects.filter(holiday_name=holiday_name).exists():
            return JsonResponse({"success": False, "message": "Holiday Name already exists."})

        # Create a new Public Holiday
        PublicHoliday.objects.create(holiday_name=holiday_name, description=description, from_date=from_date)
        return JsonResponse({"success": True, "message": "Public Holiday added successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."})

#delete Public Holiday View 
@csrf_protect
def delete_public_holiday(request):
    if request.method == "POST":
        holiday_name = request.POST.get('holidayName', '').strip()

        # Delete the specified Public Holiday
        try:
            holiday = PublicHoliday.objects.get(holiday_name=holiday_name)
            holiday.delete()
            return JsonResponse({"success": True, "message": "Public Holiday deleted successfully."})
        except PublicHoliday.DoesNotExist:
            return JsonResponse({"success": False, "message": "Public Holiday not found."})

    return JsonResponse({"success": False, "message": "Invalid request method."})


#Get List Public Holiday View 
@csrf_protect
def list_public_holidays(request):
    if request.method == "GET":
        holidays = list(PublicHoliday.objects.values("holiday_name", "description", "from_date"))
        return JsonResponse({"success": True, "data": holidays})
    
    return JsonResponse({"success": False, "message": "Invalid request method."})

#create TrainingClassType view
@csrf_protect 
def create_training_class_type(request):
    if request.method == "POST":
        tranning_type_id = request.POST.get('tranningTypeId', '').strip()
        description = request.POST.get('description', '').strip()

        # Validation for tranningTypeId (Alphanumeric)
        if not re.match(r'^[a-zA-Z0-9]+$', tranning_type_id):
            return JsonResponse({"success": False, "message": "Training Class Type ID should be alphanumeric."})

        # Validation for description (Letters, numbers, and spaces only)
        if description and not re.match(r'^[a-zA-Z0-9\s]*$', description):
            return JsonResponse({"success": False, "message": "Description should contain only letters, numbers, and spaces."})

        # Check for unique tranningTypeId
        if TrainingClassType.objects.filter(tranningTypeId=tranning_type_id).exists():
            return JsonResponse({"success": False, "message": "Training Class Type ID already exists."})

        # Create a new Training Class Type
        TrainingClassType.objects.create(tranningTypeId=tranning_type_id, description=description)
        return JsonResponse({"success": True, "message": "Training Class Type added successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."})

#delete TrainingClassType view
@csrf_protect
def delete_training_class_type(request):
    if request.method == "POST":
        tranning_type_id = request.POST.get('tranningTypeId', '').strip()

        # Delete the specified Training Class Type
        try:
            training_class = TrainingClassType.objects.get(tranningTypeId=tranning_type_id)
            training_class.delete()
            return JsonResponse({"success": True, "message": "Training Class Type deleted successfully."})
        except TrainingClassType.DoesNotExist:
            return JsonResponse({"success": False, "message": "Training Class Type not found."})

    return JsonResponse({"success": False, "message": "Invalid request method."})


# Get list of Training class View 
@csrf_protect
def list_training_class_types(request):
    if request.method == "GET":
        # Fetch all Training Class Types
        training_classes = list(TrainingClassType.objects.values("tranningTypeId", "description"))
        return JsonResponse({"success": True, "data": training_classes})

    return JsonResponse({"success": False, "message": "Invalid request method."}) 
        

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

        import re

        errors = {}

        # Title validation (if required)
        if not title:
            errors['title'] = "Title is required."

        # First Name validation: Should contain only alphabets, no special characters or numbers
        if not first_name:
            errors['first_name'] = "First Name is required."
        elif not re.match(r'^[A-Za-z]+$', first_name):
            errors['first_name'] = "First Name should contain only alphabets."

        # Middle Initial validation: Should contain only alphabets, no special characters or numbers
        if middle_initial and not re.match(r'^[A-Za-z]*$', middle_initial):
            errors['middle_initial'] = "Middle Initial should contain only alphabets."

        # Last Name validation: Should contain only alphabets, no special characters or numbers
        if not last_name:
            errors['last_name'] = "Last Name is required."
        elif not re.match(r'^[A-Za-z]+$', last_name):
            errors['last_name'] = "Last Name should contain only alphabets."

        # City validation: Should contain only alphabets, no special characters or numbers
        if not city:
            errors['city'] = "City is required."
        elif not re.match(r'^[A-Za-z\s]+$', city):
            errors['city'] = "City should contain only letters and spaces."

        # Phone Number validation: Should contain exactly 10 digits, no alphabets or special characters
        if not phone_number:
            errors['phone_number'] = "Phone Number is required."
        elif not re.match(r'^\d{10}$', phone_number):
            errors['phone_number'] = "Phone Number should be exactly 10 digits."

        # Zip/Postal Code validation: Should contain only numbers, no alphabets or special characters
        if not zip_code:
            errors['zip_code'] = "Zip Code is required."
        elif not re.match(r'^\d+$', zip_code):
            errors['zip_code'] = "Zip Code should contain only numbers."

        # Address1 validation: Should not contain only special characters, but can include letters, numbers, ',' '-' '/'
        if not address1:
            errors['address1'] = "Address1 is required."
        elif not re.match(r'^[A-Za-z0-9\s,/-]+$', address1) or re.match(r'^[,/-]+$', address1):
            errors['address1'] = "Address1 should contain letters, numbers, or ',', '-', '/'."

        # Address2 validation: Should not contain only special characters, but can include letters, numbers, ',' '-' '/'
        if address2 and (not re.match(r'^[A-Za-z0-9\s,/-]+$', address2) or re.match(r'^[,/-]+$', address2)):
            errors['address2'] = "Address2 should contain letters, numbers, or ',', '-', '/'."

        # Department ID validation (if required)
        if not department_id:
            errors['internal_organization'] = "Department is required."

        # Planned Start Date validation (if required)
        if not planned_start_date:
            errors['planned_start_date'] = "Planned Start Date is required."

        # Email validation
        if not email:
            errors['email'] = "Email is required."
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = "Invalid email format."

        # Country validation (if required)
        if not country:
            errors['country'] = "Country is required."

        # State validation (if required)
        if not state:
            errors['state'] = "State is required."

        # Phone Code validation (if required)
        if not phone_code:
            errors['phone_code'] = "Phone Code is required."

        # Employee ID validation (if required)
        if not employee_id:
            errors['employee_id'] = "Employee ID is required."

        if errors:
            context = {
                'errors': errors
            }
            return render(request, 'hrms/emp_per/NewEmploye.html', context)

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

        return render(request, 'hrms/emp_per/NewEmploye.html',{'success':True})
    return render(request, 'hrms/emp_per/NewEmploye.html')
    
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

from datetime import datetime, timezone

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
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        # Handle status update via AJAX
        json_data = json.loads(request.body)
        employee_id = json_data.get('employee_id')
        from_date = json_data.get('from_date')
        through_date = json_data.get('through_date')
        status = json_data.get('status')

        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            through_date_obj = datetime.strptime(through_date, "%Y-%m-%d")

            # Filter the EmployeeLeave record by employee_id, from_date, and through_date
            employee_leave = EmployeeLeave.objects.get(
                employee__employee_id=employee_id,
                from_date=from_date_obj,
                through_date=through_date_obj
            )
            employee_leave.status = status
            employee_leave.save()
            return JsonResponse({'success': True})
        except EmployeeLeave.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'EmployeeLeave not found'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format'})
        

    if request.method == 'POST':
        errors = {}
        employee_id = request.POST.get('employee_id')
        leave_type_id = request.POST.get('leaveTypeID')
        leave_reason_id = request.POST.get('leaveReasonType')
        from_date = request.POST.get('fromDate')
        through_date = request.POST.get('throughDate')
        approver_party_id = request.POST.get('approverParty')
        description = request.POST.get('description', '')
        status = request.POST.get('status', 'Created')

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
        
        if not re.match(r"^[a-zA-Z0-9\s]*$", description):
            errors['description'] = 'Description must contain only alphanumeric characters and spaces.'

        # If errors exist after validation, return them to the template
        if errors:
            return render(request, 'hrms/emp_res_lea/add_emp_leave.html', {'errors': errors})

        # Create the EmployeeLeave record if no errors
        employee_leave, created = EmployeeLeave.objects.update_or_create(
            employee=employee,
            from_date=from_date, 
            through_date=through_date if through_date else None,
            defaults={
                'leave_type': leave_type,
                'leave_reason': leave_reason,
                'approver': approver_party,
                'description': description,
                #'status': status if 'status' in request.POST else 'Created'  # New records get "Created"; updates use the provided status
            }
        )

        if created:
            employee_leave.status = 'Created'  # New records get "Created" status
            employee_leave.save()
            return render(request, 'hrms/emp_res_lea/add_emp_leave.html', {'success': True})
        else:
            employee_leave.status = status  # Updates use the provided status
            employee_leave.save()
            return render(request, 'hrms/emp_res_lea/leave.html')
    
    return render(request, 'hrms/emp_res_lea/add_emp_leave.html')

def employee_leave_search(request):
    if request.method == 'POST':
        # Decode and parse JSON data from the request
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        # Extract search parameters from the JSON data
        employee_id = json_data.get('employee')
        leave_type = json_data.get('leave_type')
        leave_reason = json_data.get('leave_reason')
        from_date = json_data.get('from_date')
        through_date = json_data.get('through_date')
        approver = json_data.get('approver')
        status_ids = json_data.get('status', [])  # Status filter as list of IDs

        # Build the filter dictionary
        filters = {}

        if employee_id:
            filters['employee__employee_id'] = employee_id
        if leave_type:
            filters['leave_type__id'] = leave_type  # Assuming `leave_type` uses an ID field for lookup
        if leave_reason:
            filters['leave_reason__id'] = leave_reason  # Assuming `leave_reason` uses an ID field for lookup
        if from_date:
            filters['from_date__gte'] = from_date
        if through_date:
            filters['through_date__lte'] = through_date
        if approver:
            filters['approver__employee_id'] = approver
        if status_ids:
            filters['status__in'] = status_ids

        # Query the EmployeeLeave model based on the filters
        leaves = EmployeeLeave.objects.filter(**filters)

        # Prepare response data
        response_data = []
        for leave in leaves:
            response_data.append({
                'employee_id': leave.employee.employee_id,  # FK to HR_Employee with employee_id as identifier
                'leave_type': leave.leave_type.leave_type if leave.leave_type else 'N/A',  # Display leave type name if available
                'leave_reason': leave.leave_reason.leave_reason if leave.leave_reason else 'N/A',  # Display leave reason name if available
                'from_date': leave.from_date,
                'through_date': leave.through_date,
                'approver': leave.approver.employee_id if leave.approver else 'N/A',
                'description': leave.description,
                'status': leave.status,
            })

        return JsonResponse(response_data, safe=False)

    # Return error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def delete_leave(request):
    if request.method == 'DELETE':
        employee_id = request.GET.get('employee_id')
        from_date = request.GET.get('from_date')
        through_date = request.GET.get('through_date')

        try:
            # Find and delete the specific record
            leave_record = EmployeeLeave.objects.get(
                employee_id=employee_id, 
                from_date=from_date, 
                through_date=through_date
            )
            leave_record.delete()
            return JsonResponse({'message': 'Leave record deleted successfully'}, status=200)
        except EmployeeLeave.DoesNotExist:
            return JsonResponse({'error': 'Leave record not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

##############################################################################################################################################

def create_employee_resume(request):
    errors = {}  # Dictionary to store validation errors

    if request.method == 'POST':
        # Extract data from the form
        resume_id = request.POST.get('resumeID')
        employee_id = request.POST.get('employee_id')
        content_id = request.POST.get('contentID')
        resume_date = request.POST.get('resumeDate')

        # Regex pattern for allowed characters (alphanumeric and underscores only)
        allowed_pattern = r'^[\w_]+$'

        # Validate employee_id exists in HR_Employee model
        try:
            employee = HR_Employee.objects.get(employee_id=employee_id)
        except HR_Employee.DoesNotExist:
            errors['employee_id'] = 'Employee ID does not exist in HR_Employee records.'

        # Validate resume_id is unique and follows the pattern
        if not resume_id:
            errors['resume_id'] = 'Resume ID is required.'
        elif not re.match(allowed_pattern, resume_id):
            errors['resume_id'] = 'Resume ID can only contain alphanumeric characters and underscores.'
        elif EmployeeResume.objects.filter(resume_id=resume_id).exists():
            errors['resume_id'] = 'Resume ID must be unique.'

        # Validate content_id is unique and follows the pattern
        if not content_id:
            errors['content_id'] = 'Content ID is required.'
        elif not re.match(allowed_pattern, content_id):
            errors['content_id'] = 'Content ID can only contain alphanumeric characters and underscores.'
        elif EmployeeResume.objects.filter(content_id=content_id).exists():
            errors['content_id'] = 'Content ID must be unique.'

        # Check if resume_date is provided
        if not resume_date:
            errors['resume_date'] = 'Resume date is required.'

        # If there are errors, return them to the template
        if errors:
            return render(request, 'hrms/emp_res_lea/New_resume.html', {'errors': errors})

        # If no errors, save the data to EmployeeResume model
        party_resume = EmployeeResume(
            resume_id=resume_id,
            employee_id=employee,
            content_id=content_id,
            resume_date=resume_date
        )
        try:
            party_resume.save()
        except ValidationError as e:
            # Handle any model-level validation errors
            errors['model_error'] = str(e)
            return render(request, 'hrms/emp_res_lea/New_resume.html', {'errors': errors})

        # Return a success message if saved successfully
        return render(request, 'hrms/emp_res_lea/New_resume.html', {'success': True})

    # Display form without errors if method is not POST
    return render(request, 'hrms/emp_res_lea/New_resume.html')

def employee_resume_search(request):
    if request.method == 'POST':
        # Decode and parse JSON data from the request
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        # Extract search parameters from the JSON data
        employee_id = json_data.get('employee_id')
        resume_id = json_data.get('resume_id')
        from_date = json_data.get('from_date')
        through_date = json_data.get('through_date')

        # Build the filter dictionary
        filters = {}

        if employee_id:
            filters['employee_id__employee_id'] = employee_id
        if resume_id:
            filters['resume_id__icontains'] = resume_id
        if from_date:
            filters['resume_date__gte'] = from_date
        if through_date:
            filters['resume_date__lte'] = through_date

        # Query the EmployeeResume model based on the filters
        resumes = EmployeeResume.objects.filter(**filters)

        # Prepare response data
        response_data = []
        for resume in resumes:
            response_data.append({
                'employee_id': resume.employee_id.employee_id,
                'resume_id': resume.resume_id,
                'content_id': resume.content_id,
                'resume_date': resume.resume_date.strftime('%Y-%m-%d') if resume.resume_date else 'N/A',
            })

        return JsonResponse(response_data, safe=False)

    # Return error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def delete_resume(request):
    if request.method == 'DELETE':
        employee_id = request.GET.get('employee_id')
        resume_id = request.GET.get('resume_id')

        try:
            # Find and delete the specific record
            resume_record = EmployeeResume.objects.get(
                employee_id=employee_id, 
                resume_id=resume_id, 
            )
            resume_record.delete()
            return JsonResponse({'message': 'Leave record deleted successfully'}, status=200)
        except EmployeeLeave.DoesNotExist:
            return JsonResponse({'error': 'Leave record not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
###################################### Job Requisition #############################################################################

def jobRequisitionLookup(request):
    return render(request, 'hrms/skill_qual/jobRequisitionLookup.html')
def internalJobPostingLookup(request):
    return render(request, 'hrms/skill_qual/internalJobPostingLookup.html')

def job_requisition_list(request):
    job_requisitions = JobRequisition.objects.all()

    # Retrieve filter parameters from the GET request
    job_location = request.GET.get('job_location')
    job_posting_type = request.GET.get('job_posting_type')
    qualification = request.GET.get('qualification')
    experience_years = request.GET.get('experience_years')

    # Apply filters if parameters are provided
    if job_location:
        job_requisitions = job_requisitions.filter(job_location__icontains=job_location)
    if job_posting_type:
        job_requisitions = job_requisitions.filter(job_posting_type=job_posting_type)
    if qualification:
        job_requisitions = job_requisitions.filter(qualification=qualification)
    if experience_years:
        job_requisitions = job_requisitions.filter(experience_years__gte=int(experience_years))

    context = {
        'job_requisitions': job_requisitions
    }
    return render(request, 'hrms/skill_qual/jobRequisitionLookup.html', context)

def internal_job_posting_lookup(request):
    # Get the filter values from the GET request
    application_date = request.GET.get('application_date')
    applying_party_id = request.GET.get('applying_party_id')
    approver_party_id = request.GET.get('approver_party_id')
    job_requisition_id = request.GET.get('job_requisition_id')

    # Start with all InternalJobPosting records
    postings = InternalJobPosting.objects.all()

    # Apply filters if any of the fields are provided
    if application_date:
        postings = postings.filter(applicationDate=application_date)
    if applying_party_id:
        postings = postings.filter(applyingPartyId__employee_id=applying_party_id)
    if approver_party_id:
        postings = postings.filter(approverPartyId__employee_id=approver_party_id)
    if job_requisition_id:
        postings = postings.filter(jobRequisitionId__job_requisition_id=job_requisition_id)

    context = {
        'postings': postings,
    }


    # Render the full page for initial load
    return render(request, 'hrms/skill_qual/internalJobPostingLookup.html', context)


def create_job_requisition(request):
    if request.method == 'POST':
        # Get data from the form
        job_location = request.POST.get('jobLocation')
        job_posting_type = request.POST.get('jobPostingType')
        age = request.POST.get('age') or None
        no_of_resources = request.POST.get('noOfResources')
        gender = request.POST.get('gender')
        duration_months = request.POST.get('durationMonths') or None
        qualification = request.POST.get('qualification')
        exam_type_enum_id = request.POST.get('examTypeEnumId') or None
        skill_type_id = request.POST.get('skillTypeId')
        experience_years = request.POST.get('experienceYears')
        experience_months = request.POST.get('experienceMonths')

        # Initialize a dictionary to store error messages
        errors = {}

        # Validation for Job Location (required, no special characters)
        if not job_location:
            errors['job_location'] = 'Job Location is required.'
        elif len(job_location) < 3:
            errors['job_location'] = 'Job Location must be at least 3 characters long.'
        elif not re.match(r'^[A-Za-z\s]+$', job_location):  # regex to check only alphabetic characters and spaces
            errors['job_location'] = 'Job Location must only contain letters and spaces.'
        # Validation for No of Resources (must be a positive integer)
        if not no_of_resources or int(no_of_resources) <= 0:
            errors['no_of_resources'] = 'Number of Resources must be a positive integer.'

        # Validation for Age (must be a positive integer or None)
        if age and int(age) < 0:
            errors['age'] = 'Age cannot be negative.'

        # Validation for Duration Months (must be a non-negative integer or None)
        if duration_months and int(duration_months) < 0:
            errors['duration_months'] = 'Duration in months cannot be negative.'

        # Validation for Experience Years (must be a non-negative integer)
        if not experience_years or int(experience_years) < 0:
            errors['experience_years'] = 'Experience years cannot be negative.'

        # Validation for Experience Months (must be a non-negative integer)
        if not experience_months or int(experience_months) < 0:
            errors['experience_months'] = 'Experience months cannot be negative.'

        # Fetch the skill type instance if skill_type_id is provided
        skill_type = SkillType.objects.get(skillTypeId=skill_type_id) if skill_type_id else None

        # Check if there are any validation errors
        if errors:
            return render(request, 'hrms/skill_qual/NewJobRequision.html', {
                'errors': errors,
                'job_location': job_location,
                'job_posting_type': job_posting_type,
                'age': age,
                'no_of_resources': no_of_resources,
                'gender': gender,
                'duration_months': duration_months,
                'qualification': qualification,
                'exam_type_enum_id': exam_type_enum_id,
                'skill_type_id': skill_type_id,
                'experience_years': experience_years,
                'experience_months': experience_months
            })

        # If no errors, create a new Job Requisition record
        new_requisition = JobRequisition(
            job_location=job_location,
            job_posting_type=job_posting_type,
            age=int(age) if age else None,
            no_of_resources=int(no_of_resources),
            gender=gender,
            duration_months=int(duration_months) if duration_months else None,
            qualification=qualification,
            exam_type_enum_id=exam_type_enum_id,
            skill_type=skill_type,
            experience_years=int(experience_years),
            experience_months=int(experience_months)
        )
        new_requisition.save()

        # Redirect to the same page with a success message
        return render(request, 'hrms/skill_qual/NewJobRequision.html', {'success': True})

    # For GET request, render the form
    return render(request, 'hrms/skill_qual/NewJobRequision.html')


def job_requisition_search(request):
    if request.method == 'POST':
        try:
            # Decode and parse JSON data from the request
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Extract search parameters using the correct keys
        requisition_id = data.get('job_requisition_id')
        experience_months = data.get('experience_months')
        experience_years = data.get('experience_years')
        job_location = data.get('job_location')
        skill_type_id = data.get('skill_type')
        job_posting_type = data.get('job_posting_type')
        exam_type_enum_id = data.get('exam_type_enum_id')


        # Build the filter dictionary based on received parameters
        filters = {}
        if requisition_id:
            try:
                filters['job_requisition_id'] = int(requisition_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid job requisition ID'}, status=400)
        if experience_months:
            try:
                filters['experience_months__gte'] = int(experience_months)
            except ValueError:
                return JsonResponse({'error': 'Invalid experience months'}, status=400)
        if experience_years:
            try:
                filters['experience_years__gte'] = int(experience_years)
            except ValueError:
                return JsonResponse({'error': 'Invalid experience years'}, status=400)
        if job_location:
            filters['job_location__icontains'] = job_location.strip()
        if skill_type_id:
            try:
                filters['skill_type__id'] = int(skill_type_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid skill type ID'}, status=400)
        if job_posting_type:
            filters['job_posting_type'] = job_posting_type.strip()
        if exam_type_enum_id:
            try:
                filters['exam_type_enum_id'] = exam_type_enum_id
            except ValueError:
                return JsonResponse({'error': 'Invalid exam type ID'}, status=400)

        # Debugging output
        # print("Filters applied:", filters)

        # Query the database with the filters
        requisitions = JobRequisition.objects.filter(**filters)
        # print("Requisition count:", requisitions.count())  # Debug output

        if not requisitions.exists():
            return JsonResponse({'message': 'No job requisitions found'}, status=404)

        # Prepare the response data
        response_data = [
            {
                'job_requisition_id': req.job_requisition_id,
                'skill_type': req.skill_type.skillTypeId if req.skill_type else 'N/A',
                'job_posting_type': req.job_posting_type,
                'exam_type_enum_id': req.exam_type_enum_id if req.exam_type_enum_id else 'N/A',
                'qualification': req.qualification,
                'job_location': req.job_location,
                'experience_years': req.experience_years,
                'experience_months': req.experience_months,
            }
            for req in requisitions
        ]

        return JsonResponse(response_data, safe=False)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def delete_job_requisition(request):
    if request.method == 'DELETE':
        # Extract query parameters from the request
        job_requisition_id = request.GET.get('job_requisition_id')
        job_location = request.GET.get('job_location')
        job_posting_type = request.GET.get('job_posting_type')

        if not job_requisition_id or not job_location or not job_posting_type:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        try:
            # Find and delete the specific job record based on the given parameters
            resume_record = JobRequisition.objects.get(
                job_requisition_id=job_requisition_id,
                job_location=job_location,
                job_posting_type=job_posting_type
            )
            resume_record.delete()
            
            # Return success response if deletion is successful
            return JsonResponse({'message': 'Job requisition deleted successfully'}, status=200)
        
        except EmployeeResume.DoesNotExist:
            return JsonResponse({'error': 'Job requisition not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


####################################################################################################################

def create_internal_job(request):
    errors = {}  # Dictionary to store error messages
    
    if request.method == 'POST':
        # Get form data from the request
        application_date = request.POST.get('applicationDate')
        applying_party_id = request.POST.get('applyingPartyId')
        approver_party_id = request.POST.get('approverPartyId')
        job_requisition_id = request.POST.get('jobRequisitionId')

        # Step 1: Validate application date
        if not application_date:
            errors['applicationDate'] = "Application date is required."
        else:
            # Check if the date is valid and timezone aware
            from django.utils import timezone
            from datetime import datetime
            try:
                # Convert to datetime and make it aware
                application_date = timezone.make_aware(
                    datetime.strptime(application_date, "%Y-%m-%d")
                )
            except ValueError:
                errors['applicationDate'] = "Invalid date format. Please use YYYY-MM-DD format."

        # Step 2: Validate applying party ID
        if not applying_party_id:
            errors['applyingPartyId'] = "Applying Party ID is required."
        else:
            try:
                applying_party = HR_Employee.objects.get(employee_id=applying_party_id)
            except HR_Employee.DoesNotExist:
                errors['applyingPartyId'] = "Applying Party ID does not exist."

        # Step 3: Validate approver party ID
        if not approver_party_id:
            errors['approverPartyId'] = "Approver Party ID is required."
        else:
            try:
                approver_party = HR_Employee.objects.get(employee_id=approver_party_id)
            except HR_Employee.DoesNotExist:
                errors['approverPartyId'] = "Approver Party ID does not exist."

        # Step 4: Validate job requisition ID
        if not job_requisition_id:
            errors['jobRequisitionId'] = "Job Requisition ID is required."
        else:
            try:
                job_requisition = JobRequisition.objects.get(job_requisition_id=job_requisition_id)
            except JobRequisition.DoesNotExist:
                errors['jobRequisitionId'] = "Job Requisition ID does not exist."

        # Step 5: If no errors, create a new InternalJobPosting entry
        if not errors:
            new_posting = InternalJobPosting.objects.create(
                applicationDate=application_date,
                applyingPartyId=applying_party,
                approverPartyId=approver_party,
                jobRequisitionId=job_requisition,
                status='Applied'
            )
            return render(request, 'hrms/skill_qual/newInternalJobPosting.html', {'success': True})

    # If there are errors, render the form again with error messages
    return render(request, 'hrms/skill_qual/newInternalJobPosting.html', {'errors': errors})


def job_application_search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Extract parameters from the POST data
        application_id = data.get('applicationId', None)
        status = data.get('status', None)
        application_date = data.get('applicationDate', None)
        application_date_operator = data.get('applicationDateOperator', 'equals')
        applying_party_id = data.get('applyingPartyId', None)
        approver_party_id = data.get('approverPartyId', None)
        job_requisition_id = data.get('jobRequisitionId', None)

        # Prepare the filter criteria
        filters = Q()
        
        if application_id:
            filters &= Q(applicationId=application_id)
        if status:
            filters &= Q(status=status)
        if applying_party_id:
            filters &= Q(applyingPartyId__employee_id=applying_party_id)
        if approver_party_id:
            filters &= Q(approverPartyId__employee_id=approver_party_id)
        if job_requisition_id:
            filters &= Q(jobRequisitionId__job_requisition_id=job_requisition_id)
        
        if application_date:
            try:
                date_obj = datetime.strptime(application_date, '%Y-%m-%d').date()
            except ValueError:
                date_obj = None

            # Handle the operator logic for date filtering
            if application_date_operator == 'equals' and date_obj:
                filters &= Q(applicationDate=date_obj)
            elif application_date_operator == 'lessThan' and date_obj:
                filters &= Q(applicationDate__lt=date_obj)
            elif application_date_operator == 'greaterThan' and date_obj:
                filters &= Q(applicationDate__gt=date_obj)

        # Query the database based on the filters
        job_applications = InternalJobPosting.objects.filter(filters)

        # Serialize the data into a response format
        results = []
        for application in job_applications:
            results.append({
                'applicationId': application.applicationId,
                'status': application.status,
                'applyingPartyId': application.applyingPartyId.employee_id,  # Adjusted for employee_id
                'approverPartyId': application.approverPartyId.employee_id,  # Adjusted for employee_id
                'jobRequisitionId': application.jobRequisitionId.job_requisition_id,  # Adjusted for job_requisition_id
                'applicationDate': application.applicationDate,
            })

        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_job_application(request):
    if request.method == 'DELETE':
        # Get query parameters
        application_id = request.GET.get('applicationId')
        applying_party_id = request.GET.get('applyingPartyId')

        # Find the job application to delete
        try:
            application = InternalJobPosting.objects.get(applicationId=application_id, applyingPartyId__employee_id=applying_party_id)
            application.delete()
            return JsonResponse({'message': 'Job application deleted successfully'}, status=200)
        except InternalJobPosting.DoesNotExist:
            return JsonResponse({'error': 'Job application not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def update_application_status(request, application_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')

            print(f'Status: {status}')

            # Validate the status value against the choices defined in the model
            if status not in dict(InternalJobPosting.APPLICATION_STATUS_CHOICES):
                return JsonResponse({'error': 'Invalid status'}, status=400)

            # Fetch the application record
            application = InternalJobPosting.objects.get(applicationId=application_id)

            # Update the status
            application.status = status
            application.save()

            return JsonResponse({'message': f'Application {application_id} status updated to {status}.'})

        except InternalJobPosting.DoesNotExist:
            return JsonResponse({'error': 'Application not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
###########################################################################################################################

def create_job_interview(request):
    errors = {}  # Dictionary to store error messages

    if request.method == 'POST':
        # Get form data from the request
        job_interviewee_id = request.POST.get('jobIntervieweePartyId')
        job_interviewer_id = request.POST.get('jobInterviewerPartyId')
        job_requisition_id = request.POST.get('jobRequisitionId')
        job_interview_type_id = request.POST.get('jobInterviewTypeId')
        grade_secured = request.POST.get('gradeSecuredEnumId')
        interview_result = request.POST.get('jobInterviewResult')
        interview_date = request.POST.get('jobInterviewDate')

        # Step 1: Validate interview date
        if not interview_date:
            errors['jobInterviewDate'] = "Interview date is required."
        else:
            # Validate date format and make it timezone aware
            from django.utils import timezone
            from datetime import datetime
            try:
                interview_date = timezone.make_aware(
                    datetime.strptime(interview_date, "%Y-%m-%d")
                )
            except ValueError:
                errors['jobInterviewDate'] = "Invalid date format. Please use YYYY-MM-DD format."

        # Step 2: Validate job interviewee ID
        if not job_interviewee_id:
            errors['jobIntervieweePartyId'] = "Interviewee Party ID is required."
        else:
            try:
                job_interviewee = HR_Employee.objects.get(employee_id=job_interviewee_id)
            except HR_Employee.DoesNotExist:
                errors['jobIntervieweePartyId'] = "Interviewee Party ID does not exist."

        # Step 3: Validate job interviewer ID
        if not job_interviewer_id:
            errors['jobInterviewerPartyId'] = "Interviewer Party ID is required."
        else:
            try:
                job_interviewer = HR_Employee.objects.get(employee_id=job_interviewer_id)
            except HR_Employee.DoesNotExist:
                errors['jobInterviewerPartyId'] = "Interviewer Party ID does not exist."

        # Step 4: Validate job requisition ID
        if not job_requisition_id:
            errors['jobRequisitionId'] = "Job Requisition ID is required."
        else:
            try:
                job_requisition = JobRequisition.objects.get(job_requisition_id=job_requisition_id)
            except JobRequisition.DoesNotExist:
                errors['jobRequisitionId'] = "Job Requisition ID does not exist."

        # Step 5: Validate job interview type ID
        if not job_interview_type_id:
            errors['jobInterviewTypeId'] = "Job Interview Type ID is required."
        else:
            try:
                job_interview_type = JobInterviewType.objects.get(jobinterviewType=job_interview_type_id)
            except JobInterviewType.DoesNotExist:
                errors['jobInterviewTypeId'] = "Job Interview Type ID does not exist."

        # Step 6: If no errors, create or update the JobInterview entry
        if not errors:
            job_interview, created = JobInterview.objects.update_or_create(
                job_interviewee_party=job_interviewee,
                job_interviewer_party=job_interviewer,
                job_requisition=job_requisition,
                defaults={
                    'job_interview_type': job_interview_type,
                    'grade_secured_enum_id': grade_secured,
                    'job_interview_result': interview_result,
                    'job_interview_date': interview_date,
                }
            )
            return render(request, 'hrms/skill_qual/NewjobInterview.html', {'success': True})

    # If there are errors, render the form again with error messages
    return render(request, 'hrms/skill_qual/NewjobInterview.html', 
                  {
                      'errors': errors,
                      'job_interviewee_party': job_interviewee_id,
                      'job_interviewer_party': job_interviewer_id,
                      'job_requisition': job_requisition_id,
                      'job_interview_date': interview_date.strftime('%Y-%m-%d') if interview_date else '',
                      })


def job_interview_search(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON payload
            data = json.loads(request.body)

            # Extract the filters from the payload
            job_interview_id = data.get('job_interview_id')
            job_interview_id_op = data.get('job_interview_id_op', 'equals')  # Default to 'equals'

            job_interviewee_party_id = data.get('job_interviewee_party_id')
            job_requisition_id = data.get('job_requisition_id')
            job_interviewer_party_id = data.get('job_interviewer_party_id')

            job_interview_type_id = data.get('job_interview_type_id')
            grade_secured_enum_id = data.get('grade_secured_enum_id')
            job_interview_result = data.get('job_interview_result')

            job_interview_start_date = data.get('job_interview_start_date')
            job_interview_start_date_op = data.get('job_interview_start_date_op', 'equals')  # Default to 'equals'
            job_interview_end_date = data.get('job_interview_end_date')
            job_interview_end_date_op = data.get('job_interview_end_date_op', 'equals')  # Default to 'equals'

            # Prepare the filter criteria
            filters = Q()

            # Apply filters for the fields with operators
            if job_interview_id:
                if job_interview_id_op == 'equals':
                    filters &= Q(id=job_interview_id)
                elif job_interview_id_op == 'lessThan':
                    filters &= Q(id__lt=job_interview_id)
                elif job_interview_id_op == 'greaterThan':
                    filters &= Q(id__gt=job_interview_id)

            if job_interviewee_party_id:
                filters &= Q(job_interviewee_party__employee_id=job_interviewee_party_id)
            if job_requisition_id:
                filters &= Q(job_requisition__job_requisition_id=job_requisition_id)
            if job_interviewer_party_id:
                filters &= Q(job_interviewer_party__employee_id=job_interviewer_party_id)
            if job_interview_type_id:
                filters &= Q(job_interview_type__jobinterviewType=job_interview_type_id)
            if grade_secured_enum_id:
                filters &= Q(grade_secured_enum_id=grade_secured_enum_id)
            if job_interview_result:
                filters &= Q(job_interview_result=job_interview_result)

            # Handle start date filtering
            if job_interview_start_date:
                try:
                    start_date_obj = datetime.strptime(job_interview_start_date, '%Y-%m-%d').date()
                except ValueError:
                    start_date_obj = None

                if start_date_obj:
                    if job_interview_start_date_op == 'equals':
                        filters &= Q(job_interview_date=start_date_obj)  # Use job_interview_date here
                    elif job_interview_start_date_op == 'lessThan':
                        filters &= Q(job_interview_date__lt=start_date_obj)  # Use job_interview_date here
                    elif job_interview_start_date_op == 'greaterThan':
                        filters &= Q(job_interview_date__gt=start_date_obj)

            # Handle end date filtering
            if job_interview_end_date:
                try:
                    end_date_obj = datetime.strptime(job_interview_end_date, '%Y-%m-%d').date()
                except ValueError:
                    end_date_obj = None

                if end_date_obj:
                    if job_interview_end_date_op == 'equals':
                        filters &= Q(job_interview_date=end_date_obj)
                    elif job_interview_end_date_op == 'lessThan':
                        filters &= Q(job_interview_date__lt=end_date_obj)
                    elif job_interview_end_date_op == 'greaterThan':
                        filters &= Q(job_interview_date__gt=end_date_obj)

            # Query the database based on the filters
            job_interviews = JobInterview.objects.filter(filters)

            # Serialize the data into a response format
            results = []
            for interview in job_interviews:
                results.append({
                    'jobInterviewId': interview.id,
                    'jobIntervieweePartyId': interview.job_interviewee_party.employee_id,
                    'jobRequisitionId': interview.job_requisition.job_requisition_id,
                    'jobInterviewerPartyId': interview.job_interviewer_party.employee_id,
                    'jobInterviewTypeId': interview.job_interview_type.jobinterviewType,
                    'gradeSecuredEnumId': interview.grade_secured_enum_id,
                    'jobInterviewResult': interview.job_interview_result,
                    'jobInterviewDate': interview.job_interview_date,
                })

            return JsonResponse(results, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
#########################################################################################################################

from django.utils import timezone
from datetime import datetime

def add_training_class(request):
    errors = {}  # Dictionary to store error messages

    if request.method == 'POST':
        # Get form data from the request
        approver_id = request.POST.get('approverId')
        training_type_id = request.POST.get('trainingType')
        description = request.POST.get('description')
        from_date = request.POST.get('fromDate')
        from_time = request.POST.get('fromTime')
        through_date = request.POST.get('throughDate')
        through_time = request.POST.get('throughTime')

        # Step 1: Validate Approver ID
        if not approver_id:
            errors['approverId'] = "Approver Party ID is required."
        else:
            try:
                approver = HR_Employee.objects.get(employee_id=approver_id)
            except HR_Employee.DoesNotExist:
                errors['approverId'] = "Approver Party ID does not exist."

        # Step 2: Validate Training Type
        if not training_type_id or training_type_id == "Select Training Type":
            errors['trainingType'] = "Training Type is required."
        else:
            try:
                training_type = TrainingClassType.objects.get(tranningTypeId=training_type_id)
            except TrainingClassType.DoesNotExist:
                errors['trainingType'] = "Training Type does not exist."

        # Step 3: Validate From Date
        if not from_date:
            errors['fromDate'] = "From Date is required."
        else:
            try:
                from_date = timezone.make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
            except ValueError:
                errors['fromDate'] = "Invalid date format. Please use YYYY-MM-DD."

        # Step 4: Validate Through Date
        if not through_date:
            errors['throughDate'] = "Through Date is required."
        else:
            try:
                through_date = timezone.make_aware(datetime.strptime(through_date, "%Y-%m-%d"))
            except ValueError:
                errors['throughDate'] = "Invalid date format. Please use YYYY-MM-DD."

        # Step 5: Validate From Time and Through Time
        if not from_time:
            errors['fromTime'] = "From Time is required."
        if not through_time:
            errors['throughTime'] = "Through Time is required."

        if not description:
            errors['description'] = "Description is required."
        elif re.match(r'^[^a-zA-Z0-9]', description):
            # Check if description starts with a special character
            errors['description'] = "Description should not start with a special character."
        elif not re.search(r'[a-zA-Z0-9]', description):
            # Check if description contains only special characters (no alphanumeric characters)
            errors['description'] = "Description should not contain only special characters."

        # Step 6: If no errors, create or update the TrainingClass entry
        if not errors:
            try:
                training_class, created = TrainingClass.objects.update_or_create(
                    approverId=approver,
                    trainingType=training_type,
                    description=description,
                    defaults={
                        'fromDate': from_date,
                        'fromTime': from_time,
                        'throughDate': through_date,
                        'throughTime': through_time
                    }
                )
                return render(request, 'hrms/skill_qual/addnewEvent.html', {'success': True})
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    # Fetch data for dropdowns and render the form
    employees = HR_Employee.objects.all()
    training_types = TrainingClassType.objects.all()

    return render(request, 'hrms/skill_qual/addnewEvent.html', {
        'errors': errors,
        'employees': employees,
        'training_types': training_types,
        'approverId': request.POST.get('approverId', ''),
        'description': request.POST.get('description', ''),
        'fromDate': request.POST.get('fromDate', ''),
        'fromTime': request.POST.get('fromTime', ''),
        'throughDate': request.POST.get('throughDate', ''),
        'throughTime': request.POST.get('throughTime', ''),
    })


@require_GET
def get_trainings(request):
    date = request.GET.get('date')
    
    # Fetch trainings scheduled for the given date
    trainings = TrainingClass.objects.filter(fromDate=date).select_related('trainingType').values(
        'trainingClassId',
        'approverId__employee_id',
        'trainingType__description',  # Adjust the field if the name is different in TrainingClassType
        'description',
        'fromTime',
        'throughTime'
    )
    
    return JsonResponse(list(trainings), safe=False)

def add_attendee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        training_class_id = request.POST.get('training_class_id')

        try:
            employee = HR_Employee.objects.get(employee_id=employee_id)
            training_class = TrainingClass.objects.get(trainingClassId=training_class_id)

            if TrainingAttendee.objects.filter(employee=employee, trainingClass=training_class).exists():
                return JsonResponse({'success': False, 'error': 'Employee is already assigned to this training class'})

            # Create a new attendee
            attendee = TrainingAttendee.objects.create(
                employee=employee,
                trainingClass=training_class,
                status='Assigned'
            )
            
            return JsonResponse({
                'success': True,
                'attendee': {
                    'employee_id': attendee.employee.employee_id,
                    'training_type_id': attendee.attendeeId,
                    'training_class_id': attendee.trainingClass.trainingClassId,
                    'status': attendee.status
                }
            })
        except HR_Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'})
        except TrainingClass.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Training Class not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_attendees(request, training_class_id):
    print(f'Training Class ID received: {training_class_id}')
    
    # Fetch all attendees related to the specified training class
    attendees = TrainingAttendee.objects.filter(trainingClass__trainingClassId=training_class_id).values(
        'employee__employee_id',        # Fetch the employee ID from the related HR_Employee model
        'attendeeId',                   # Attendee ID from the TrainingAttendee model
        'trainingClass__trainingClassId', # Training Class ID from the related TrainingClass model
        'status'                        # Attendee status
    )
    
    # Debugging to verify the fetched attendees
    print(f'Fetched Attendees: {list(attendees)}')
    
    return JsonResponse(list(attendees), safe=False)

def addnew_event(request):
    date = request.GET.get('date')
    return render(request, 'hrms/skill_qual/addnewEvent.html', {'date': date})

def get_upcoming_training_classes(request):
    current_date = datetime.now().date()  # Get the current date (no time)
    upcoming_classes = TrainingClass.objects.filter(fromDate__gte=current_date).order_by('fromDate', 'fromTime')
    
    data = []
    for training_class in upcoming_classes:
        data.append({
            'from_date': training_class.fromDate.strftime('%Y-%m-%d'),
            'from_time': training_class.fromTime.strftime('%H:%M %p'),
            'through_date': training_class.throughDate.strftime('%Y-%m-%d'),
            'through_time': training_class.throughTime.strftime('%H:%M %p'),
            'training_type': training_class.trainingType.description,  # Adjust this field as per your model's relation
            'description': training_class.description,
        })
    return JsonResponse(data, safe=False)
#########################################################################################################################

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
def lookups(request):
    return render(request, 'hrms/skill_qual/lookups.html')


def pay_slip(request):
    return render(request, 'hrms/emp_res_lea/pay_slip.html')

def payslip_create(request):
    return render(request, 'hrms/emp_res_lea/payslip_create.html')


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
    

###########################################################################################################################################

# class PerformanceReviewViewSet(viewsets.ModelViewSet):
#     queryset = PerformanceReview.objects.all()
#     serializer_class = PerformanceReviewSerializer

#     def list(self, request, *args, **kwargs):
#         employee_id = request.query_params.get('employee_id', None)
#         email = request.query_params.get('email', None)
#         performance_review_id = request.query_params.get('performance_review_id', None)

#         # Apply filters based on query parameters
#         if performance_review_id:
#             performance_reviews = self.queryset.filter(perf_review_id=performance_review_id)
#         elif employee_id:
#             performance_reviews = self.queryset.filter(hr_employee__employee_id=employee_id)
#         elif email:
#             performance_reviews = self.queryset.filter(hr_employee__email=email)
#         else:
#             performance_reviews = self.queryset

#         if not performance_reviews.exists():
#             return Response({"detail": "No performance review found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(performance_reviews, many=True)
#         return Response(serializer.data)


def create_performance_review(request):
    if request.method == 'POST':
        try:
            # Parse incoming data
            data = request.POST
            perf_review_id = data.get('perfReviewId', '')
            employee_party_id = data.get('employeePartyId', '')
            manager_party_id = data.get('managerPartyId', '')
            manager_role_type = data.get('managerRoleType', '')
            payment_id = data.get('paymentId', '')
            empl_position_name = data.get('emplPositionId', '')
            from_date = data.get('fromDate', '')
            through_date = data.get('throughDate', '')
            comments = data.get('comments', '')

            # Check if the employee exists in the HR_Employee model
            try:
                employee = HR_Employee.objects.get(employee_id=employee_party_id)
            except HR_Employee.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Employee not found.'})

            # Handle missing or invalid Position Type
            position_type = None
            if empl_position_name:  # Only try to find a PositionType if one is provided
                try:
                    position_type = PositionType.objects.get(name=empl_position_name)
                except PositionType.DoesNotExist:
                    # If PositionType doesn't exist, we just keep it as None
                    
                    # Optional: You could return an error here if you want strict validation
                    return JsonResponse({'status': 'error', 'message': 'Position Type not found.'})
            # Parse dates
            from_date_parsed = datetime.strptime(from_date, '%Y-%m-%d').date() if from_date else None
            through_date_parsed = datetime.strptime(through_date, '%Y-%m-%d').date() if through_date else None

            # Create the Performance Review entry, even with blank/null data
            review = PerformanceReview.objects.create(
                perf_review_id=perf_review_id,
                emp_party_id=employee,
                manager_party_id=manager_party_id,
                manager_role_type=manager_role_type,
                payment_id=payment_id,
                empl_position_type=position_type,  # Can be None if PositionType is missing
                from_date=from_date_parsed,
                through_date=through_date_parsed,
                comments=comments
            )

            return JsonResponse({'status': 'success', 'message': 'Performance review created successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



def find_performance_review(request):
    if request.method == 'POST':
        # Get form data from the POST request
        perf_review_id = request.POST.get('perfReviewId', '').strip()
        employee_party_id = request.POST.get('employeePartyId', '').strip()
        manager_party_id = request.POST.get('managerPartyId', '').strip()
        manager_role_type_id = request.POST.get('managerRoleTypeId', '').strip()
        payment_id = request.POST.get('paymentId', '').strip()
        empl_position_name = request.POST.get('emplPositionName', '').strip()
        from_date = request.POST.get('fromDate', '').strip()
        through_date = request.POST.get('throughDate', '').strip()
        comments = request.POST.get('comments', '').strip()

        # Initialize filters object
        filters = {}

        # Apply filters (only if the fields are not empty)
        if perf_review_id:
            filters['perf_review_id__icontains'] = perf_review_id
        if employee_party_id:
            filters['emp_party_id__employee_id__icontains'] = employee_party_id
        if manager_party_id:
            filters['manager_party_id__icontains'] = manager_party_id
        if manager_role_type_id:
            filters['manager_role_type__icontains'] = manager_role_type_id
        if payment_id:
            filters['payment_id__icontains'] = payment_id
        if empl_position_name:
            filters['empl_position_type__name__icontains'] = empl_position_name
        if from_date:
            filters['from_date__gte'] = from_date
        if through_date:
            filters['through_date__lte'] = through_date
        if comments:
            filters['comments__icontains'] = comments

        # Query the database with filters
        reviews = PerformanceReview.objects.filter(**filters)

        # Format the result data
        review_data = [
            {
                'performance_review_id': review.perf_review_id,
                'employee_party_id': review.emp_party_id.employee_id,
                'manager_party_id': review.manager_party_id,
                'manager_role_type_id': review.manager_role_type,
                'payment_id': review.payment_id,
                'empl_position_name': review.empl_position_type.name if review.empl_position_type else None,
                'from_date': review.from_date,
                'through_date': review.through_date,
                'comments': review.comments,
            }
            for review in reviews
        ]

        # Return the data in JSON format
        return JsonResponse({'data': review_data})

    return render(request, 'hrms/emp_per/performance.html')


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

#######################################################################################################################################################

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

class SkillTypeList(APIView):
    def get(self, request):
        skillTypeId = SkillType.objects.all()
        serializer = SkillTypeSerializer(skillTypeId, many=True)
        return Response(serializer.data)
    
class JobInterviewTypeList(APIView):
    def get(self, request):
        jobinterviewType = JobInterviewType.objects.all()
        serializer = JobInterviewTypeSerializer(jobinterviewType, many=True)
        return Response(serializer.data)

class TrainingClassTypeList(APIView):
    def get(self, request):
        TrainingClassTypes = TrainingClassType.objects.all()
        serializer = TrainingClassTypeSerializer(TrainingClassTypes, many=True)
        return Response(serializer.data)
    

@csrf_protect
@require_POST
def create_employment_application(request):
    # Parse incoming JSON data
    try:
        data = json.loads(request.body)

        # Extract data from request (use None if the field is not provided)
        application_id = data.get('applicationId', None)
        position_id = data.get('positionId', None)
        status = data.get('statusId', None)
        empapp_source = data.get('empappSourceId', None)
        party_id = data.get('partyId', None)
        application_date = data.get('applicationDate', None)
        print(f"position_id: {position_id}")

        # Lookup the position, party (applying party), etc. by their IDs if provided
        position = PositionType.objects.get(name=position_id) if position_id else None
        applying_party = HR_Employee.objects.get(employee_id=party_id) if party_id else None

        # Create and save the EmploymentApplication instance
        application = EmploymentApplication.objects.create(
            application_id=application_id,
            position=position,
            status=status,
            source=empapp_source,
            applying_party=applying_party,
            application_date=application_date
        )

        # Return a success response
        return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
def search_employment_applications(request):
    # Fetch parameters from the request query
    appID = request.GET.get('appID', '')
    positionID = request.GET.get('positionID', '')
    empappSourceId = request.GET.get('empappSourceId', '')
    applyingParty = request.GET.get('applyingParty', '')
    applicationDateStart = request.GET.get('applicationDateStart', '')
    applicationDateEnd = request.GET.get('applicationDateEnd', '')
    statuses = request.GET.get('statuses', '')  # Get the statuses from the request
    
    # Build the filter condition dynamically based on input
    filter_conditions = Q()

    if appID:
        filter_conditions &= Q(application_id__icontains=appID)
    if positionID:
        filter_conditions &= Q(position__name__icontains=positionID)
    if empappSourceId:
        filter_conditions &= Q(source=empappSourceId)
    if applyingParty:
        # Filter based on the HR_Employee's employee_id
        filter_conditions &= Q(applying_party__employee_id=applyingParty)
    if applicationDateStart:
        filter_conditions &= Q(application_date__gte=parse_date(applicationDateStart))
    if applicationDateEnd:
        filter_conditions &= Q(application_date__lte=parse_date(applicationDateEnd))
    
    # If the 'statuses' parameter is provided, add it to the filter
    if statuses:
        status_list = [int(status) for status in statuses.split(',')]  # Convert the string to a list of integers
        filter_conditions &= Q(status__in=status_list)  # Filter by status

    # Fetch the filtered applications
    applications = EmploymentApplication.objects.filter(filter_conditions)

    # Prepare the response data
    result_data = []
    for app in applications:
        app_data = {
            'appID': app.application_id,
            'positionID': app.position.name if app.position else None,  # Position name instead of ID
            'status': dict(EmploymentApplication.STATUS_CHOICES).get(app.status, 'Unknown'),
            'empappSource': dict(EmploymentApplication.SOURCE_CHOICES).get(app.source, 'Unknown'),
            'applicationDate': app.application_date.strftime('%Y-%m-%d'),
        }
        
        # Add applyingParty only if applying_party exists
        if app.applying_party:
            app_data['applyingParty'] = app.applying_party.employee_id
        
        result_data.append(app_data)

    # Return the response as JSON
    return JsonResponse({'success': True, 'data': result_data})

def delete_employment_application(request):
    if request.method == 'DELETE':
        # Get query parameters
        application_id = request.GET.get('applicationId')
        applying_party_id = request.GET.get('applyingPartyId')

        # Validate the parameters
        if not application_id or not applying_party_id:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        # Find the job application to delete
        try:
            application = EmploymentApplication.objects.get(application_id=application_id, applying_party_id__employee_id=applying_party_id)
            application.delete()
            return JsonResponse({'message': 'Job application deleted successfully'}, status=200)
        except EmploymentApplication.DoesNotExist:
            return JsonResponse({'error': 'Job application not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

##########################################################################################################################################################

def view_training_approvals(request):
    # Fetch all the training class data and prefetch related attendees
    results = TrainingClass.objects.prefetch_related(
        Prefetch('trainingattendee_set', queryset=TrainingAttendee.objects.all(), to_attr='attendees')
    )

    # Directly pass the results to the template
    return render(request, 'hrms/skill_qual/TrainingApproval.html', {'results': results})