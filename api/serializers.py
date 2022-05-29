from rest_framework import serializers
from category.models import Category
from product.models import Product, ProductTemplate
from ticket.models import Ticket, TicketMessage
from users.models import CustomUser
from favorite.models import Favorite
from reminder.models import Reminder
from market.models import Market, BusinessType, Bank
from state.models import Province, City
from address.models import Address
from wallet.models import Wallet, Transaction
from message.models import Message, Chat
from order.models import Order, OrderLine
from attribute.models import Attribute, AttributeValue, ProductAttribute
from config.models import WebsiteConfiguration
from rest_framework.fields import CurrentUserDefault







class WebsiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteConfiguration
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    pstatus = serializers.CharField(max_length=200, source="persian_status")
    ptype = serializers.CharField(max_length=200, source="persian_type")
    class Meta:
        model = Transaction
        exclude = ('wallet_id', )
        depth=2

class WalletSerializer(serializers.ModelSerializer):
    transaction_set = TransactionSerializer(many=True, read_only=True)
    class Meta:
        model = Wallet
        exclude = ("user_id", )
        depth=2

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ("user_id", )
        depth=2
        
class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = "__all__"
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
        depth=2

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = "__all__"
        depth=2

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        exclude = ['product_id']
        depth=2

class CategorySerializer3(serializers.ModelSerializer):
    url = serializers.CharField(max_length="200")
    class Meta:
        model = Category
        fields = ["id", "name", 'persian_name', 'parent_id', 'url']
        depth=4

class CategorySerializer2(serializers.ModelSerializer):
    categories = CategorySerializer3(many=True, source="category_set") 
    parent = CategorySerializer3(many=False, source="parent_id")
    url = serializers.CharField(max_length="200")

    class Meta:
        model = Category
        fields = ["id", "name", 'persian_name', 'parent_id', 'url', 'categories', 'parent']
        depth=4

class CategorySerializer(serializers.ModelSerializer):    
    parent = CategorySerializer2( many=False,  source="parent_id")
    categories = CategorySerializer2(many=True, source="category_set") 
    url = serializers.CharField(max_length="200")

    class Meta:
        model = Category
        fields = ["id", "name", 'persian_name', 'parent_id', 'url', 'parent', 'categories']
        depth=4
class ProductTemplateSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer( many=True, read_only=True, source="productattribute_set")
    # category_id = CategorySerializer(many=False)

    class Meta:
        model = ProductTemplate
        exclude = ['product_id']

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length="200")
    _count = serializers.IntegerField(source="available_count")
    templates = ProductTemplateSerializer(many=True, read_only=True, source="producttemplate_set")
    attributes = ProductAttributeSerializer(many=True, read_only=True, source="productattribute_set")
    category_id = CategorySerializer(many=False)
    status_text = serializers.CharField(max_length="255")
    class Meta:
        model = Product
        fields = '__all__'
        depth = 3
        
class FavoriteSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(many=False, read_only=True)
    class Meta:
        model = Favorite
        exclude = ('user_id', )
        depth = 3

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        exclude = ('user_id', )
        depth = 2




class MarketSerializer2(serializers.ModelSerializer):
    products = ProductSerializer( many=True, read_only=True, source="product_set")
    # reminder_set = ReminderSerializer( many=True, read_only=True)
    
    class Meta:
        model = Market
        exclude = ['user', ]
        # exclude = ('id', 'password', 'user_permissions', 'groups')
        depth = 2

class SimpleUserSerializer(serializers.ModelSerializer):
    market = MarketSerializer2(many=False, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'avatar_image', 'market', 'is_superuser', 'is_staff']
        depth = 2

class TicketMessageSerializer(serializers.ModelSerializer):
    user_id = SimpleUserSerializer(many=False)

    class Meta:
        model = TicketMessage
        fields = "__all__"
        
class TicketSerializer(serializers.ModelSerializer):
    messages = TicketMessageSerializer(many=True, read_only=True, source="ticketmessage_set")
    class Meta:
        model = Ticket
        fields = '__all__'

class OrderLineSerializer(serializers.ModelSerializer):
    template_id = ProductTemplateSerializer(read_only=True)
    product_id = ProductSerializer(read_only=True)
    price = serializers.IntegerField(read_only=True, source="get_price")
    class Meta: 
        model = OrderLine
        exclude = ['order_id']
        depth = 5

class OrderSerializer2(serializers.ModelSerializer):
    class Meta: 
        model = Order
        exclude = ['user_id']
        depth = 2

class OrderSerializer(serializers.ModelSerializer):
    orderlines = OrderLineSerializer(source="orderline_set", many=True, read_only=True)
    sub_orderlines = OrderLineSerializer(source="original_lines", many=True, read_only=True)
    total = serializers.IntegerField(source="get_total", read_only=True)
    total_dis = serializers.IntegerField(source="get_discount", read_only=True)
    final_price = serializers.IntegerField(source="get_final_price", read_only=True)
    discount_code_amount = serializers.IntegerField(source="get_discount_code_amount", read_only=True)
    user_id = SimpleUserSerializer( many=False, read_only=True)
    products_count = serializers.IntegerField(source="get_products_count", read_only=True)
    status_text = serializers.CharField(source="get_status_text")
    sub_orders = OrderSerializer2(many=True)
    class Meta: 
        model = Order
        fields = '__all__'
        depth = 2

class MarketSerializer(serializers.ModelSerializer):
    products = ProductSerializer( many=True, read_only=True, source="product_set")
    orders = OrderSerializer(many=True, read_only=True, source="get_orders")
    
    class Meta:
        model = Market
        exclude = ['user', ]
        # exclude = ('id', 'password', 'user_permissions', 'groups')
        depth = 2

class UserSerializer(serializers.ModelSerializer):
    favorite_set = FavoriteSerializer( many=True, read_only=True)
    reminder_set = ReminderSerializer( many=True, read_only=True)
    address_set = AddressSerializer( many=True, read_only=True)
    market = MarketSerializer(many=False, read_only=True)
    wallet = WalletSerializer(many=False, read_only=True, source="wallet_id")
    tickets = TicketSerializer(many=True, read_only=True, source="ticket_set")
    orders = OrderSerializer(many=True, read_only=True, source="get_orders")
    unread_message_count = serializers.IntegerField(source="get_unread_messages_count")
    class Meta:
        model = CustomUser
        exclude = ('id', 'password', 'user_permissions', 'groups')
        depth = 2


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields= "__all__"
        depth = 2
    


class ChatSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer( many=False, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="message_set")
    class Meta:
        model = Chat
        fields= "__all__"
        depth=2


       