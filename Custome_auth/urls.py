from django.urls import path ,include
from django.contrib.auth.views import *
from Custome_auth import views
from Custome_auth.views import *

urlpatterns =[
    path('login/',LoginView.as_view(),name='baselogin'),
    path('',views.home,name='home'),
    path('logout/',customeLogout,name='baselogout'),
    path('Good-bye/',views.bye,name='Goodbye'),
    path('home/',views.welcome,name = 'welcome'),
    path('register/',views.register_request,name='registerpage'),
    path('form/',test_form12.as_view(), name= 'oo'),
    path('password-reset/', PasswordResetView.as_view(),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]