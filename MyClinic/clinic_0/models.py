from django.db import models

# Create your models here.
class Patient(models.Model):
    CATEGORY_CHOICES = (
        ('burn', 'Burn'),
        ('emergency', 'Emergency'),
        ('regular', 'Regular'),
    )
    name = models.CharField(max_length=100,unique=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    age = models.IntegerField()
    date_of_visit = models.DateField()
    follow_up_status = models.BooleanField(default=False)
    examination_or_operation_fees = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name