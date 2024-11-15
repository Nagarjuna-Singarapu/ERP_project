"""shanaya_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.dashboard, name='dashboard')
Class-based views
    1. Add an import:  from other_app.views import dashboard
    2. Add a URL to urlpatterns:  path('', dashboard.as_view(), name='dashboard')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ERP_project/shanaya_crm/urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm_app.urls')),
    path('hrms/', include('crm_app.HRMS.urls')),
]
