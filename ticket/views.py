from xml.dom import ValidationErr
from django.shortcuts import render
from rest_framework.decorators import authentication_classes, api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import Ticket, TicketMessage
# from orders.models import Order
from django.contrib.auth import get_user_model
from django.db.models import Q
import difflib
from django.contrib import messages
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

#Rev
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_ticket(request):
    if not request.auth :
        return Response({"error": 1, "message": "ابتدا وارد سایت شوید.", "type": "info"})
    order_id = request.data.get('order_id', 0)
    section = request.data.get('section', 'پشتیبانی')
    title = request.data.get('title', '')
    content = request.data.get('content', '')
    priority = request.data.get('priority', 'کم')
    
    if not title or not content:
        return Response({"error": 1, "message": "اطلاعات ناقص", "type": "error"}
        )
    

    params = {
        "title":title,
        "user_id":request.user,
        "section":section,
        "priority":priority,
        "status":"pending"
    }
    # if order_id:
        # order = Order.objects.get(pk=int(order_id))
        # params["order_id"] = order

    ticket = Ticket.objects.create(   **params  )
    a = ticket.ticketmessage_set.create(message=content, user_id=request.user)
    a.save()
    ticket.save()
    

    return Response({"error": 0, "message": "تیکت با موفقیت ثبت شد.", "type": "success"})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_message(request):
    if not request.auth :
        return Response({"error": 1, "message": "ابتدا وارد سایت شوید.", "type": "info"})
    ticket_id = request.data.get('ticket_id', 0)
    message = request.data.get('message', '')
    
  

    ticket = Ticket.objects.get(id=ticket_id)
    if(not ticket or ticket.status == "closed"):
        return Response({"error": 1, "message": "تیکت بسته شده است", "type": "error"})
    if any([difflib.SequenceMatcher(None, message, x.message).ratio()>0.85 for x in  ticket.ticketmessage_set.all()]):
        return Response({"error": 1, "message": "متنی با تشابه تقریبی 85 درصد و بالاتر ، قبلا ارسال شده است.", "type": "error"})
    a = ticket.ticketmessage_set.create(message=message, user_id=request.user)
    a.save()
    ticket.save()
    

    return Response({"error": 0, "message": "تیکت با موفقیت ثبت شد.", "type": "success"})

@api_view(['POST', "GET"])
@authentication_classes([JWTAuthentication])
def close_ticket(request):
    if not request.auth :
        return Response({"error": 1, "message": "ابتدا وارد سایت شوید.", "type": "info"})
    try:
        ticket = Ticket.objects.get(id=request.data.get('id', 0))
        if ticket.user_id.id != request.user.id:
            raise Exception("")
    except Exception as e:
        return Response({"error": 1, "message": "یافت نشد", "type": "warning"})
    else:
        ticket.status = "closed"
        ticket.save()
        messages.add_message(request, messages.SUCCESS, 'بسته شد')
        return Response({"error": 0, "message": "بسته شد", "type": "success"})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def seen(request, pk):
    if not request.auth :
        return Response({"error": 1, "message": "ابتدا وارد سایت شوید.", "type": "info"})
    ticket = Ticket.objects.filter(id=pk).first()

    if ticket:
        ticket.seen_by_user = True
        ticket.save()
    
    return Response({"error": 0})



@login_required
# @api_view(('GET',"POST"))
# @authentication_classes([])
def close_ticket_admin(request, pk):
    ctx = {
        "user": request.user,
        "tickets" : Ticket.objects.all().order_by('-created'),
    }
    try:
        ticket = Ticket.objects.get(pk=pk)
    except Exception as e:
        return render(request, 'admin-panel/tickets/', ctx)
    else:
        ticket.status = "closed"
        ticket.save()
        messages.add_message(request, messages.SUCCESS, 'بسته شد')
    return render(request, 'admin-panel/tickets/', ctx)



from .models import ContactUs
@api_view(['POST'])
@authentication_classes([])
def send_contact_us_message(request):
    name = request.data.get('name', 'کاربر')
    email = request.data.get('email', '')
    message = request.data.get('message', '')

    if not name or not email or not message:
        return Response({"error": 1, "message": "اطلاعات ناقص", "type":"warning"})
    
    ContactUs.objects.create(name=name, email=email, message=message)
    return Response({"error": 0, "message": "َبا موفقیت ثبت شد.", "type": "success"})

