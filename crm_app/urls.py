# CRM_APP/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.contrib.auth import views as authentication_views


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('signup-success/', views.signup_success, name='signup_success'),
    
    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('PerDeshbord/', views.PerDeshbord, name='PerDeshbord'),
    path('improvement/', views.improvement, name='improvement'),
    path('company/', views.company, name='company'),
    path('Employee/', views.Employee, name='Employee'),
    path('report/', views.report, name='report'),
    path('review/', views.review, name='review'),
    path('viewreport/', views.viewreport, name='viewreport'),
    
    
    
    
 
    path("password_reset/", authentication_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_done/", authentication_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", authentication_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", authentication_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)