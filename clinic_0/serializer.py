from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class patientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'