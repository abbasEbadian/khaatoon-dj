from market.models import Market
from .models import Message, Chat
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers import MessageSerializer, ChatSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
def get_market_chats(request):
    if request.user.market: 
        data = Chat.objects.filter( market=request.user.market )
        data = ChatSerializer(data, many=True).data
    else:
        data = []
    return Response (data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
def get_user_chats(request):
    data = Chat.objects.filter( user=request.user )
    data = ChatSerializer(data, many=True).data

    return Response (data)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def send_message(request):
    try:
        chat_id = request.data.get('chat_id', 0)
        text = request.data.get('text', 0)
        sender = request.data.get('sender', 0)

        chat = Chat.objects.get(id=int(chat_id))
        chat.message_set.create(text=text,sender=sender)

        return Response ({"error": 0, "message": "ایجاد شد", "chat": ChatSerializer(chat, many=False).data})

    except Exception as e:
        return Response ({"error": 1, "message": str(e)})


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def seen_message_from_market(request):
    try:
        chat_id = request.data.get('chat_id', 0)
        chat = Chat.objects.get(id=int(chat_id), market=request.user.market)
        
        for message in chat.message_set.filter(sender="user"):
            message.seen = True
            message.save() 

        return Response ({"error": 0})

    except Exception as e:
        return Response ({"error": 1, "message": str(e)})

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def seen_message_from_user(request):
    try:
        chat_id = request.data.get('chat_id', 0)

        chat = Chat.objects.get(id=int(chat_id), user=request.user)
        for message in chat.message_set.filter(sender="market"):
            message.seen = True
            message.save() 

        return Response ({"error": 0})

    except Exception as e:
        return Response ({"error": 1, "message": str(e)})

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def create_message_for_user(request):
    try:
        market = request.data.get('market_id', 0)
        market = Market.objects.get(pk=int(market))
        chat,created = Chat.objects.get_or_create(user=request.user, market=market)

        return Response ({"error": 0, "chat_id": chat.id})

    except Exception as e:
        return Response ({"error": 1, "message": str(e)})

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
def create_message_for_market(request):
    try:
        user_id = request.data.get('user_id', 0)
        user = User.objects.get(pk=int(user_id))
        chat, created= Chat.objects.get_or_create(user=user, market=request.user.market)

        return Response ({"error": 0, "chat_id": chat.id})

    except Exception as e:
        return Response ({"error": 1, "message": str(e)})
