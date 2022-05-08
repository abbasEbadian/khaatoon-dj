from django.shortcuts import render
from .models import Product
from category.models import Category
from api.serializers import ProductSerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


@api_view(["GET"])
@authentication_classes([])
def get_all_products(request):
    try:
        products = Product.objects.all()
        products = ProductSerializer(products, many=True).data

        products_length = len(products)
        return Response ({"products": products, "products_length": products_length})

    except Exception as e:
        print(e)
        return Response ([])

@api_view(["GET"])
@authentication_classes([])
def get_products_by_category_id(request, pk):
    try:
        category = Category.objects.get(pk=pk) 
        products = Product.objects.filter(Q(category_id=category.id) | Q(category_id=category.parent_id.id) | Q(category_id=category.parent_id.parent_id.id))
        products = ProductSerializer(products, many=True)
        print(products)
        return Response (products.data)
    except Exception as e:
        print(e)
        return Response ([])


@api_view(["GET"])
@authentication_classes([])
def get_product_by_id(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product = ProductSerializer(product, many=False).data
        return Response ({"product": product, "similar_products": []})
    except Exception as e:
        print(e)
        return Response ({"product": {}, "similar_products": []})
        