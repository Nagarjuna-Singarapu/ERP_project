#ERP_project/crm_app/HRMS/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_countries, get_states
from . import views

router = DefaultRouter()
# router.register(r'hr-employees', HREmployeeViewSet, basename='hr_employee')
# router.register(r'performance-reviews', PerformanceReviewViewSet, basename='performance_review')

urlpatterns = [
    path('api/countries/', get_countries, name='get_countries'),
    path('api/states/<str:country_name>/', get_states, name='get_states'),
    path('submit-employee/', views.submit_employee, name='submit_employee'),
    # path('create-employee/', views.create_employee, name='create_employee'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-employee-id/', views.check_employee_id, name='check_employee_id'),

    path('search-employees/', views.search_employees, name='search_employees'),
    # path('find-employee/', views.find_employee, name='find_employee'),
    # path('lookup/', views.find_employee, name='lookup'),

    path('create-employment/', views.create_employment, name='create_employment'),
    path('api/get-employee-data/', views.get_employee_data, name='get_employee_data'),
    path('api/department/', views.get_departments, name='get_departments'),
    path('api/paygrades/', views.PayGradeList.as_view(), name='paygrade-list'),
    path('api/salarysteps/', views.SalaryStepList.as_view(), name='salarystep-list'),
    path('api/terminationtype/', views.TerminationTypeList.as_view(), name='terminationType-list'),
    path('api/terminationreason/', views.TerminationReasonList.as_view(), name='terminationReason-list'),
    path('api/positiontypes/', views.PositionTypeList.as_view(), name='positiontype-list'),
    path('api/leavetypes/', views.LeaveTypeList.as_view(), name='leaveType-list'),
    path('api/leavereasons/', views.LeaveReasonList.as_view(), name='leaveReason-list'),
    path('api/skilltypes/', views.SkillTypeList.as_view(), name='skillType-list'),
    path('api/jobinterviewtypes/', views.JobInterviewTypeList.as_view(), name='jobInterviewType-list'),
    path('api/trainingclasstypes/', views.TrainingClassTypeList.as_view(), name='trainingClassType-list'),

    path('employment-search/', views.employment_search, name='employment_search'),
    path('api/employment-data/', views.employment_data, name='employment_data'),

    path('create-employee-position/', views.create_employee_position, name='create_employee_position'),
    path('api/get-employee-position-data/', views.get_employee_position, name='get_employee_position'),
    path('employment-position-search/', views.employment_position_search, name='employment_position_search'),
    path('api/employment-position-data/', views.employment_position_data, name='employment_position_data'),
    
    path('create-employee-qualification/', views.create_employee_qualification, name='create_employee_qualification'),
    path('employee-qualification-search/', views.employee_qualification_search, name='employee_qualification_search'),
    path('api/employee-qualification-data/', views.employee_qualification_data, name='employee_qualification_data'),
    path('api/delete-qualification/<str:employee_id>/', views.delete_employee_qualification, name='delete_employee_qualification'),

    path('add-employee-leave/', views.add_employee_leave, name='add_employee_leave'),
    path('employee-leave-search/', views.employee_leave_search, name='employee_leave_search'),
    path('api/delete-leave/', views.delete_leave, name='delete_leave'),

    path('create-employee-resume/', views.create_employee_resume, name='create_employee_resume'),
    path('employee-resume-search/', views.employee_resume_search, name='employee_resume_search'),
    path('api/delete-resume/', views.delete_resume, name='delete_resume'),

    path('job-requisitions/', views.job_requisition_list, name='job_requisition_list'),
    path('jobRequisitionLookup/', views.jobRequisitionLookup, name='jobRequisitionLookup'),
    path('internalJobPostingLookup/', views.internalJobPostingLookup, name='internalJobPostingLookup'),
    path('internal-job-posting-lookup/', views.internal_job_posting_lookup, name='internal_job_posting_lookup'),
    path('new-job-requisition/', views.create_job_requisition, name='new_job_requisition'),
    path('job-requisition-search/', views.job_requisition_search, name='job_requisition_search'),
    path('api/delete-job-requisition/', views.delete_job_requisition, name='delete_job_requisition'),

    path('create-internal-job/', views.create_internal_job, name='create_internal_job'),
    path('job-application-search/', views.job_application_search, name='job_application_search'),
    path('api/delete-job-application/', views.delete_job_application, name='delete_job_application'),
    path('update-application-status/<int:application_id>/', views.update_application_status, name='update_application_status'),

    path('create-job-interview/', views.create_job_interview, name='create_job_interview'),
    path('job-interview-search/', views.job_interview_search, name='job_interview_search'),

    path('add-training/', views.add_training_class, name='add_training_class'),
    path('api/get-trainings/', views.get_trainings, name='get_trainings'),
    path('add-attendee/', views.add_attendee, name='add_attendee'),
    path('get-attendees/<int:training_class_id>/', views.get_attendees, name='get_attendees'),
    path('addnewEvent/', views.addnew_event, name='addnewEvent'),
    path('api/upcoming-training/', views.get_upcoming_training_classes, name='get_upcoming_training_classes'),

    # anuj hrms
    path('NewEmploye/', views.NewEmploye, name='NewEmploye'),
    path('emp_main/', views.emp_main, name='emp_main'),
    path('Employment/', views.Employments, name='Employment'),
    path('Employe_position/', views.Employe_position, name='Employe_position'),    
    path('lookup/', views.lookup, name='lookup'),
    path('NewEmployement/', views.NewEmployement, name='NewEmployement'),
    path('FindEmploye/', views.FindEmploye, name='FindEmploye'),
    path('New_positions/', views.New_positions, name='New_positions'),
    path('Search_Emp_position/', views.Search_Emp_position, name='Search_Emp_position'),
    path('Paygrad/', views.Paygrad, name='Paygrad'),
    path('EditSalary/', views.EditSalary, name='EditSalary'),
    path('performance/', views.performance, name='performance'),
    path('EditPerformace/', views.EditPerformace, name='EditPerformace'),
    path('LookUpPerformace/', views.LookUpPerformace, name='LookUpPerformace'),
     
    # sunny hrms
    path('employement_appli/', views.employement_appli, name='employement_appli'),
    path('New_emp_app/', views.New_emp_app, name='New_emp_app'),
    path('resume/', views.resume, name='resume'),
    path('leave/', views.leave, name='leave'),
    path('lookup_emp_app/', views.lookup_emp_app, name='lookup_emp_app'),
    path('lookup_emp_posi/', views.lookup_emp_posi, name='lookup_emp_posi'),
    path('lookup_party/', views.lookup_party, name='lookup_party'),
    path('New_resume/', views.New_resume, name='New_resume'),
    path('lookup_party_resume/', views.lookup_party_resume, name='lookup_party_resume'),
    path('add_emp_leave/', views.add_emp_leave, name='add_emp_leave'),
    path('leave_approval/', views.leave_approval, name='leave_approval'),

    path('pay_slip/', views.pay_slip, name='pay_slip'),
    path('payslip_create/', views.payslip_create, name='payslip_create'),
    
    # global HR by sunny and amit 
    path('skill-types/', views.skill_types, name='skill_types'),

    path('api/get-skill-type/', views.get_skill_type, name='get_skill_type'),
    path('skill-type/', views.skill_type, name='skill_type'),

    path('responsibility_types/', views.responsibility_types, name='responsibility_types'),

    path('api/get_responsibility_type/', views.get_responsibility_type, name='get_responsibility_type'),
    path('responsibility_type/', views.responsibility_type, name='responsibility_type'),

    path('termination_reasons/', views.termination_reasons, name='termination_reasons'),
    path('api/get_termination_reason/', views.get_termination_reason, name='get_termination_reason'),
    path('termination_reason/', views.termination_reason, name='termination_reason'),

    #TerminationTypes 
    path('termination_types/', views.termination_types, name='termination_types'),
    path('termination_type/', views.list_termination_types, name='termination_type_list'),
    path('termination_type/create/', views.create_termination_type, name='termination_type_create'),
    path('termination_type/delete/', views.delete_termination_type, name='termination_type_delete'),
    
     #Position Type
    path('position_types/', views.position_types, name='position_types'),
    path('api/positiondata/', views.get_position_data, name='get_position_data'),
    path('create_position/', views.create_position, name='create_position'),
    path('api/delete-position/<int:name>/', views.delete_position_type, name='delete_position'),
    path('api/search_position_type/', views.search_position_type, name='search_position_type'),

    #PaygradesTypes
    path('pay_grades/', views.pay_grades, name='pay_grades'),  # To display the list and search form
    path('api/get-paygrade-data/', views.get_paygrade_data, name='get_paygrade_data'),
    path('api/search-pay-grades/', views.search_pay_grades, name='search_pay_grades'),
    path('api/create-paygrade/', views.create_paygrade, name='create_paygrade'),
    path('api/delete-pay-grade/<str:id>/', views.delete_pay_grade, name='delete_pay_grade'),


       #Employee Leave Type
    path('emp_leave_types/', views.emp_leave_types, name='emp_leave_types'),
    path('create/', views.create_leave_type, name='leave_type_create'),
    path('delete/', views.delete_leave_type, name='leave_type_delete'),
    path('list/', views.list_leave_types, name='leave_type_list'),

     #JobInterviewType
    path('job_interview_types/', views.job_interview_types, name='job_interview_types'),
    path('create_job_interview_type/', views.create_job_interview_type, name='create_job_interview_type'),
    path('delete_job_interview_type/', views.delete_job_interview_type, name='delete_job_interview_type'),
    path('list_job_interview_types/', views.list_job_interview_types, name='list_job_interview_types'),
    
   #TrainingClassType
    path('tranning_class_types/', views.tranning_class_types, name='tranning_class_types'),
    path('create-training-class-type/', views.create_training_class_type, name='create_training_class_type'),
    path('list-training-class-types/', views.list_training_class_types, name='list_training_class_types'),
    path('delete-training-class-type/', views.delete_training_class_type, name='delete_training_class_type'),

  #Public Holiday Type
    path('public_holiday/', views.public_holiday, name='public_holiday'),
    path('create-public-holiday/', views.create_public_holiday, name='create_public_holiday'),
    path('api/list-public-holidays/', views.list_public_holidays, name='list_public_holidays'),
    path('delete-public-holiday/', views.delete_public_holiday, name='delete_public_holiday'),
    
    path('EditPayGrade/', views.EditPayGrade, name='EditPayGrade'),
    
   #EmpLeaveReasonType
    path('EmpLeaveReasonType/', views.EmpLeaveReasonType, name='EmpLeaveReasonType'),
    path('leave_reason_type_create/', views.create_leave_reason_type, name='leave_reason_type_create'),
    path('leave_reason_type_delete/', views.delete_leave_reason_type, name='leave_reason_type_delete'),
    path('leave_reason_type_list/', views.list_leave_reason_types, name='leave_reason_type_list'),
    
    path('Edit_PositionTypes/', views.Edit_PositionTypes, name='Edit_PositionTypes'),
    
    
    
    # gannu hrms
    path('Skills/', views.Skills, name='Skills'),
    path('Qualification/', views.Qualification, name='Qualification'),
    path('newparties/', views.newparties, name='newparties'),
    path('skill_lookupparty/', views.skill_lookupparty, name='skill_lookupparty'),
    path('newpartiesQualifivation/', views.newpartiesQualifivation, name='newpartiesQualifivation'),

    # path('', include(router.urls)),

    path('create-party-skill/', views.create_party_skill, name='create_party_skill'),
    path('Recruitment/', views.Recruitment, name='Recruitment'),
    path('JobRequision/', views.JobRequision, name='JobRequision'),
    path('NewJobRequision/', views.NewJobRequision, name='NewJobRequision'),
    path('Approvals/', views.Approvals, name='Approvals'),
    path('jobInterview/', views.jobInterview, name='jobInterview'),
    path('newInternalJobPosting/', views.newInternalJobPosting, name='newInternalJobPosting'),
    path('NewjobInterview/', views.NewjobInterview, name='NewjobInterview'),
    path('Relocation/', views.Relocation, name='Relocation'),
    
    
    path('TrainingCalender/', views.TrainingCalender, name='TrainingCalender'),
    path('dayView/', views.dayView, name='dayView'),
    path('monthView/', views.monthView, name='monthView'),
    path('upcomingEvent/', views.upcomingEvent, name='upcomingEvent'),
    path('TrainingApproval/', views.TrainingApproval, name='TrainingApproval'),
    path('weekView/', views.weekView, name='weekView'),
    path('CalenderSection/', views.CalenderSection, name='CalenderSection'),
    path('addnewEventMonth/', views.addnewEventMonth, name='addnewEventMonth'),
    path('addnewEvent/', views.addnewEvent, name='addnewEvent'),
    path('lookups/', views.lookups, name='lookups'),
    
    path('search-party-skills/', views.search_party_skills, name='search_party_skills'),

    path('delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),

    path('create-performance-review/', views.create_performance_review, name='create_performance_review'),
    path('find-performance-review/', views.find_performance_review, name='find_performance_review'),

    path('create-employment-application/', views.create_employment_application, name='create_employment_application'),
    path('search-employment-applications/', views.search_employment_applications, name='search_employment_applications'),
    path('delete-employment-application/', views.delete_employment_application, name='delete_employment_application'),

    path('view-training-approvals/', views.view_training_approvals, name='view_training_approvals'),
]