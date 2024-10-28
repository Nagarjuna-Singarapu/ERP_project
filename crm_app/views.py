# CRM_APP/views.py
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from .models import UserSignup, Profile
from .forms import PasswordResetForm, SetNewPasswordForm
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from django.contrib import messages
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Create form instance with POST data
        if form.is_valid():  # Check if the form is valid
            user = form.save()  # Save the user to the database
            UserSignup.objects.create(user=user)  # Create a token for the user
            Profile.objects.create(user=user)
            success_message = "Successfully signed up! Please log in."
            return render(request, 'signup.html', {'form': SignupForm(), 'success_message': success_message})  # Show success message

        else:
            error_messages = form.errors.as_data()  # Get error messages
            return render(request, 'signup.html', {'form': form, 'error_messages': error_messages})  # Show error messages

    form = SignupForm()  # Create an empty form instance for GET request
    return render(request, 'signup.html', {'form': form})  # Render the signup page

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Retrieve the user based on the provided email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email')
                return redirect('login')

            # Authenticate using the retrieved user object
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    from_email = 'aapaitest@gmail.com'


@login_required
def dashboard_view(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # Handle the case where no profile exists
    
    return render(request, 'dashboard.html', {'profile': profile})

def signup_success(request):
    return render(request, 'signup_success.html')

@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)  # Fetch the profile
    except Profile.DoesNotExist:
        return redirect('signup')  # Redirect to signup or create a profile

    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.bio = request.POST.get('bio')
        profile.phone_number = request.POST.get('phone_number')
        profile.date_of_birth = request.POST.get('date_of_birth')  # Handle date of birth
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')
        profile.save()
        return redirect('profile')  # Redirect to the profile view after saving

    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def profiles(request):
    return render(request, 'profile.html')

def viewprofile(request):
    return render(request, 'viewprofile.html')

def profileicon(request):
    return render(request, 'profileicon.html')

def PerDeshbord(request):
    return render(request, 'Performance/PerDeshbord.html')

def improvement(request):
    return render(request, 'Performance/improvement.html')

def company(request):
    return render(request, 'Performance/company.html')

def Employee(request):
    return render(request, 'Performance/Employee.html')

def report(request):
    return render(request, 'Performance/report.html')

def review(request):
    return render(request, 'Performance/review.html')

def viewreport(request):
    return render(request, 'Performance/viewreport.html')
    
def forecasting(request):
    return render(request, 'forecasting/forecasting.html')



# anuj
def emp_main(request):
    return render(request, 'hrms/emp_per/emp_main.html')

def Employment(request):
    return render(request, 'hrms/emp_per/Employement.html')

def Employe_position(request):
    return render(request, 'hrms/emp_per/Employe_position.html')

def NewEmploye(request):
    return render(request, 'hrms/emp_per/NewEmploye.html')

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








