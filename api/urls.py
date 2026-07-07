from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView, ProfileView,
    CategoryViewSet, ProductViewSet,
    CartAPIView, CartItemDeleteAPIView,
    OrderAPIView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Catalog (Handled automatically by the router)
    path('', include(router.urls)),
    
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    
    # Cart
    path('cart/', CartAPIView.as_view(), name='cart_api'),
    path('cart/item/<int:pk>/', CartItemDeleteAPIView.as_view(), name='cart_item_delete_api'),
    
    # Orders
    path('orders/', OrderAPIView.as_view(), name='order_api'),
]