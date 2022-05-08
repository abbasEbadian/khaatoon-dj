from rest_framework import serializers
from category.models import Category
from product.models import Product
from users.models import CustomUser
from favorite.models import Favorite
from reminder.models import Reminder
from market.models import Market, BusinessType
from state.models import Province, City
from attribute.models import Attribute, AttributeValue, ProductAttribute



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
        depth=3

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", 'persian_name', 'parent_id', 'url']

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(max_length="200")
    productattribute_set = ProductAttributeSerializer( many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        depth = 2
        
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




class MarketSerializer(serializers.ModelSerializer):
    # favorite_set = FavoriteSerializer( many=True, read_only=True)
    # reminder_set = ReminderSerializer( many=True, read_only=True)

    class Meta:
        model = Market
        fields = '__all__'
        # exclude = ('id', 'password', 'user_permissions', 'groups')
        depth = 2
        
class UserSerializer(serializers.ModelSerializer):
    favorite_set = FavoriteSerializer( many=True, read_only=True)
    reminder_set = ReminderSerializer( many=True, read_only=True)
    market = MarketSerializer(many=False, read_only=True)
    class Meta:
        model = CustomUser
        exclude = ('id', 'password', 'user_permissions', 'groups')
        depth = 2


    
