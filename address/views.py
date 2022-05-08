from .models import Address
from state.models import Province, City
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication 
User = get_user_model()



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_address(request):
    try:
        province_id = request.data.get('province_id', 0)
        city_id = request.data.get('city_id', 0)
        address = request.data.get('address', 0)
        mobile = request.data.get('mobile', 0)
        phone = request.data.get('phone', 0)
        postal = request.data.get('postal', 0)
        create = request.data.get('create', 1)
        address_id = request.data.get('id', 0)

        if not any([province_id, city_id, address, mobile, phone, postal]):
            return Response({"error": 1, "message": "اطلاعات ناقص"})
        province_id = Province.objects.get(pk=province_id)
        city_id = City.objects.get(pk=city_id)
        if create:
            address, created = Address.objects.get_or_create(user_id=request.user, address=address, city_id=city_id, province_id=province_id, mobile=mobile, phone=phone, postal=postal)
            if not request.user.address_set.filter(active=True):
                f = request.user.address_set.first()
                f.active = True
                f.save()
        
            if created:
                return Response({"error": 0, "message": "آدرس با موفقیت ثبت شد"})
            return Response({"error": 1, "message": "آدرس با این اطلاعات از قبل موجود است."})
        
        else :
            if not address_id:
                return Response({"error": 1, "message": "آدرس یافت نشد."})
            
            _address = Address.objects.get(pk=int(address_id))
            _address.province_id = province_id
            _address.city_id = city_id
            _address.address = address
            _address.mobile = mobile
            _address.phone = phone
            _address.postal = postal

            _address.save()
            return Response({"error": 0, "message": "آدرس با موفقیت تغییر یافت"})

    except Exception as e:
        
        return Response({"error": 1, "message": "خطا در ثبت", "extra": str(e)})



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def edit_address(request):
    address_id = request.data.get('address_id', 0)
    province_id = request.data.get('province_id', 0)
    city_id = request.data.get('city_id', 0)
    address = request.data.get('address', 0)
    mobile = request.data.get('mobile', 0)
    phone = request.data.get('phone', 0)
    postal = request.data.get('postal', 0)


    return Response({})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def change_active(request, pk):
    try:
        for a in request.user.address_set.all():
            a.active = a.id == pk
            a.save()
        return Response({"error": 0, "message": "آدرس پیشفرض با موفقیت تغییر یافت"})
    except Exception as e:
        return Response({"error": 1, "message": "خطا در ثبت", "extra": str(e)})

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete(request, pk):
    try:
        a = request.user.address_set.get(pk=pk)
        a.delete()
        return Response({"error": 0, "message": "آدرس  با موفقیت حذف شد "})
    except Exception as e:
        return Response({"error": 1, "message": "خطا در ثبت", "extra": str(e)})



