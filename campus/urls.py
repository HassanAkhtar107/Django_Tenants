from django.urls import path
from campus.views import CampusTenantData
from campus import views

urlpatterns = [
    path('', views.project_list, name='campus_list'),
    path('TenantDataList/', CampusTenantData.as_view(), name='campus_list'),
    
]