from django.shortcuts import render
from .models import WebsiteConfiguration
from api.serializers import WebsiteConfigurationSerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


@api_view(["GET"])
@authentication_classes([])
def get_all_configs(request):
    website = WebsiteConfigurationSerializer(WebsiteConfiguration.objects.get(), many=False).data

    return Response({
        "website": website
    })
