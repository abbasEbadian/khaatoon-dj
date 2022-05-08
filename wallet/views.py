from .models import Wallet, Transaction
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication 
User = get_user_model()


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
# Create your views here.
def create_address(request):
    return Response({})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
# Create your views here.
def edit(request):

    return Response({})