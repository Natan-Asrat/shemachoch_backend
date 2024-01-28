from django.shortcuts import render
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet
from . import models, serializers, authentication
from django.db.models import Count, Subquery, OuterRef, IntegerField
from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

# Create your views here.
from . import cycle
class DistributeAPI(RetrieveUpdateAPIView, GenericViewSet):
    queryset = models.Shemach.objects.all()
    serializer_class = serializers.DistributeItemSerializer


class MemberAPI(ListAPIView, RetrieveAPIView, CreateAPIView, GenericViewSet):
    authentication_classes = [authentication.FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Shemach.objects.all()
    serializer_class = serializers.MemberSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class OilStock(ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericViewSet):
    queryset = models.Stock.objects.filter(
            item = models.INVENTORY_CHOICES[0][0],
            cycle = cycle.get_cycle()
        )
    serializer_class = serializers.GoodSerializer
    lookup_field = "group"
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = queryset.filter(**filter_kwargs).first()
        return obj
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['unit'] = settings.OIL_UNIT
        context['item'] = 'O'
        return context
    
class SugarStock(ListAPIView, CreateAPIView, UpdateAPIView, GenericViewSet):
    queryset = models.Stock.objects.filter(
        item = models.INVENTORY_CHOICES[1][0],
            cycle = cycle.get_cycle()
    )
    serializer_class = serializers.GoodSerializer
    lookup_field = "group"
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = queryset.filter(**filter_kwargs).first()
        return obj
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['unit'] = settings.SUGAR_UNIT
        context['item'] = 'S'

        return context
    
class AddMemberAPI(CreateAPIView, GenericViewSet):
    queryset = models.Shemach.objects.all()
    serializer_class = serializers.AddMemberSerializer
    authentication_classes = [authentication.FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class GetUser(ListAPIView, GenericViewSet):
    authentication_classes = [authentication.FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Employee.objects.none()
    serializer_class = serializers.EmptySerializer
    def list(self, request):
        user = request.user
        position = "Super Admin" if user.is_superuser else ("Employee" if user.is_staff else "User")
        data = {
            'phoneNumber': user.phoneNumber,
            'name': user.first_name,
            'position': position
        }
        return Response(data)
