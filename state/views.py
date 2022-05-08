from .models import Province,City
from product.models import Product
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from api.serializers import ProvinceSerializer, CitySerializer

from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
@authentication_classes([])
def get_province_all(request):
    p = ProvinceSerializer(Province.objects.all(), many=True).data
    return Response(p)


@api_view(['GET'])
@authentication_classes([])
def get_cities_by_province(request, pk):
    try:
        p = CitySerializer(City.objects.filter(province_id=pk), many=True).data
        return Response(p)
    except:
        return Response([])
        
        