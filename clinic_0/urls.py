from django.urls import path
from clinic_0.views import *
from clinic_0 import views


urlpatterns = [
    path('',views.Main_page, name = 'homeclinic'),
    path('Create_Patient/', PatientCreateView.as_view(), name= 'create_patient'),
    path('View_Patients/', All_patients.as_view(),name = 'view_all_class'),
    path('all/',list,name = 'view_all_fun'),
    path('patients/<int:pk>/', PatientListView.as_view(), name= 'view_patient'),

]