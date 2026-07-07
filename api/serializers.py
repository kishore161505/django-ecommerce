from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.models import Category, Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem

User = get_user_model()

# --- AUTH SERIALIZERS ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

# --- PRODUCT SERIALIZERS ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

# --- CART SERIALIZERS ---
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    # Using 'items' based on our previous troubleshooting
    items = CartItemSerializer(many=True, read_only=True, source='items')
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

# --- ORDER SERIALIZERS ---
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    # Depending on your OrderItem model, this might need to be 'orderitem_set' if 'items' throws an error
    items = OrderItemSerializer(many=True, read_only=True, source='items') 

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_number', 'status', 'total_amount', 'created_at', 'items']