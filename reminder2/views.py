from .models import Favorite
from product.models import Product
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication 
User = get_user_model()


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def toggle(request):
    if not request.data.get("product_id", None):
        return Response({"error": 1, "message": "اطلاعات ناقص", "status": 401})

    if not request.auth:
        return Response({"error": 1, "message": "وارد حساب شوید", "status": 401})

    try:
        product = Product.objects.get(pk=request.data.get("product_id"))
    except Exception as e:
        return Response({"error": 1, "created": c, "message": "محصول یافت نشد."})

    f, c= Reminder.objects.get_or_create(user_id=request.user, product_id=product)
    if not c:
        f.delete()
    return Response({"error": 0, "created": c, "message": "ثبت شد."})