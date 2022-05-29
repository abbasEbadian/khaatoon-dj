from django.shortcuts import render
from .models import Category
from api.serializers import CategorySerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(["GET"])
@authentication_classes([])
def get_all_categories(request):
    cats = Category.objects.filter(parent_id__isnull=True)
    cats2 = Category.objects.all()
    cats = CategorySerializer(cats, many=True).data
    cats2 = CategorySerializer(cats2, many=True).data

    return Response ({"categories": cats, "flat_categories": cats2})



