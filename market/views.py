from django.shortcuts import render

from market.forms import coveruploadform, imageuploadform
from .models import BusinessType, Market, Bank
from state.models import Province, City
from api.serializers import BusinessTypeSerializer, MarketSerializer, ProvinceSerializer, BankSerializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(["GET"])
@authentication_classes([])
def get_all_banks(request):
   
    prov = Bank.objects.all()
    prov = BankSerializer(prov, many=True).data

    return Response (prov)

@api_view(["GET"])
@authentication_classes([])
def get_market_by_user_name(request, username):
   
    prov = Market.objects.filter(username=username).first()
    prov = MarketSerializer(prov, many=False).data

    return Response (prov)


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

    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def upload_cover_image(request):
    if not request.auth:
        return Response({
            "error": "1",
            "message": "لطفا ابتدا وارد شوید",
            "type": "error"
        })
    
    if request.method == "POST":
        if request.user.authentication_status == "authorized":
            return Response({"error": 1, "message":  "امکان تغییر تصویر بعد از احراز هویت وجود ندارد.", "type": "warning"})
        form = coveruploadform(request.POST, request.FILES)
        if form.is_valid():
            request.user.market.cover=request.FILES['image']
            request.user.market.save()
            return Response({"error": 0, "message": "با موفقیت اپلود شد"})
    return Response({"error": 1, "message": "خطا در آپلود"})
    

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def upload_avatar_image(request):
    if not request.auth:
        return Response({
            "error": "1",
            "message": "لطفا ابتدا وارد شوید",
            "type": "error"
        })
    
    if request.method == "POST":
        if request.user.authentication_status == "authorized":
            return Response({"error": 1, "message":  "امکان تغییر تصویر بعد از احراز هویت وجود ندارد.", "type": "warning"})
        form = imageuploadform(request.POST, request.FILES)
        if form.is_valid():
            request.user.market.image=request.FILES['image']
            request.user.market.save()
            return Response({"error": 0, "message": "با موفقیت اپلود شد"})
    return Response({"error": 1, "message": "خطا در آپلود"})

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def update_market_document(request):
   
    if request.method == "POST":
        if request.user.authentication_status == "authorized":
            return Response({"error": 1, "message":  "امکان تغییر تصویر بعد از احراز هویت وجود ندارد.", "type": "warning"})
        request.user.market.document = request.FILES['image']
        request.user.market.save()
        return Response({"error": 0, "message": "با موفقیت اپلود شد"})
    return Response({"error": 1, "message": "خطا در آپلود"})



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def update_market_detail(request):
    try:
        
        name  = request.data.get('name', 0)
        message  = request.data.get('message', 0)
        username  = request.data.get('username', 0)
        businesstype_id  = request.data.get('businesstype_id', 0)
        about  = request.data.get('about', 0)
        mobile  = request.data.get('mobile', 0)
        phone  = request.data.get('phone', 0)
        province  = request.data.get('province', 0)
        city  = request.data.get('city', 0)
        address  = request.data.get('address', 0)
        instagram_address  = request.data.get('instagram_address', "")
        website_address  = request.data.get('website_address', "")
        telegram_address = request.data.get('telegram_address', "")
        same = Market.objects.filter(username=username)
        Market.objects.get_or_create(user=request.user, defaults={"name":name, "message":message, "username":username} )

        if same and not (same.count() == 1 and same.first() == request.user.market):
            return Response ({"error":1, "message": "غرفه ای با این ادرس قبلا ثبت شده است"})
        business = BusinessType.objects.get(pk=int(businesstype_id))
        province = Province.objects.filter(name = province)
        city = City.objects.filter(name = city)
        data = {
            "name":name,
            "message":message,
            "username":username,
            "business_type":business,
            "about":about,
            "mobile":mobile,
            "phone":phone,
            "address":address,
            "instagram_address": instagram_address,
            "website_address": website_address,
            "telegram_address": telegram_address,
        }
        if not any([name, message, username, businesstype_id, about, mobile, phone]):
            return Response ({"error": 1, "message" : "اطلاعات ناقص"})
        
        for key in data.keys():
            setattr(request.user.market, key, data[key])
        
        request.user.market.save()

        
        return Response ({"error":0, "message": "با موفقیت ثبت شد"})
    except Exception as e:
        print(e)
        return Response ({"error": 1, "message": str(e)})


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def update_market_detail_bank(request):
    try:
        bank  = request.data.get('bank', 0)
        national_code  = request.data.get('national_code', 0)
        shaba  = request.data.get('shaba', 0)
        card_number  = request.data.get('card_number', 0)
        if not any([bank, national_code, shaba, card_number]):
            return Response ({"error": 1, "message" : "اطلاعات ناقص"})

        bank = Bank.objects.get(id=int(bank))
        # if not bank:
        #     return Response ({"error":1, "message": "غرفه ای با این ادرس قبلا ثبت شده است"})
        
        data = {
            "national_code":national_code,
            "shaba":shaba,
            "card_number":card_number,
        }
        if bank: data["bank"] = bank
        
        for key in data.keys():
            setattr(request.user.market, key, data[key])
        
        request.user.market.save()

        
        return Response ({"error":0, "message": "با موفقیت ثبت شد"})
    except Exception as e:
        print(e)
        return Response ({"error": 1, "message": str(e)})
        