from django.shortcuts import get_object_or_404
from .models import Order, OrderLine, Discount
from product.models import Product, ProductTemplate
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import OrderSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_basket(request):
    if request.auth:
        o, c = Order.objects.get_or_create(user_id=request.user, status="draft")
        serializer = OrderSerializer(o, many=False)

        return Response(serializer.data)
    return Response([])
    
import uuid, random, string
def generate_fake_card(template):
    uid = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))
    pin = uuid.uuid4()
    return Product.objects.create(template_id=template, pin=pin, uid=uid, is_fake=True)



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_to_cart(request):
    if not request.auth:
        return Response({
            "error": 1, 
            "message": "ابتدا وارد سایت شوید",
            "type": "info" 
        })
    order,c = Order.objects.get_or_create(user_id=request.user, status="draft")
    template_id = request.data.get("template_id", None)
    count = request.data.get("count", 1)
    if not template_id:
        return Response({"error": 1, "message": "اطلاعات ناقص", "type": "error"})
    
    template = get_object_or_404(Product, pk=int(template_id))
    # template = get_object_or_404(ProductTemplate, pk=int(template_id))
    if not template:
        return Response({"error": 1,"message": "محصول یافت نشد", "type": "error"})
    
    line_with_same_id, created = order.orderline_set.get_or_create(product_id=template, market_id=template.market_id, defaults={"count": 1})
    if not created:
        line_with_same_id.count += 1

    # order.update_is_satisfied()
    line_with_same_id.save()
    order.save()
    return Response({"error": 0, "message": "افزوده شد", "type": "success"})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def increase_cart_item(request):
    if not request.auth:
        return Response({
            "error": 1, 
            "message": "ابتدا وارد سایت شوید",
            "type": "info" 
        })
    line_id = request.data.get("line_id", None)
    if not line_id:
        return Response({"error": 1, "message": "اطلاعات ناقص", "type": "error"})
    
    line = get_object_or_404(OrderLine, pk=int(line_id))
    # template = get_object_or_404(ProductTemplate, pk=int(template_id))
    if not line:
        return Response({"error": 1,"message": "خط سفارش یافت نشد", "type": "error"})
    
    line.count += 1

    # order.update_is_satisfied()
    line.save()
    return Response({"error": 0, "message": "افزوده شد", "type": "success"})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def decrease_cart_item(request):
    if not request.auth:
        return Response({
            "error": 1, 
            "message": "ابتدا وارد سایت شوید",
            "type": "info" 
        })
    line_id = request.data.get("line_id", None)
    if not line_id:
        return Response({"error": 1, "message": "اطلاعات ناقص", "type": "error"})
    
    line = get_object_or_404(OrderLine, pk=int(line_id))
    # template = get_object_or_404(ProductTemplate, pk=int(template_id))
    if not line:
        return Response({"error": 1,"message": "خط سفارش یافت نشد", "type": "error"})
    
    line.count -= 1

    # order.update_is_satisfied()
    line.save()
    return Response({"error": 0, "message": "ثبت شد", "type": "success"})



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def remove_cart_item(request):
    if not request.auth:
        return Response({"error": "کاربر یافت نشد"})
    line_id = request.data.get("line_id", None)
    if  line_id is None:
        return Response({"error": "اطلاعات ناقص"})
    
    line = get_object_or_404(OrderLine, pk=int(line_id))
    if not line:
        return Response({"error": "محصول یافت نشد"})
    
    line.delete()

    return Response({"error": 0,"message": "با موفقیت حذف شد"})


@api_view(['POST', 'DELETE'])
@authentication_classes([JWTAuthentication])
def delete_cart(request):
    if not request.auth:
        return Response({
            "error": 1, 
            "message": "ابتدا وارد سایت شوید",
            "type": "info" 
        })
    
    try:
        if not request.user.order_set.get(status="draft").orderline_set.all():
            return Response({
            "error": 1 ,
            "message": "سبد خرید شما خالی ست.",
            "type": "info"
        })
        f = request.user.order_set.get(status="draft").orderline_set.all().delete()
        request.user.order_set.get(status="draft").remove_discount()
        return Response({
            "error": 0,
            "message": "با موفقیت ثبت شد",
            "type": "success"
        })
    except Exception as e:
        return Response({
            "error": 1,
            "message": "خطا در انجام عملیات",
            "extra": str(e),
            "type": "error"
        })

