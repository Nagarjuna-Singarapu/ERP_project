from django.urls import path
from .views import get_countries, get_states
from . import views

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
    path('get-employee/<str:employee_id>/', views.get_employee, name='get_employee'),
    path('api/department/', views.get_departments, name='get_departments'),
    path('api/paygrades/', views.PayGradeList.as_view(), name='paygrade-list'),
    path('api/salarysteps/', views.SalaryStepList.as_view(), name='salarystep-list'),
    path('api/terminationtype/', views.TerminationTypeList.as_view(), name='terminationType-list'),
    path('api/terminationreason/', views.TerminationReasonList.as_view(), name='terminationReason-list'),
    
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
    
    
    # global HR by sunny and amit 
    path('skill_types/', views.skill_types, name='skill_types'),
    path('responsibility_types/', views.responsibility_types, name='responsibility_types'),
    path('termination_reasons/', views.termination_reasons, name='termination_reasons'),
    path('termination_types/', views.termination_types, name='termination_types'),
    path('position_types/', views.position_types, name='position_types'),
    path('emp_leave_types/', views.emp_leave_types, name='emp_leave_types'),
    path('pay_grades/', views.pay_grades, name='pay_grades'),
    path('job_interview_types/', views.job_interview_types, name='job_interview_types'),
    path('tranning_class_types/', views.tranning_class_types, name='tranning_class_types'),
    path('public_holiday/', views.public_holiday, name='public_holiday'),
    path('EditPayGrade/', views.EditPayGrade, name='EditPayGrade'),
    path('EmpLeaveReasonType/', views.EmpLeaveReasonType, name='EmpLeaveReasonType'),
    path('emp_leave_types/', views.emp_leave_types, name='emp_leave_types'),
    path('Edit_PositionTypes/', views.Edit_PositionTypes, name='Edit_PositionTypes'),
    
    
    
    # gannu hrms
    path('Skills/', views.Skills, name='Skills'),
    path('Qualification/', views.Qualification, name='Qualification'),
    path('newparties/', views.newparties, name='newparties'),
    path('skill_lookupparty/', views.skill_lookupparty, name='skill_lookupparty'),
    path('newpartiesQualifivation/', views.newpartiesQualifivation, name='newpartiesQualifivation'),
    
    
    
    path('TrainingCalender/', views.TrainingCalender, name='TrainingCalender'),
    path('dayView/', views.dayView, name='dayView'),
    path('monthView/', views.monthView, name='monthView'),
    path('upcomingEvent/', views.upcomingEvent, name='upcomingEvent'),
    path('TrainingApproval/', views.TrainingApproval, name='TrainingApproval'),
    path('weekView/', views.weekView, name='weekView'),
    path('CalenderSection/', views.CalenderSection, name='CalenderSection'),
    path('addnewEventMonth/', views.addnewEventMonth, name='addnewEventMonth'),
    path('addnewEvent/', views.addnewEvent, name='addnewEvent'),
    path('nagaslookup/', views.nagaslookup, name='nagaslookup'),
    
]