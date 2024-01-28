from . import models, cycle
from rest_framework import serializers
from django.db.models import Sum
from datetime import timedelta
from django.conf import settings
from decimal import Decimal

EXPIRES_IN = settings.EXPIRES_IN
    
class EmptySerializer(serializers.Serializer):
    pass
class DistributeItemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    quantityOil = serializers.ReadOnlyField()
    quantitySugar = serializers.ReadOnlyField()
    receivesOil = serializers.ReadOnlyField()
    receivesSugar = serializers.ReadOnlyField()
    class Meta:
        model = models.Shemach
        fields = [
            'id',
            'name',
            'quantityOil',
            'quantitySugar',
            'receivesOil',
            'receivesSugar',
            'hasReceivedOil',
            'hasReceivedSugar'
        ]

class MemberSerializer(serializers.ModelSerializer):
    expiry = serializers.SerializerMethodField()
    class Meta:
        model = models.Shemach
        fields = [
            'id',
            'name',
            'residentId',
            'date',
            'expiry',
            'quantityOil',
            'quantitySugar',
            'receivesOil',
            'receivesSugar',
            'hasReceivedOil',
            'hasReceivedSugar',
            'group'
        ]
    def get_expiry(self, obj):
        registration = obj.date
        expiry = registration + timedelta(days = EXPIRES_IN)
        return expiry

class GoodSerializer(serializers.ModelSerializer):
    group = serializers.ChoiceField(choices=models.GROUP_CHOICES, source='get_group_display', read_only=True)
    item = serializers.ChoiceField(choices=models.INVENTORY_CHOICES, source='get_item_display', read_only=True)
    received_members = serializers.SerializerMethodField(read_only=True)
    total_stock = serializers.SerializerMethodField(read_only=True)
    total_members = serializers.SerializerMethodField(read_only=True)
    required_stock = serializers.SerializerMethodField(read_only=True)
    remaining_stock = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Stock
        fields = [
            'item',
            'group',
            'remaining_stock',
            'received_members',
            'total_members',
            'required_stock',
            'total_stock'
        ]
    def get_remaining_stock(self, obj):
        group = obj.group
        sum = None
        if(obj.item == models.INVENTORY_CHOICES[0][0]):
            sum = models.Shemach.objects.filter(group = group, receivesOil=True, hasReceivedOil = True).aggregate(s=Sum('quantityOil'))['s']
        if(obj.item == models.INVENTORY_CHOICES[1][0]):
            sum = models.Shemach.objects.filter(group = group, receivesSugar=True, hasReceivedSugar = True).aggregate(s=Sum('quantitySugar'))['s']
        if(sum is not None):
            return obj.remainingQuantity - sum
        return 0
    def get_total_stock(self, obj):
        group = obj.group
        sum = None
        if(obj.item == models.INVENTORY_CHOICES[0][0]):
            sum = models.Shemach.objects.filter(group = group, receivesOil=True, hasReceivedOil = True).aggregate(s=Sum('quantityOil'))['s']
        if(obj.item == models.INVENTORY_CHOICES[1][0]):
            sum = models.Shemach.objects.filter(group = group, receivesSugar=True, hasReceivedSugar = True).aggregate(s=Sum('quantitySugar'))['s']
        if(sum is not None):
            sum += obj.remainingQuantity
            return sum
        return 0

    def get_total_members(self, obj):
        group = obj.group
        count = None
        if(obj.item == models.INVENTORY_CHOICES[0][0]):
            count = models.Shemach.objects.filter(group = group, receivesOil=True).count()
        if(obj.item == models.INVENTORY_CHOICES[1][0]):
            count = models.Shemach.objects.filter(group = group, receivesSugar=True).count()
        if(count is not None):
            return count
        return 0
    def get_received_members(self, obj):
        group = obj.group
        count = None
        if(obj.item == models.INVENTORY_CHOICES[0][0]):
            count = models.Shemach.objects.filter(group = group, receivesOil=True, hasReceivedOil = True).count()
        if(obj.item == models.INVENTORY_CHOICES[1][0]):
            count = models.Shemach.objects.filter(group = group, receivesSugar=True, hasReceivedSugar = True).count()
        if(count is not None):
            return count
        return 0
    def get_required_stock(self, obj):
        # group = obj.group
        # sum = None
        # if(obj.item == models.INVENTORY_CHOICES[0][0]):
        #     sum = models.Shemach.objects.filter(group = group, receivesOil=True, hasReceivedOil = False).aggregate(s=Sum('quantityOil'))['s']
        # if(obj.item == models.INVENTORY_CHOICES[1][0]):
        #     sum = models.Shemach.objects.filter(group = group, receivesSugar=True, hasReceivedSugar = False).aggregate(s=Sum('quantitySugar'))['s']
        # if(sum is not None):
        #     return sum
        # return 0
        return obj.remainingQuantity
    def to_representation(self, instance):
        data = super().to_representation(instance)
        stock = data.pop('remaining_stock')
        data['stock'] = stock + ' ' + self.context.get('unit')
        return data
    def create(self, validated_data):
        validated_data['cycle'] = cycle.get_cycle()
        validated_data['item'] = self.context.get('item')
        print(validated_data)
        instance, created = models.Stock.objects.get_or_create(**validated_data)
        return instance


class AddMemberSerializer(serializers.ModelSerializer):
    quantityOil = serializers.DecimalField(decimal_places=2, max_digits=5, required= False)
    quantitySugar = serializers.DecimalField(decimal_places=2, max_digits=5, required= False)
    receivesOil = serializers.BooleanField(required=False)
    receivesSugar = serializers.BooleanField(required=False)
    hasReceivedOil = serializers.ReadOnlyField()
    hasReceivedSugar = serializers.ReadOnlyField()
    CURRENT_GROUP = 1
    class Meta:
        model = models.Shemach
        fields = '__all__'
    def to_internal_value(self, d):
        data = d.copy()
        qOil = data['quantityOil']
        qSugar = data['quantitySugar']
        CURRENT_GROUP = getattr(AddMemberSerializer, 'CURRENT_GROUP', 1)
        data['group'] = CURRENT_GROUP
        setattr(AddMemberSerializer, 'CURRENT_GROUP', CURRENT_GROUP + 1 if CURRENT_GROUP < 4 else 1)        
        if qOil is None or qOil.startswith('0') or qOil == '':
            data['receivesOil'] = False
        else:
           data['receivesOil'] = True 
        if qSugar is None or qSugar.startswith('0') or qSugar == '':
            print(qSugar)
            data['receivesSugar'] = False
        else:
           data['receivesSugar'] = True 
        return super().to_internal_value(data)
