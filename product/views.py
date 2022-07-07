from django.shortcuts import render

from attribute.models import Attribute, AttributeValue, ProductAttribute
from .models import Product
from market.models import Market
from category.models import Category
from api.serializers import MarketSerializer, ProductSerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q
import json
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

@api_view(["POST"])
@authentication_classes([])
def search_with_name(request):
    try:
        name=request.data.get('name', "")
        products = Product.objects.filter(name__icontains=name)
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
def get_index_products(request):
    try:
        products = Product.objects.all().order_by("-id")
        return Response ({
            "timerSliderProducts": ProductSerializer(products, many=True).data[:6],
            "newProducts": ProductSerializer(products, many=True).data[:12],
            "suggestSliderProducts": ProductSerializer(products, many=True).data[:10],
            "magicSliderProducts": ProductSerializer(products, many=True).data[:6],
            "markets": MarketSerializer(Market.objects.all(), many=True).data[:15],
        })
    except Exception as e:
        print(e)
        return Response ({})


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


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def update_visibility(request):
    try:
        pk = request.data.get('pk', 0)
        visible = request.data.get('visible', False)
        product = Product.objects.get(pk=pk)
        if product.market_id.user != request.user:
            return Response ({"error": 1, "message": "این محصول متعلق به شما نیست."})

        if product.status != "confirmed" and visible:
            return Response ({"error": 1, "message": "محصول هنوز تایید نشده است."})
        
        product.published = visible
        product.save() 
    
        return Response ({"error": 0, "message": "ثبت شد"})
    except Exception as e:
        print(e)
        return Response ({"error": 1, "message": "خطا در ثبت"})


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        if product.market_id.user != request.user:
            return Response ({"error": 1, "message": "این محصول متعلق به شما نیست."})
  
        product.delete() 
    
        return Response ({"error": 0, "message": "با موفقیت حذف شد."})
    except Exception as e:
        print(e)
        return Response ({"error": 1, "message": "خطا در ثبت"})
        

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def create_product(request):
    try:
        print(request.data)
        # print(request.POST)
        name = request.data.get('name', 0)
        description = request.data.get('description', 0)
        price = max(int(request.data.get('price', 0)), 1)
        preperation_time = max(1, int(request.data.get('preperation_time', 1)))
        count = max(int(request.data.get('count', 0)), 0)
        category_id = request.data.get('category_id', 0)
        image = request.data.get('image', 0)
        image1 = request.data.get('image1', 0)
        image2 = request.data.get('image2', 0)
        image3 = request.data.get('image3', 0)
        image4 = request.data.get('image4', 0)
        extra_description = request.data.get('extra_description', "")
        attributes = request.data.get('attributes', 0)
        variants = request.data.get('variants', 0)
        combinations = request.data.get('combinationData', {})
        
        if not any([name, description, price, preperation_time, count, category_id, image]):
            return Response ({"error": 1, "message" : "اطلاعات ناقص"})
        cat = Category.objects.filter(persian_name=category_id)
        cat = cat and cat[0]
        
        if request.user.market.product_set.filter(name=name):
            return Response ({"error":1, "message": "محصولی با این نام، قبلا در غرفه شما ثبت شده است "})

        data = {
            "name":name,
            "description":description,
            "extra_description": extra_description,
            "price":price,
            "preperation_time":preperation_time,
            "count":count,
            "category_id":cat,
            "image":image,
            "market_id":request.user.market        
        }   

        product = Product.objects.create(**data)
        if image1 and image1 != "undefined": product.image_1 = image1
        if image2 and image2 != "undefined": product.image_2 = image2
        if image3 and image3 != "undefined": product.image_3 = image3
        if image4 and image4 != "undefined": product.image_4 = image4
        attributes = json.loads(attributes)
        for attribute in attributes:
            attr, c = Attribute.objects.get_or_create(name=attribute["attribute"])
            value, vc = AttributeValue.objects.get_or_create(name=attribute["attributeValue"], defaults={"attribute_id": attr})
            product.productattribute_set.create(attribute_id=attr, value_id=value)
       
        combinations = json.loads(combinations) or {}
        # return Response({})
        for value_names, data in combinations.items():
            variant = product.producttemplate_set.create(count=int(data["count"]), price=int(data["price"]))
            for value_name, attr_name in zip(value_names.split("-"), data["attribute"].split("-")):
                attr, c = Attribute.objects.get_or_create(name=attr_name)
                value, vc = AttributeValue.objects.get_or_create(name=value_name, defaults={"attribute_id": attr})
                variant.productattribute_set.create(attribute_id=attr, value_id=value, key=value_names+"__"+data["attribute"])
                
            variant.save()
        
        if not combinations:
            variant = product.producttemplate_set.create(price=price, count=count, default=True)
            

        product.save()
        

        return Response ({"error":0, "message": "محصول با موفقیت ایجاد گردید و پس از تایید کارشناسان ، قابل نمایش خواهد بود."})
    except Exception as e:
        print(e)
        return Response ({"error": 1, "message": str(e)})
        

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def update_product(request):
    try:
        pk = int(request.data.get('pk', 0))
        name = request.data.get('name', 0)
        description = request.data.get('description', 0)
        price = max(int(request.data.get('price', 0)), 1)
        preperation_time = max(1, int(request.data.get('preperation_time', 1)))
        count = int(request.data.get('count', -1))
        category_id = request.data.get('category_id', 0)
        image = request.data.get('image', 0)
        image1 = request.data.get('image1', 0)
        image2 = request.data.get('image2', 0)
        image3 = request.data.get('image3', 0)
        image4 = request.data.get('image4', 0)
        extra_description = request.data.get('extra_description', "")
        attributes = request.data.get('attributes', 0)
        combinations = request.data.get('combinationData', {})
        
        
        cat = Category.objects.filter(persian_name=category_id)
        cat = cat and cat[0]
        _product = Product.objects.filter(pk=pk)
        product = _product[0]
        similar = request.user.market.product_set.filter(name=name).exclude(pk=pk)
        if  similar :
            return Response ({"error":1, "message": "محصولی با این نام، قبلا در غرفه شما ثبت شده است "})
        if  not product :
            return Response ({"error":1, "message": "محصول یافت نشد "})

        data = {
            "name":name,
            "description":description,
            "extra_description": extra_description,
            "price":price,
            "preperation_time":preperation_time,
            "count":count,
            "category_id":cat,
        }   
        images = [image, image1, image2, image3, image4]
        extra = ""
        if any(images) and product.status == 'confirmed':
            extra = "امکان تغییر تصویر بعد از تایید محصول وجود ندارد."
        else:
            if image  and image  != "undefined": product.image = image
            if image1 and image1 != "undefined": product.image_1 = image1
            if image2 and image2 != "undefined": product.image_2 = image2
            if image3 and image3 != "undefined": product.image_3 = image3
            if image4 and image4 != "undefined": product.image_4 = image4

        _product.update(**data)
        attributes = json.loads(attributes)
        
        product.productattribute_set.all().delete()
        for attribute in attributes:
            attr, c = Attribute.objects.get_or_create(name=attribute["attribute"])
            value, vc = AttributeValue.objects.get_or_create(name=attribute["attributeValue"], defaults={"attribute_id": attr})
            product.productattribute_set.create(attribute_id=attr, value_id=value)
       
        combinations = json.loads(combinations) or {}
        changed_combinations = []
        for value_names, data in combinations.items():
            product_attr = ProductAttribute.objects.filter(product_template_id__product_id=product, key=value_names+"__"+data["attribute"]).first()
            variant = product_attr and product_attr.product_template_id
            if not variant:
                variant = product.producttemplate_set.create()
                for value_name, attr_name in zip(value_names.split("-"), data["attribute"].split("-")):
                    attr, c = Attribute.objects.get_or_create(name=attr_name)
                    value, vc = AttributeValue.objects.get_or_create(name=value_name, defaults={"attribute_id": attr})
                    variant.productattribute_set.create(attribute_id=attr, value_id=value)
                
            variant.count = int(data["count"])
            variant.price = int(data["price"])
            variant.save()
            changed_combinations.append(variant)
        
        for v in product.producttemplate_set.iterator():
            if v not in changed_combinations:
                v.delete()

        if not combinations:
            for v in product.producttemplate_set.iterator():
                if v not in changed_combinations:
                   v.delete()
                   
            variant, c = product.producttemplate_set.get_or_create(default=True)
            product.count = count
            product.price = price
            variant.count = count
            variant.price = price
            variant.save()

        product.save()
        

        return Response ({"error":0, "message": "محصول با موفقیت بروز شد", "extra": extra})
    except Exception as e:
        print(e)
        return Response ({"error": 1, "message": str(e)})
        