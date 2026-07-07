from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from products.models import Category, Product
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem

from .serializers import (
    RegisterSerializer, UserSerializer, CategorySerializer, ProductSerializer,
    CartSerializer, OrderSerializer
)
from .permissions import IsAdminOrReadOnly

User = get_user_model()

# --- AUTH VIEWS ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# --- PRODUCT VIEWS ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True).select_related('category')
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

# --- CART VIEWS ---
class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        # Fixed IntegrityError by setting the price default
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'price': product.price} 
        )
        
        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        return Response({"message": "Item added to cart"}, status=status.HTTP_200_OK)

class CartItemDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        cart_item.delete()
        return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)

# --- ORDER VIEWS ---
class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            user=request.user,
            order_number=get_random_string(10).upper(), 
            total_amount=0 
        )
        
        total = 0
        for cart_item in cart.items.all():
            item_price = cart_item.product.price 
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=item_price,
                quantity=cart_item.quantity
            )
            total += (item_price * cart_item.quantity)
        
        order.total_amount = total
        order.save()
        
        # Empty the cart
        cart.items.all().delete()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)