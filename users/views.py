from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import UserSerializer
from state.models import Province
from wallet.models import Wallet
from django.contrib.auth import get_user_model, authenticate as check_auth
User = get_user_model()

@api_view(["POST"])
@authentication_classes([])
def authenticate(request):
    mobile = request.data.get('mobile', None)
    password = request.data.get('password', None)

    if not mobile or not password:
        return Response({
            "error": 1,
            "message": "اطلاعات را به صورت کامل وارد کنید." 
        })
    
    user, created = User.objects.get_or_create(username=mobile)

    if created:
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response ({
            "error" : 0,
            "action": "register",
            "token": str(refresh.access_token),
            "message": "حساب کاربری شما با موفقیت ایجاد شد."
        })

    
    user = check_auth(username=mobile, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response ({
            "error" : 0,
            "action": "login",
            "token": str(refresh.access_token),
            "message": "با موفقیت وارد شدید"
        })
    return Response ({
        "error" : 1,
        "message": "رمز عبور نادرست است."
    })


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def profile(request):
    if request.method == "GET":
        if request.auth:
            Wallet.objects.get_or_create(user_id=request.user)
            user = UserSerializer(request.user, many=False)
            user = user.data
        else:
            user = {}
        return Response(user)
    elif request.method == "POST":
        try:
            name = request.data.get('first_name', "")
            email = request.data.get('email', "")
            mobile = request.data.get('mobile', "")
            province = request.data.get('province', "")
            if request.auth:
                request.user.first_name = name
                request.user.email = email
                request.user.mobile = mobile
                request.user.province_id = Province.objects.get(pk=int(province))
                Wallet.objects.get_or_create(user_id=request.user)
                request.user.save()
            else: 
                raise Exception("Not Authenticated")
        except Exception as e:
            return Response ({"error": 1, "message": "خطا در ثبت", "extra": str(e)})
        else:
            return Response ({"error": 0, "message": "با موفقیت ثبت شد."})

        

