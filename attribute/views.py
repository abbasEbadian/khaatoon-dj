from .models import Attribute, AttributeValue
from product.models import Product
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from api.serializers import AttributeSerializer, AttributeValueSerializer, ProvinceSerializer, CitySerializer

from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
@authentication_classes([])
def get_all_attributes(request):
    attributes = AttributeSerializer(Attribute.objects.all(), many=True).data
    attributeValues = AttributeValueSerializer(AttributeValue.objects.all(), many=True).data
    return Response({
        "attributes": attributes,
        "attributeValues": attributeValues,
    })

