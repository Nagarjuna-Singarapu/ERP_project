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
    path('api/get-employee-data/', views.get_employee_data, name='get_employee_data'),
    path('api/department/', views.get_departments, name='get_departments'),
    path('api/paygrades/', views.PayGradeList.as_view(), name='paygrade-list'),
    path('api/salarysteps/', views.SalaryStepList.as_view(), name='salarystep-list'),
    path('api/terminationtype/', views.TerminationTypeList.as_view(), name='terminationType-list'),
    path('api/terminationreason/', views.TerminationReasonList.as_view(), name='terminationReason-list'),

    path('employment-search/', views.employment_search, name='employment_search'),
    path('api/employment-data/', views.employment_data, name='employment_data'),
    
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
     
    # sunny hrms
    path('Employee_app/', views.Employee_app, name='Employee_app'),
    path('New_emp_app/', views.New_emp_app, name='New_emp_app'),
    path('resume/', views.resume, name='resume'),
    path('leave/', views.leave, name='leave'),
    path('lookupempapp/', views.lookupempapp, name='lookupempapp'),
    path('lookupempposi/', views.lookupempposi, name='lookupempposi'),
    path('lookupparty/', views.lookupparty, name='lookupparty'),
    path('Newresume/', views.Newresume, name='Newresume'),
    path('lookpartyresume/', views.lookpartyresume, name='lookpartyresume'),
    path('addempleave/', views.addempleave, name='addempleave'),
    path('leaveappr/', views.leaveappr, name='leaveappr'),
    
    # gannu hrms
    path('Skills/', views.Skills, name='Skills'),
    path('Qualification/', views.Qualification, name='Qualification'),
    path('newparties/', views.newparties, name='newparties'),
    path('skill_lookupparty/', views.skill_lookupparty, name='skill_lookupparty'),
    path('newpartiesQualifivation/', views.newpartiesQualifivation, name='newpartiesQualifivation'),
]