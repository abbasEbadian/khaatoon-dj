from django.shortcuts import render
from .models import BusinessType
from state.models import Province
from api.serializers import BusinessTypeSerializer, ProvinceSerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(["GET"])
@authentication_classes([])
def get_all_business_and_province(request):
    bus = BusinessType.objects.all()
    bus = BusinessTypeSerializer(bus, many=True).data
    
    prov = Province.objects.all()
    prov = ProvinceSerializer(prov, many=True).data

    return Response ({
        "business_types": bus,
        "provinces": prov,

    })



