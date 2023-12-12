from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import Count
from django.utils import timezone
# Create your models here.
class Employee(AbstractUser):
    phoneNumber = models.CharField(max_length=25)
    last_seen = models.DateTimeField(default=timezone.now)
    website = models.TextField(default = "", blank=True)
    REQUIRED_FIELDS = ['phoneNumber']
    def __str__(self) -> str:
        return self.phoneNumber + " " + self.first_name

QUANTITIES_TO_HANDOUT_OIL = [
    (0, 'None'),
    (3, '3 lts'),
    (5, '5 lts')
]
QUANTITIES_TO_HANDOUT_SUGAR = [
    (0, 'None'),
    (3, '3 kg'),
    (5, '5 kg')
]
INVENTORY_CHOICES = [
    ('O', 'Oil'),
    ('S', 'Sugar')
]
INVENTORY_FLOW_CHOICES = [  
    ('I', 'Inflow'),
    ('O', 'Outflow')
]
GROUP_CHOICES = [
    (1, 'Group 1'),
    (2, 'Group 2'),
    (3, 'Group 3'),
    (4, 'Group 4')
]
class Shemach(models.Model):
    name = models.CharField(max_length=50)
    residentId = models.CharField(max_length=20, unique=True)
    date = models.DateField(auto_now_add=True)
    quantityOil = models.DecimalField(decimal_places=2, max_digits=5, default=0, choices=QUANTITIES_TO_HANDOUT_OIL)
    quantitySugar = models.DecimalField(decimal_places=2, max_digits=5, default=0, choices=QUANTITIES_TO_HANDOUT_SUGAR)
    receivesOil = models.BooleanField(default=True)
    receivesSugar = models.BooleanField(default=True)
    hasReceivedOil = models.BooleanField(default=False)
    hasReceivedSugar = models.BooleanField(default=False)
    group = models.IntegerField(choices=GROUP_CHOICES, default=1)

class Stock(models.Model):
    item = models.CharField(choices=INVENTORY_CHOICES, max_length=2)
    distributedQuantity = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    remainingQuantity = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    cycle = models.IntegerField()
    group = models.IntegerField(choices=GROUP_CHOICES, default=1)


class InventoryFlow(models.Model):
    item = models.CharField(choices=INVENTORY_CHOICES, max_length=2)
    flow = models.CharField(choices=INVENTORY_FLOW_CHOICES, max_length=1, default='O')
    flowQuantity = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    remainingQuantity = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    cycle = models.IntegerField()
    group = models.IntegerField(choices=GROUP_CHOICES, default=1)
    employee = models.ForeignKey(to='Employee', on_delete=models.DO_NOTHING)
    employeePhoneNumber = models.CharField(max_length=25)
    shemach = models.ForeignKey(to='Shemach', on_delete=models.DO_NOTHING, null = True, blank=True)
    shemachResidentId = models.CharField(max_length=20, null = True, blank=True)


class BlockChain(models.Model):
    transaction = models.ForeignKey(to='InventoryFlow', on_delete=models.DO_NOTHING)
    data = models.CharField(max_length=128)
    previousHash = models.CharField(max_length=128, blank=True, null=True)
    hash = models.CharField(max_length=128)
