from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from .models import *
from .serializer import *

from rest_framework import status, viewsets, generics
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User,Group
from django.core.paginator import EmptyPage, Paginator
from django.views.generic.base import TemplateView 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.contrib import messages
from rest_framework.generics import ListCreateAPIView
from datetime import datetime
from django.db.models import Sum

@login_required()
def Main_page(request):
    return render(request, 'main.html')

class PatientCreateView(LoginRequiredMixin,CreateView):
    model = Patient
    fields = ['name', 'address', 'phone_number', 'category', 'age', 'date_of_visit', 'follow_up_status', 'examination_or_operation_fees']
    template_name = 'create_patient.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Patient {} was created successfully.'.format(form.cleaned_data['name']))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'There was an error creating the patient. Try again . Patient name must be Unique')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('create_patient')

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    fields = ['name', 'address', 'phone_number', 'category', 'age', 'date_of_visit', 'follow_up_status', 'examination_or_operation_fees']
    template_name = 'list_confirm_patient.html'
    def get_success_url(self):
        return reverse('homeclinic')
    
class All_patients( ListCreateAPIView):
    queryset  = Patient.objects.all()
    serializer_class = patientSerializer
    permission_classes = [IsAdminUser]

@login_required()
def list(request):

    queryset = Patient.objects.all()
    totalnum = queryset.count()
    name_query  = request.GET.get('name')
    date_query = request.GET.get('date')
    category_query = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if name_query:
        queryset = queryset.filter(name__icontains=name_query)
    if str(name_query).lower() == 'all':
        queryset = Patient.objects.all()
    if date_query:
        queryset = queryset.filter(date_of_visit=date_query)
    if category_query:
        queryset = queryset.filter(category__icontains=category_query)
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        queryset = queryset.filter(date_of_visit__range=[start_date, end_date])

    serializer = patientSerializer(queryset, many=True)
    total_fees = queryset.aggregate(Sum('examination_or_operation_fees'))['examination_or_operation_fees__sum']
    total_count = queryset.count()
    if totalnum != total_count:
        context = {
            'patients': serializer.data,
            'total_fees': total_fees,
            'total_count': total_count,
        }
    elif str(name_query).lower() == 'all' and request.user.is_superuser:
        context = {
            'patients': serializer.data,
            'total_fees': total_fees,
            'total_count': total_count,
        }
    else:
        context = {
            'patients': '',
            'total_fees': 0,
            'total_count': 0,
        }
    return render(request,'view_all_patients.html',context)
    